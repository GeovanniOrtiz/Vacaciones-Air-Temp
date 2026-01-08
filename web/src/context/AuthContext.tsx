'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, getCurrentUser, logout as authLogout, isAuthenticated } from '@/lib/auth';
import { useRouter, usePathname } from 'next/navigation';

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: (token: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    const pathname = usePathname();

    const fetchUser = async () => {
        try {
            if (isAuthenticated()) {
                const userData = await getCurrentUser();
                setUser(userData);
            } else {
                setUser(null);
            }
        } catch (error) {
            console.error('Error fetching user:', error);
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUser();
    }, []);

    const login = async (token: string) => {
        setLoading(true);
        localStorage.setItem('auth_token', token);
        await fetchUser();
        router.push('/');
    };

    const logout = () => {
        authLogout();
        setUser(null);
        router.push('/login');
    };

    // Redirect to login if not authenticated and not on login page
    useEffect(() => {
        if (!loading && !user && pathname !== '/login') {
            router.push('/login');
        }
    }, [user, loading, pathname, router]);

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
