import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// Define the authentication store using Pinia
export const useAuthStore = defineStore('auth', () => {
  // --- State ---
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null')); // Load user from localStorage
  const token = ref(localStorage.getItem('token') || null); // Load token from localStorage

  // --- Getters ---
  const isAuthenticated = computed(() => !!token.value); // Determine if the user is authenticated

  // --- Actions ---
  /**
   * Sets the user data and persists it in localStorage.
   * @param {object} userData - User data to store.
   */
  function setUser(userData) {
    user.value = userData;
    localStorage.setItem('user', JSON.stringify(userData));
  }

  /**
   * Sets the authentication token and persists it in localStorage.
   * @param {string} newToken - Token to store.
   */
  function setToken(newToken) {
    token.value = newToken;
    localStorage.setItem('token', newToken);
  }

  /**
   * Logs out the current user and clears localStorage.
   */
  function logout() {
    user.value = null;
    token.value = null;
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  }

  // --- Return ---
  // Expose state, getters, and actions
  return {
    user,
    token,
    isAuthenticated,
    setUser,
    setToken,
    logout
  };
});
