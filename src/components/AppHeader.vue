<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Jam-Date</a>
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


<style scoped>
/* Customize the brand */
.navbar-brand {
  font-weight: 700;
  font-size: 1.4rem;
  color: #fff !important;
  letter-spacing: 0.5px;
}

/* Nav link appearance */
.nav-link {
  font-weight: 500;
  color: #f0f0f0 !important;
  transition: color 0.3s ease, background-color 0.3s ease;
}

/* Active or hovered nav link */
.nav-link:hover,
.nav-link.active {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #ffffff !important;
}

/* Navbar container spacing */
.navbar .container-fluid {
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Nav items spacing */
.nav-item {
  margin-left: 0.5rem;
  margin-right: 0.5rem;
}

/* Toggle button icon color override */
.navbar-toggler {
  border: none;
}

.navbar-toggler-icon {
  filter: brightness(0) invert(1); /* ensure it's white */
}

/* Fix for top spacing due to fixed-top */
body {
  padding-top: 70px; /* adjust if navbar height changes */
}
</style>
