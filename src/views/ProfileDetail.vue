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
        
       
        const userResponse = await axios.get(`/api/users/${profile.value.user_id_fk}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        userPhoto.value = userResponse.data.user.photo;
        canFavorite.value = currentUser && currentUser.id !== profile.value.user_id_fk;
        
      
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

      
        if (response.status === 201 || response.status === 200) {
          isFavorited.value = true;
          await fetchFavorites();
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
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.profile-photo-container {
  text-align: center;
}

.profile-photo {
  max-width: 100%;
  height: auto;
  border: 3px solid #dee2e6;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.profile-content h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.profile-content .lead {
  font-size: 1.1rem;
  color: #6c757d;
  margin-bottom: 1.5rem;
}

.profile-details h4 {
  margin-top: 1.5rem;
  font-size: 1.2rem;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.4rem;
}

.profile-details ul {
  padding-left: 0;
  margin-bottom: 1rem;
}

.profile-details li {
  padding: 0.3rem 0;
}

.biography h4 {
  margin-top: 1.5rem;
  font-size: 1.2rem;
}

.biography p {
  white-space: pre-wrap;
  background-color: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.btn-outline-danger {
  font-weight: 500;
}
</style>
