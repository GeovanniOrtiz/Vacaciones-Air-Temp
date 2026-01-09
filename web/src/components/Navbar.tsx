'use client';

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";

export function Navbar() {
    const { user, logout } = useAuth();

    return (
        <nav className="bg-white border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex">
                        <div className="flex-shrink-0 flex items-center">
                            <Link href="/" className="text-xl font-bold text-blue-600">
                                Departamento de Integracion
                            </Link>
                        </div>
                        <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                            <Link
                                href="/"
                                className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                            >
                                Inicio
                            </Link>
                            {user?.role === 'admin' && (
                                <>
                                    <Link
                                        href="/employees"
                                        className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                                    >
                                        Empleados
                                    </Link>
                                    <Link
                                        href="/users"
                                        className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                                    >
                                        Usuarios
                                    </Link>
                                </>
                            )}
                        </div>
                    </div>
                    <div className="flex items-center">
                        {user ? (
                            <div className="flex items-center space-x-4">
                                <div className="text-sm text-gray-700">
                                    <span className="font-medium">{user.username}</span>
                                    <span className="ml-1 text-gray-500">({user.role})</span>
                                </div>
                                {user.role === 'employee' && (
                                    <Link
                                        href="/profile"
                                        className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                                    >
                                        Mi Perfil
                                    </Link>
                                )}
                                <button
                                    onClick={logout}
                                    className="text-sm text-red-600 hover:text-red-800 font-medium"
                                >
                                    Cerrar Sesión
                                </button>
                            </div>
                        ) : (
                            <Link
                                href="/login"
                                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                            >
                                Iniciar Sesión
                            </Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}
