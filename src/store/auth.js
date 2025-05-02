import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apiClient } from '@/services/api'; // Import the configured Axios instance
import router from '@/router'; // Import router for redirects

// Define the authentication store using Pinia
export const useAuthStore = defineStore('auth', () => {
    // --- State ---
    // Reactive references for user data, CSRF token, and loading state
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null')); // Load user from localStorage
    const csrfToken = ref(null);
    const isLoading = ref(false); // Track loading state for UI feedback
    const error = ref(null); // Store potential errors

    // --- Getters ---
    // Computed property to determine if the user is authenticated
    const isAuthenticated = computed(() => !!user.value);
    // Computed property to get the user ID safely
    const userId = computed(() => user.value?.id || null);

    // --- Actions ---

    /**
     * Fetches the CSRF token from the backend.
     */
    async function fetchCsrfToken() {
        // Avoid fetching if already loading or token exists
        if (isLoading.value || csrfToken.value) return;

        isLoading.value = true; // Set loading state
        error.value = null; // Clear previous errors
        try {
            // Make GET request to the backend endpoint for CSRF token
            const response = await apiClient.get('/v1/csrf-token');
            csrfToken.value = response.data.csrf_token; // Store the fetched token
            console.log("CSRF token fetched successfully.");
        } catch (err) {
            console.error("Failed to fetch CSRF token:", err.response?.data || err.message);
            error.value = "Could not initialize security token. Please try again later."; // Set error message
            csrfToken.value = null; // Ensure token is null on failure
        } finally {
            isLoading.value = false; // Reset loading state
        }
    }

    /**
     * Logs in the user with provided credentials.
     * @param {object} credentials - { username, password }
     * @param {string | null} redirectPath - Path to redirect to after successful login.
     */
    async function login(credentials, redirectPath = null) {
        if (isLoading.value) return false; // Prevent multiple login attempts

        isLoading.value = true;
        error.value = null;
        let loginSuccess = false;
        try {
            // Ensure CSRF token is available before attempting login (POST request)
            if (!csrfToken.value) {
                await fetchCsrfToken();
                if (!csrfToken.value) { // Check again if fetch failed
                     throw new Error("CSRF token is missing. Cannot log in.");
                }
            }

            // Make POST request to the backend login endpoint
            const response = await apiClient.post('/auth/login', credentials);
            user.value = response.data.user; // Store user data
            localStorage.setItem('user', JSON.stringify(user.value)); // Persist user data in localStorage
            console.log("Login successful:", user.value.username);
            loginSuccess = true;

            // Redirect after successful login
            router.push(redirectPath || '/'); // Redirect to intended path or home

        } catch (err) {
            console.error("Login failed:", err.response?.data || err.message);
            const backendError = err.response?.data?.error;
            error.value = backendError || "Login failed. Please check your username and password.";
            logout(); // Clear any potentially partially set state on failure
            loginSuccess = false;
        } finally {
            isLoading.value = false;
        }
        return loginSuccess; // Return success status
    }

    /**
     * Registers a new user.
     * @param {FormData} formData - User registration data including photo (as FormData).
     */
    async function register(formData) {
        if (isLoading.value) return false;

        isLoading.value = true;
        error.value = null;
        let registerSuccess = false;
        try {
             // Ensure CSRF token is available before attempting registration (POST request)
            if (!csrfToken.value) {
                await fetchCsrfToken();
                 if (!csrfToken.value) { // Check again if fetch failed
                     throw new Error("CSRF token is missing. Cannot register.");
                 }
            }

            // Make POST request to the backend register endpoint
            // Axios automatically sets 'Content-Type': 'multipart/form-data' for FormData
            await apiClient.post('/register', formData);
            console.log("Registration successful.");
            registerSuccess = true;
            // Optionally redirect to login page after successful registration
            router.push('/login');

        } catch (err) {
            console.error("Registration failed:", err.response?.data || err.message);
             // Extract specific errors if the backend provides them (e.g., username taken)
             const backendErrors = err.response?.data;
             if (backendErrors && typeof backendErrors === 'object') {
                 // Format backend validation errors nicely
                 error.value = Object.entries(backendErrors)
                     .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
                     .join('; ');
             } else {
                 error.value = "Registration failed. Please check your input and try again.";
             }
            registerSuccess = false;
        } finally {
            isLoading.value = false;
        }
        return registerSuccess;
    }

    /**
     * Logs out the current user.
     */
    async function logout() {
        console.log("Logging out user...");
        // Optional: Call backend logout endpoint if it performs server-side cleanup
        // try {
        //     if (csrfToken.value) { // Need CSRF for POST
        //         await apiClient.post('/auth/logout');
        //     }
        // } catch (err) {
        //     console.error("Backend logout failed (might be okay if stateless):", err.response?.data || err.message);
        // }

        // Clear local state
        user.value = null;
        csrfToken.value = null; // Clear CSRF token on logout
        localStorage.removeItem('user'); // Remove user from localStorage
        // No need to clear error/loading here as it's usually followed by redirect

        // Redirect to login page after logout
        // Use replace to prevent going back to the logged-in state
        router.replace('/login');
    }

    // --- Initialization ---
    // Fetch CSRF token when the store is initialized (or on demand)
    // fetchCsrfToken(); // Fetch immediately, or let components trigger it

    // --- Return ---
    // Expose state, getters, and actions
    return {
        user,
        csrfToken,
        isLoading,
        error,
        isAuthenticated,
        userId,
        fetchCsrfToken,
        login,
        register,
        logout
    };
});
