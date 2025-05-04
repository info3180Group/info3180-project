<script setup>
import { ref } from "vue";

const message = ref("Welcome to the Jam Date!");
const subMessage = ref("Your ultimate date-matching application designed to help you find meaningful connections");
</script>

<template>
  <div class="container home-page">
    <div class="text-center py-5">
      <img 
        alt="Vue logo" 
        class="logo mb-4" 
        src="@/assets/logo.svg" 
        width="125" 
        height="125" 
      />
      <h1 class="mb-3">{{ message }}</h1>
      <p class="lead mb-4">{{ subMessage }}</p>

      <div>
        <router-link to="/my-profile" class="btn btn-primary me-3">
          View Your Profile
        </router-link>
        <router-link to="/matches" class="btn btn-outline-success">
          Find Matches
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page h1 {
  font-size: 2.25rem;
  font-weight: bold;
}

.logo {
  animation: pulse 3s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.9; }
  100% { transform: scale(1); opacity: 1; }
}

.lead {
  font-size: 1.1rem;
  color: #555;
}
</style>
