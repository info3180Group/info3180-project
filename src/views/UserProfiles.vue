<template>
  <div class="user-profiles container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>My Profiles</h2>
      <RouterLink to="/profiles/new" class="btn btn-primary">
        Create New Profile
      </RouterLink>
    </div>

    <div v-if="loading" class="text-center">
      <p>Loading profiles...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="profiles.length === 0" class="text-center">
      <p>You haven't created any profiles yet.</p>
      <RouterLink to="/profiles/new" class="btn btn-primary mt-3">
        Create Your First Profile
      </RouterLink>
    </div>

    <div v-else class="row">
      <div v-for="profile in profiles" :key="profile.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">Profile {{ profile.id }}</h5>
            <p class="card-text">{{ profile.description }}</p>
            
            <div class="profile-details">
              <ul class="list-unstyled">
                <li><strong>Parish:</strong> {{ profile.parish }}</li>
                <li><strong>Gender:</strong> {{ profile.sex }}</li>
                <li><strong>Age:</strong> {{ new Date().getFullYear() - profile.birth_year }}</li>
              </ul>
            </div>
            
            <div class="d-grid gap-2">
              <RouterLink 
                :to="`/profile/${profile.id}`" 
                class="btn btn-primary"
              >
                View Profile
              </RouterLink>
              <RouterLink 
                :to="`/profile/edit/${profile.id}`" 
                class="btn btn-outline-secondary"
              >
                Edit Profile
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'UserProfiles',
  setup() {
    const profiles = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const currentUser = JSON.parse(localStorage.getItem('user') || 'null');

    const fetchUserProfiles = async () => {
      try {
        const response = await axios.get('/api/profiles', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        profiles.value = response.data.filter(
          profile => profile.user_id_fk === currentUser.id
        );
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load profiles';
        console.error('Error loading profiles:', err);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchUserProfiles();
    });

    return {
      profiles,
      loading,
      error
    };
  }
};
</script>

<style scoped>
.user-profiles {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.profile-details {
  margin: 1rem 0;
}
</style>