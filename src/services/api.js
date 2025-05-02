import axios from 'axios';
import { useAuthStore } from '@/stores/auth'; // Import Pinia auth store

// --- Configuration ---
// IMPORTANT: Replace with your actual Flask backend URL
const API_BASE_URL = 'http://127.0.0.1:8080/api'; // Updated base URL
// IMPORTANT: Replace with the base URL where user photos are served
// This might require a dedicated route in your Flask app (e.g., /uploads/<filename>)
const PHOTO_BASE_URL = 'http://localhost:5000/uploads/'; // Example placeholder

// --- Axios Instance ---
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Accept': 'application/json',
        // 'Content-Type' will be set by Axios based on data (e.g., application/json or multipart/form-data)
    },
    // withCredentials: true // Uncomment if you need to send cookies (e.g., for session-based auth)
});

// --- Interceptors ---

// Request Interceptor: Inject CSRF token before sending requests
apiClient.interceptors.request.use(async (config) => {
    const authStore = useAuthStore(); // Get auth store instance

    // Add CSRF token for methods that typically require it (POST, PUT, DELETE, PATCH)
    // Flask-WTF usually expects it in the 'X-CSRFToken' header
    if (['post', 'put', 'delete', 'patch'].includes(config.method?.toLowerCase())) {
        // Ensure CSRF token is fetched if not already available
        if (!authStore.csrfToken) {
            await authStore.fetchCsrfToken(); // Fetch CSRF token on demand
        }
        // Add the token to the header if available
        if (authStore.csrfToken) {
            config.headers['X-CSRFToken'] = authStore.csrfToken;
        } else {
             // Handle case where CSRF token couldn't be fetched (optional)
             console.warn('CSRF token is missing. Request might fail.');
             // You might want to prevent the request here or notify the user
        }
    }

    // Example: Add Authorization header if using JWT tokens (uncomment if needed)
    // if (authStore.token) {
    //     config.headers.Authorization = `Bearer ${authStore.token}`;
    // }

    return config; // Continue with the modified request config
}, (error) => {
    // Handle request configuration errors
    console.error("API Request Error:", error);
    return Promise.reject(error);
});

// Response Interceptor (Optional): Handle global errors like 401 Unauthorized
apiClient.interceptors.response.use(
    (response) => response, // Pass through successful responses
    (error) => {
        const authStore = useAuthStore();
        // Example: Handle 401 Unauthorized - redirect to login or refresh token
        if (error.response && error.response.status === 401) {
            console.error('Unauthorized access - 401');
            // authStore.logout(); // Log out the user
            // router.push('/login'); // Redirect to login page
            // Or attempt token refresh if using JWT refresh tokens
        }
         // Handle other errors globally if needed
         console.error('API Response Error:', error.response?.data || error.message);

        return Promise.reject(error); // Propagate the error
    }
);


// --- Helper Function ---

/**
 * Constructs the full URL for a user's photo.
 * @param {string | null | undefined} photoFilename - The filename from the backend.
 * @returns {string} - The full photo URL or a placeholder.
 */
function getUserPhotoUrl(photoFilename) {
    if (photoFilename) {
        // Basic check to prevent constructing URLs for invalid filenames
        if (typeof photoFilename === 'string' && photoFilename.trim() !== '') {
             // Use placeholder if PHOTO_BASE_URL is not configured
             if (!PHOTO_BASE_URL || PHOTO_BASE_URL === 'http://localhost:5000/uploads/') {
                 console.warn("PHOTO_BASE_URL not configured in api.js, using placeholder.");
                 // Simple text placeholder
                 return `https://placehold.co/100x100/e2e8f0/64748b?text=${photoFilename.charAt(0).toUpperCase()}`;
             }
             return `${PHOTO_BASE_URL}${encodeURIComponent(photoFilename)}`;
        }
    }
    // Return a generic placeholder if no filename is provided
    return 'https://placehold.co/100x100/e2e8f0/64748b?text=N/A';
}


export { apiClient, getUserPhotoUrl, API_BASE_URL, PHOTO_BASE_URL }; // Export the configured client and helper
