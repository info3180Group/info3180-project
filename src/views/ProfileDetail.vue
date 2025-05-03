<template>
  <div class="profile-detail container">
    <div v-if="loading" class="text-center">
      <p>Loading profile...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else class="profile-content">
      <div class="row">
        <div class="col-md-4">
          <div class="profile-photo-container mb-3">
            <img 
              :src="userPhoto ? `/uploads/${userPhoto}` : '/default-profile.jpg'" 
              :alt="profile?.name"
              class="profile-photo img-fluid rounded"
            />
          </div>
        </div>
        
        <div class="col-md-8">
          <h2>{{ profile.name }}</h2>
          <p class="lead">{{ profile.description }}</p>
          
          <div class="profile-details">
            <h4>Personal Information</h4>
            <ul class="list-unstyled">
              <li><strong>Age:</strong> {{ new Date().getFullYear() - profile.birth_year }}</li>
              <li><strong>Parish:</strong> {{ profile.parish }}</li>
              <li><strong>Gender:</strong> {{ profile.sex }}</li>
              <li><strong>Race:</strong> {{ profile.race }}</li>
              <li><strong>Height:</strong> {{ profile.height }}</li>
            </ul>

            <h4>Preferences</h4>
            <ul class="list-unstyled">
              <li><strong>Favorite Cuisine:</strong> {{ profile.fav_cuisine }}</li>
              <li><strong>Favorite Color:</strong> {{ profile.fav_colour }}</li>
              <li><strong>Favorite Subject:</strong> {{ profile.fav_school_subject }}</li>
            </ul>

            <h4>Values</h4>
            <ul class="list-unstyled">
              <li><strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</li>
              <li><strong>Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}</li>
              <li><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</li>
            </ul>

            <div class="biography mt-4">
              <h4>Biography</h4>
              <p>{{ profile.biography }}</p>
            </div>
          </div>

          <button 
            v-if="canFavorite && !isFavorited"
            @click="handleFavorite" 
            class="btn btn-outline-danger mt-3"
          >
            <i class="bi bi-heart"></i>
            Add to Favorites
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'ProfileDetail',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const profile = ref(null);
    const userPhoto = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const canFavorite = ref(false);
    const isFavorited = ref(false);
    const favorites = ref([]);
    const csrf_token = ref('');

    const currentUser = JSON.parse(localStorage.getItem('user') || 'null');

    const fetchFavorites = async () => {
      try {
        const response = await axios.get(`/api/users/${currentUser.id}/favourites`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        favorites.value = response.data.favourites || [];
        // Update favorite status if profile is loaded, comparing user IDs
        if (profile.value) {
          isFavorited.value = favorites.value.some(fav => 
            parseInt(fav.id) === parseInt(profile.value.user_id_fk)
          );
        }
      } catch (err) {
        console.error('Error fetching favorites:', err);
      }
    };

    const fetchProfile = async () => {
      try {
        const profileId = route.params.id;
        const response = await axios.get(`/api/profile/${profileId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        profile.value = response.data;
        
        // Fetch user details to get the photo
        const userResponse = await axios.get(`/api/users/${profile.value.user_id_fk}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        userPhoto.value = userResponse.data.user.photo;
        canFavorite.value = currentUser && currentUser.id !== profile.value.user_id_fk;
        
        // Check favorite status after profile is loaded
        if (canFavorite.value) {
          await fetchFavorites();
        }
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load profile';
        console.error('Profile loading error:', err);
      } finally {
        loading.value = false;
      }
    };

    const getCsrfToken = async () => {
      try {
        const res = await fetch("/api/v1/csrf-token");
        const data = await res.json();
        csrf_token.value = data.csrf_token;
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
      }
    };

    const handleFavorite = async () => {
      try {
        const response = await axios.post(`/api/profiles/${profile.value.user_id_fk}/favourite`, {
          user_id: currentUser.id  
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value,
            'Content-Type': 'application/json'
          }
        });

        // Check response and update UI
        if (response.status === 201 || response.status === 200) {
          isFavorited.value = true;
          await fetchFavorites(); // Refresh favorites list
        }
      } catch (err) {
        if (err.response?.status === 400) {
          error.value = err.response.data.error;
        } else {
          error.value = 'Failed to favorite profile';
        }
        console.error('Favorite error:', err);
      }
    };

    onMounted(async () => {
      await getCsrfToken();
      await fetchProfile();
    });

    return {
      profile,
      userPhoto,
      loading,
      error,
      canFavorite,
      isFavorited,
      favorites,
      handleFavorite,
      csrf_token
    };
  }
};
</script>

<style scoped>
.profile-detail {
  padding-top: 2rem;
}

.profile-photo {
  width: 100%;
  max-width: 300px;
  height: auto;
  object-fit: cover;
}

.profile-photo-container {
  text-align: center;
}

.profile-details {
  margin-top: 2rem;
}

.profile-details h4 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.profile-details ul li {
  margin-bottom: 0.5rem;
}
</style>