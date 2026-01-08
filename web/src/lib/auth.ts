/**
 * Authentication library for the web application
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface User {
    id: number;
    username: string;
    role: 'admin' | 'employee';
    employee_id?: number;
    is_active: number;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

/**
 * Login with username and password
 */
export async function login(username: string, password: string): Promise<AuthResponse> {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error al iniciar sesión');
    }

    const data = await response.json();
    // Store token in localStorage
    if (typeof window !== 'undefined') {
        localStorage.setItem('auth_token', data.access_token);
    }
    return data;
}

/**
 * Get current user profile
 */
export async function getCurrentUser(): Promise<User> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
    if (!token) throw new Error('No hay sesión activa');

    const response = await fetch(`${API_URL}/auth/me`, {
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        if (response.status === 401) {
            logout();
        }
        throw new Error('Error al obtener el perfil');
    }

    return response.json();
}

/**
 * Logout and clear session
 */
export function logout() {
    if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
    }
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
    if (typeof window !== 'undefined') {
        return !!localStorage.getItem('auth_token');
    }
    return false;
}
