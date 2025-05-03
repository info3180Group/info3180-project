<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">VueJS with Flask</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">About</RouterLink>
            </li>
            <!-- Show these items only when user is NOT logged in -->
            <template v-if="!isAuthenticated">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/login">Login</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/register">Register</RouterLink>
              </li>
            </template>
            <!-- Show these items only when user is logged in -->
            <template v-else>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/my-profile">My Profile</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/profiles">Profiles</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/matches">Matches</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/top-profiles">Top Profiles</RouterLink>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" @click.prevent="handleLogout">Logout</a>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Check if user is authenticated by looking for token in localStorage
const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token');
});

// Logout handler
const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login');
};
</script>

<style>
/* Add any component specific styles here */
</style>