'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { getEmployee, getVacationSummary, getVacationRecords, Employee, VacationSummary, VacationRecord } from '@/lib/api';
import { formatDate } from '@/lib/utils';

export default function EmployeeDetails() {
    const params = useParams();
    const employeeId = parseInt(params.id as string);

    const [employee, setEmployee] = useState<Employee | null>(null);
    const [summary, setSummary] = useState<VacationSummary | null>(null);
    const [records, setRecords] = useState<VacationRecord[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchData = async () => {
        try {
            const [empData, summaryData, recordsData] = await Promise.all([
                getEmployee(employeeId),
                getVacationSummary(employeeId),
                getVacationRecords(employeeId)
            ]);
            setEmployee(empData);
            setSummary(summaryData);
            setRecords(recordsData);
        } catch (err: any) {
            setError(err.message || 'Error al cargar los datos');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000);
        return () => clearInterval(interval);
    }, [employeeId]);

    if (loading && !employee) {
        return (
            <main className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-7xl mx-auto">
                    <div className="text-center py-12">Cargando...</div>
                </div>
            </main>
        );
    }

    if (error && !employee) {
        return (
            <main className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-7xl mx-auto">
                    <div className="bg-red-50 text-red-700 p-4 rounded-lg">
                        Error: {error}
                    </div>
                    <Link href="/employees" className="text-blue-600 hover:text-blue-800 mt-4 inline-block">
                        ← Volver a la lista
                    </Link>
                </div>
            </main>
        );
    }

    if (!employee) {
        return (
            <main className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-7xl mx-auto">
                    <div className="text-center py-12 text-gray-500">Empleado no encontrado</div>
                    <Link href="/employees" className="text-blue-600 hover:text-blue-800 mt-4 inline-block">
                        ← Volver a la lista
                    </Link>
                </div>
            </main>
        );
    }

    return (
        <main className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-7xl mx-auto">
                <Link href="/employees" className="text-blue-600 hover:text-blue-800 mb-4 inline-block">
                    ← Volver a la lista
                </Link>

                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                    <h1 className="text-3xl font-bold text-gray-900 mb-4">{employee.full_name}</h1>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <p className="text-sm text-gray-500">Número de Empleado</p>
                            <p className="text-lg font-medium text-gray-900">{employee.employee_number}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-500">Fecha de Ingreso</p>
                            <p className="text-lg font-medium text-gray-900">
                                {formatDate(employee.entry_date)}
                            </p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-500">Departamento</p>
                            <p className="text-lg font-medium text-gray-900">{employee.department || 'N/A'}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-500">Puesto</p>
                            <p className="text-lg font-medium text-gray-900">{employee.position || 'N/A'}</p>
                        </div>
                        {employee.email && (
                            <div>
                                <p className="text-sm text-gray-500">Email</p>
                                <p className="text-lg font-medium text-gray-900">{employee.email}</p>
                            </div>
                        )}
                        {employee.phone && (
                            <div>
                                <p className="text-sm text-gray-500">Teléfono</p>
                                <p className="text-lg font-medium text-gray-900">{employee.phone}</p>
                            </div>
                        )}
                    </div>
                </div>

                {summary && (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h2 className="text-2xl font-bold text-gray-900 mb-6">Resumen de Vacaciones</h2>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                            <div className="bg-blue-50 p-4 rounded-lg">
                                <p className="text-sm text-blue-700 font-medium">Antigüedad</p>
                                <p className="text-2xl font-bold text-blue-900">
                                    {summary.service_years} años {summary.service_months} meses
                                </p>
                            </div>

                            <div className="bg-green-50 p-4 rounded-lg">
                                <p className="text-sm text-green-700 font-medium">Días Disponibles</p>
                                <p className="text-2xl font-bold text-green-900">{summary.vacation_days}</p>
                            </div>

                            <div className="bg-orange-50 p-4 rounded-lg">
                                <p className="text-sm text-orange-700 font-medium">Días Tomados</p>
                                <p className="text-2xl font-bold text-orange-900">{summary.days_taken}</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="border border-gray-200 p-4 rounded-lg">
                                <p className="text-sm text-gray-500">Días Restantes</p>
                                <p className="text-3xl font-bold text-gray-900">{summary.days_remaining}</p>
                                <div className="mt-2 bg-gray-200 rounded-full h-2">
                                    <div
                                        className="bg-blue-600 h-2 rounded-full transition-all"
                                        style={{
                                            width: `${Math.max(0, Math.min(100, (summary.days_remaining / summary.vacation_days) * 100))}%`
                                        }}
                                    />
                                </div>
                            </div>

                            <div className="border border-gray-200 p-4 rounded-lg">
                                <p className="text-sm text-gray-500">Prima Vacacional</p>
                                <p className="text-3xl font-bold text-gray-900">{summary.vacation_premium_percentage}%</p>
                            </div>
                        </div>

                        <div className="mt-6 pt-6 border-t border-gray-200">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                                <div>
                                    <p className="text-gray-500">Periodo Actual</p>
                                    <p className="font-medium text-gray-900">
                                        {formatDate(summary.period_start)} - {formatDate(summary.period_end)}
                                    </p>
                                </div>
                                <div>
                                    <p className="text-gray-500">Año de Servicio</p>
                                    <p className="font-medium text-gray-900">{summary.current_year}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {records.length > 0 && (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mt-6">
                        <h2 className="text-2xl font-bold text-gray-900 mb-6">Historial de Vacaciones</h2>
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Periodo
                                        </th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Días
                                        </th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Descripción
                                        </th>
                                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Año
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {records.map((record) => (
                                        <tr key={record.id}>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                {formatDate(record.start_date)} - {formatDate(record.end_date)}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                {record.days_taken}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-500">
                                                {record.description || '-'}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {record.year}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </div>
        </main>
    );
}
