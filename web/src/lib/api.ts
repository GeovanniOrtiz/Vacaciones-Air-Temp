const API_BASE_URL = 'http://127.0.0.1:8000/api';

export interface Employee {
    id: number;
    employee_number: string;
    full_name: string;
    entry_date: string;
    department?: string;
    position?: string;
    email?: string;
    phone?: string;
}

export interface VacationSummary {
    employee_id: number;
    employee_number: string;
    full_name: string;
    entry_date: string;
    entry_year: number;
    current_year: number;
    years_of_service: number;
    completed_years: number;
    service_years: number;
    service_months: number;
    vacation_days: number;
    vacation_premium_percentage: number;
    vacation_premium_days: number;
    next_increase_years: number;
    next_vacation_days: number;
    year: number;
    total_days: number;
    days_taken: number;
    days_remaining: number;
    usage_percentage: number;
    period_start: string;
    period_end: string;
}

async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
    const headers = {
        ...options.headers,
        'Authorization': token ? `Bearer ${token}` : '',
    };

    const res = await fetch(url, { ...options, headers });
    if (res.status === 401) {
        if (typeof window !== 'undefined') {
            localStorage.removeItem('auth_token');
            window.location.href = '/login';
        }
    }
    return res;
}

export async function getEmployees(search?: string): Promise<Employee[]> {
    const url = new URL(`${API_BASE_URL}/employees/`);
    if (search) {
        url.searchParams.append('search', search);
    }

    const res = await fetchWithAuth(url.toString());
    if (!res.ok) throw new Error('Failed to fetch employees');
    return res.json();
}

export async function getEmployee(id: number): Promise<Employee> {
    const res = await fetchWithAuth(`${API_BASE_URL}/employees/${id}`);
    if (!res.ok) throw new Error('Failed to fetch employee');
    return res.json();
}

export async function getVacationSummary(id: number, year?: number): Promise<VacationSummary> {
    const url = new URL(`${API_BASE_URL}/employees/${id}/vacation-summary`);
    if (year) {
        url.searchParams.append('year', year.toString());
    }

    const res = await fetchWithAuth(url.toString());
    if (!res.ok) throw new Error('Failed to fetch vacation summary');
    return res.json();
}

export interface VacationRecord {
    id: number;
    employee_id: number;
    year: number;
    days_taken: number;
    start_date: string;
    end_date: string;
    description?: string;
    created_at: string;
}

export interface User {
    id: number;
    username: string;
    role: 'admin' | 'employee';
    employee_id?: number;
    is_active: number;
    employee?: Employee;
}

export async function getUsers(): Promise<User[]> {
    const res = await fetchWithAuth(`${API_BASE_URL.replace('/api', '')}/api/users/`);
    if (!res.ok) throw new Error('Failed to fetch users');
    return res.json();
}

export async function updateUserPassword(userId: number, password: string): Promise<any> {
    const res = await fetchWithAuth(`${API_BASE_URL.replace('/api', '')}/api/users/${userId}/password`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
    });
    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'Failed to update password');
    }
    return res.json();
}

export async function deleteUser(userId: number): Promise<any> {
    const res = await fetchWithAuth(`${API_BASE_URL.replace('/api', '')}/api/users/${userId}`, {
        method: 'DELETE'
    });
    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'Failed to delete user');
    }
    return res.json();
}

export async function getVacationRecords(employeeId: number): Promise<VacationRecord[]> {
    const url = new URL(`${API_BASE_URL}/vacations/`);
    url.searchParams.append('employee_id', employeeId.toString());

    const res = await fetchWithAuth(url.toString());
    if (!res.ok) throw new Error('Failed to fetch vacation records');
    return res.json();
}
