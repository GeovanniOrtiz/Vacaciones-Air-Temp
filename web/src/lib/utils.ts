/**
 * Utility functions for the web application
 */

/**
 * Formats a date string (YYYY-MM-DD) to a localized string (es-MX)
 * without timezone shifts.
 */
export function formatDate(dateString: string | null | undefined): string {
    if (!dateString) return 'N/A';

    try {
        // Handle YYYY-MM-DD format specifically to avoid UTC shift
        if (typeof dateString === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(dateString)) {
            const [year, month, day] = dateString.split('-').map(Number);
            // new Date(year, monthIndex, day) creates a date in local time
            const date = new Date(year, month - 1, day);
            return date.toLocaleDateString('es-MX');
        }

        // Fallback for other formats
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return 'N/A';

        return date.toLocaleDateString('es-MX');
    } catch (error) {
        console.error('Error formatting date:', error);
        return 'N/A';
    }
}
