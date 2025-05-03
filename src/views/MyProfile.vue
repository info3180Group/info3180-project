<template>
  <div class="my-profile container">
    <h2>My Profile</h2>
    
    <div v-if="loading" class="text-center">
      <p>Loading profile...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else-if="!profile" class="text-center">
      <div class="alert alert-info">
        <p>You haven't created a profile yet!</p>
        <RouterLink to="/profile/edit" class="btn btn-primary mt-3">
          Create Profile
        </RouterLink>
      </div>
    </div>
    
    <div v-else class="profile-content">
      <div class="row">
        <div class="col-md-4">
          <div class="profile-photo-container mb-3">
            <img 
              :src="currentUser.photo ? `/uploads/${currentUser.photo}` : '/default-profile.jpg'" 
              :alt="currentUser.name"
              class="profile-photo img-fluid rounded"
            />
          </div>
          <RouterLink to="/profile/edit" class="btn btn-primary w-100">
            Edit Profile
          </RouterLink>
        </div>
        
        <div class="col-md-8">
          <h3>{{ currentUser.name }}</h3>
          <p class="lead">{{ profile.description }}</p>
          
          <div class="profile-details mt-4">
            <h4>Personal Information</h4>
            <ul class="list-unstyled">
              <li><strong>Age:</strong> {{ new Date().getFullYear() - profile.birth_year }}</li>
              <li><strong>Parish:</strong> {{ profile.parish }}</li>
              <li><strong>Gender:</strong> {{ profile.sex }}</li>
              <li><strong>Race:</strong> {{ profile.race }}</li>
              <li><strong>Height:</strong> {{ profile.height }}cm</li>
            </ul>

            <h4 class="mt-4">Preferences</h4>
            <ul class="list-unstyled">
              <li><strong>Favorite Cuisine:</strong> {{ profile.fav_cuisine }}</li>
              <li><strong>Favorite Color:</strong> {{ profile.fav_colour }}</li>
              <li><strong>Favorite Subject:</strong> {{ profile.fav_school_subject }}</li>
            </ul>

            <div class="interests mt-4">
              <h4>Values</h4>
              <div class="badges">
                <span v-if="profile.political" class="badge bg-info me-2">Political</span>
                <span v-if="profile.religious" class="badge bg-info me-2">Religious</span>
                <span v-if="profile.family_oriented" class="badge bg-info me-2">Family Oriented</span>
              </div>
            </div>

            <div class="biography mt-4">
              <h4>Biography</h4>
              <p>{{ profile.biography }}</p>
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
import { useRouter } from 'vue-router';

export default {
  name: 'MyProfile',
  setup() {
    const router = useRouter();
    const profile = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const currentUser = JSON.parse(localStorage.getItem('user') || 'null');

    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/profiles', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        profile.value = response.data.find(p => p.user_id_fk === currentUser.id);
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load profile';
        console.error('Profile loading error:', err);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchProfile();
    });

    return {
      profile,
      loading,
      error,
      currentUser
    };
  }
};
</script>

<style scoped>
.my-profile {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.profile-photo {
  width: 100%;
  max-width: 300px;
  height: auto;
  object-fit: cover;
}

.badges .badge {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
}

.profile-details h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}
</style>