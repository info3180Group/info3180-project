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
              <RouterLink 
                to="/" 
                class="nav-link"
                exact-active-class="active"
              >
                Home
              </RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink 
                class="nav-link" 
                to="/about"
                active-class="active"
              >
                About
              </RouterLink>
            </li>
            <!-- Show these items only when user is NOT logged in -->
            <template v-if="!authStore.isAuthenticated">
              <li class="nav-item">
                <RouterLink 
                  class="nav-link" 
                  to="/login"
                  active-class="active"
                >
                  Login
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink 
                  class="nav-link" 
                  to="/register"
                  active-class="active"
                >
                  Register
                </RouterLink>
              </li>
            </template>
            <!-- Show these items only when user is logged in -->
            <template v-else>
              <li class="nav-item">
                <RouterLink 
                  class="nav-link" 
                  to="/my-profile"
                  active-class="active"
                >
                  My Profile
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink 
                  class="nav-link" 
                  to="/profiles"
                  active-class="active"
                >
                  Profiles
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink 
                  class="nav-link" 
                  to="/matches"
                  active-class="active"
                >
                  Matches
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink 
                  class="nav-link" 
                  to="/top-profiles"
                  active-class="active"
                >
                  Top Profiles
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink 
                  class="nav-link" 
                  to="/my-profiles"
                  active-class="active"
                >
                  My Profiles
                </RouterLink>
              </li>
              <li class="nav-item">
                <a 
                  class="nav-link" 
                  href="#" 
                  @click.prevent="handleLogout"
                >
                  Logout
                </a>
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
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';

const router = useRouter();
const authStore = useAuthStore();

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>

.navbar-brand {
  font-weight: 700;
  font-size: 1.4rem;
  color: #fff !important;
  letter-spacing: 0.5px;
}


.nav-link {
  position: relative;
  padding: 0.5rem 1rem;
  font-weight: 500;
  color: #f0f0f0 !important;
  transition: all 0.3s ease;
}


.nav-link:hover,
.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: #ffffff !important;
  font-weight: 600;
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


body {
  padding-top: 70px; 
}
</style>
