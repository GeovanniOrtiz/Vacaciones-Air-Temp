'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { formatDate } from '@/lib/utils';
import { useRouter } from 'next/navigation';

interface VacationSummary {
    employee_id: number;
    employee_number: string;
    full_name: string;
    entry_date: string;
    years_of_service: number;
    completed_years: number;
    service_years: number;
    service_months: number;
    vacation_days: number;
    total_days: number;
    days_taken: number;
    days_remaining: number;
    usage_percentage: number;
    period_start: string;
    period_end: string;
    year: number;
}

interface VacationRecord {
    id: number;
    year: number;
    days_taken: number;
    start_date: string;
    end_date: string;
    description: string;
}

export default function ProfilePage() {
    const { user, loading } = useAuth();
    const [summary, setSummary] = useState<VacationSummary | null>(null);
    const [records, setRecords] = useState<VacationRecord[]>([]);
    const [fetching, setFetching] = useState(true);
    const router = useRouter();

    useEffect(() => {
        if (!loading && (!user || user.role !== 'employee')) {
            if (user?.role === 'admin') {
                router.push('/employees');
            } else {
                router.push('/login');
            }
            return;
        }

        if (user?.employee_id) {
            fetchProfileData();
        }
    }, [user, loading, router]);

    const fetchProfileData = async () => {
        const token = localStorage.getItem('auth_token');
        const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

        try {
            // Fetch summary
            const summaryRes = await fetch(`${API_URL}/api/employees/${user?.employee_id}/vacation-summary`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (summaryRes.ok) setSummary(await summaryRes.json());

            // Fetch records
            const recordsRes = await fetch(`${API_URL}/api/vacations/?employee_id=${user?.employee_id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (recordsRes.ok) setRecords(await recordsRes.json());
        } catch (error) {
            console.error('Error fetching profile data:', error);
        } finally {
            setFetching(false);
        }
    };

    if (loading || fetching) {
        return (
            <div className="flex items-center justify-center min-h-[calc(100vh-64px)]">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (!summary) return null;

    return (
        <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Mi Perfil de Vacaciones</h1>
                <p className="text-gray-600 mt-2">Bienvenido, {user?.username}. Aquí puedes ver tu historial y días disponibles.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Personal Info & Summary Card */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4 border-b pb-2">Información General</h2>
                        <div className="space-y-4">
                            <div>
                                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Número de Empleado</p>
                                <p className="text-lg font-medium text-gray-900">{summary.employee_number}</p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Nombre Completo</p>
                                <p className="text-lg font-medium text-gray-900">{summary.full_name}</p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Fecha de Ingreso</p>
                                <p className="text-lg font-medium text-gray-900">{formatDate(summary.entry_date)}</p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Antigüedad</p>
                                <p className="text-lg font-medium text-gray-900">{summary.service_years} años, {summary.service_months} meses</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-blue-600 rounded-2xl shadow-lg p-6 text-white">
                        <h2 className="text-lg font-semibold mb-4 opacity-90">Resumen del Periodo</h2>
                        <div className="space-y-6">
                            <div className="flex justify-between items-end">
                                <div>
                                    <p className="text-blue-100 text-sm">Días Disponibles</p>
                                    <p className="text-4xl font-bold">{summary.days_remaining}</p>
                                </div>
                                <div className="text-right">
                                    <p className="text-blue-100 text-sm">Total del Ciclo</p>
                                    <p className="text-xl font-semibold">{summary.total_days}</p>
                                </div>
                            </div>

                            <div className="w-full bg-blue-500/30 rounded-full h-3">
                                <div
                                    className="bg-white rounded-full h-3 transition-all duration-1000"
                                    style={{ width: `${summary.usage_percentage}%` }}
                                ></div>
                            </div>

                            <div className="grid grid-cols-2 gap-4 text-sm">
                                <div className="bg-white/10 rounded-xl p-3">
                                    <p className="opacity-70">Tomados</p>
                                    <p className="text-lg font-bold">{summary.days_taken}</p>
                                </div>
                                <div className="bg-white/10 rounded-xl p-3">
                                    <p className="opacity-70">Ciclo</p>
                                    <p className="font-medium">{summary.year}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* History Table */}
                <div className="lg:col-span-2">
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
                            <h2 className="text-lg font-semibold text-gray-900">Historial de Vacaciones</h2>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Periodo</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Días</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ciclo</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {records.length > 0 ? (
                                        records.map((record) => (
                                            <tr key={record.id} className="hover:bg-gray-50 transition-colors">
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                    {formatDate(record.start_date)} - {formatDate(record.end_date)}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-blue-600">
                                                    {record.days_taken}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                    {record.year}
                                                </td>
                                                <td className="px-6 py-4 text-sm text-gray-500">
                                                    {record.description || '-'}
                                                </td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan={4} className="px-6 py-10 text-center text-gray-500">
                                                No tienes registros de vacaciones todavía.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}
