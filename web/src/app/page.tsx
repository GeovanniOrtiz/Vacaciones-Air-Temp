'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { getEmployees, Employee } from '@/lib/api';

export default function Home() {
  const { user, loading: authLoading } = useAuth();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    if (!authLoading && user?.role === 'employee') {
      router.push('/profile');
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (authLoading || !user || user.role !== 'admin') return;

    const fetchData = () => {
      getEmployees()
        .then(setEmployees)
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [user, authLoading]);

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-64px)]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Sistema de Vacaciones</h1>
          <p className="text-gray-600 mt-2">Panel de Control</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-700">Total Empleados</h3>
            <p className="text-3xl font-bold text-blue-600 mt-2">
              {loading ? '...' : employees.length}
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-700">Acciones Rápidas</h3>
            <div className="mt-4 space-y-2">
              <Link
                href="/employees"
                className="block text-center bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
              >
                Ver Empleados
              </Link>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-6">
            Error: {error}
          </div>
        )}

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-800">Empleados Recientes</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {loading ? (
              <div className="p-6 text-center text-gray-500">Cargando...</div>
            ) : (
              employees.slice(0, 5).map((emp) => (
                <div key={emp.id} className="p-6 hover:bg-gray-50 transition flex justify-between items-center">
                  <div>
                    <h4 className="font-medium text-gray-900">{emp.full_name}</h4>
                    <p className="text-sm text-gray-500">{emp.position} - {emp.department}</p>
                  </div>
                  <Link
                    href={`/employees/${emp.id}`}
                    className="text-blue-600 hover:text-blue-800 font-medium text-sm"
                  >
                    Ver Detalles →
                  </Link>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
