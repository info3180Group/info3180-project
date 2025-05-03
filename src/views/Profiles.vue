<template>
  <div class="profiles container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Search Profiles</h2>
      <RouterLink to="/profile/edit" class="btn btn-primary">
        {{ hasProfile ? 'Edit My Profile' : 'Create Profile' }}
      </RouterLink>
    </div>
    
    <!-- Search Form -->
    <div class="search-form">
      <form @submit.prevent="searchProfiles" class="mb-4">
        <div class="row g-3">
          <div class="col-md-3">
            <input 
              type="text" 
              v-model="searchParams.name" 
              class="form-control" 
              placeholder="Search by name"
            >
          </div>
          <div class="col-md-2">
            <input 
              type="number" 
              v-model="searchParams.birth_year" 
              class="form-control" 
              placeholder="Birth year"
            >
          </div>
          <div class="col-md-2">
            <select v-model="searchParams.sex" class="form-select">
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <div class="col-md-3">
            <input 
              type="text" 
              v-model="searchParams.race" 
              class="form-control" 
              placeholder="Race"
            >
          </div>
          <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100">Search</button>
          </div>
        </div>
      </form>
    </div>

    <!-- Results Section -->
    <div class="profiles-grid">
      <div v-if="loading" class="text-center">
        <p>Loading profiles...</p>
      </div>
      
      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
      </div>
      
      <div v-else-if="profiles.length === 0" class="text-center">
        <p>No profiles found.</p>
      </div>
      
      <div v-else class="row">
        <div v-for="profile in profiles" :key="profile.profile_id" class="col-md-4 mb-4">
          <div class="card">
            <img 
              :src="profile.photo ? `/uploads/${profile.photo}` : '/default-profile.jpg'" 
              class="card-img-top profile-thumb" 
              :alt="profile.name"
            />
            <div class="card-body">
              <h5 class="card-title">{{ profile.name }}</h5>
              <p class="card-text">{{ profile.description }}</p>
              <ul class="list-unstyled">
                <li><strong>Age:</strong> {{ new Date().getFullYear() - profile.birth_year }}</li>
                <li><strong>Parish:</strong> {{ profile.parish }}</li>
                <li><strong>Gender:</strong> {{ profile.sex }}</li>
              </ul>
              <button 
                @click="viewProfile(profile.profile_id)" 
                class="btn btn-primary me-2"
              >
                View Profile
              </button>
              <button 
                v-if="canFavorite(profile)"
                @click="favoriteProfile(profile.user_id)" 
                class="btn"
                :class="[
                  isFavorited(profile.user_id) 
                    ? 'btn-danger' 
                    : 'btn-outline-danger'
                ]"
              >
                <i class="bi" :class="[
                  isFavorited(profile.user_id) 
                    ? 'bi-heart-fill' 
                    : 'bi-heart'
                ]"></i>
                {{ isFavorited(profile.user_id) ? 'Favorited' : 'Add to Favorites' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'Profiles',
  setup() {
    const router = useRouter();
    const profiles = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const searchParams = ref({
      name: '',
      birth_year: '',
      sex: '',
      race: ''
    });

    const currentUser = JSON.parse(localStorage.getItem('user') || 'null');
    const userProfile = ref(null);
    const favorites = ref([]);
    const csrf_token = ref('');

    const getCsrfToken = async () => {
      try {
        const res = await fetch("/api/v1/csrf-token");
        const data = await res.json();
        csrf_token.value = data.csrf_token;
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
      }
    };

    const checkUserProfile = async () => {
      try {
        const response = await axios.get('/api/profiles', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value
          }
        });
        
        userProfile.value = response.data.find(profile => 
          profile.user_id_fk === currentUser.id
        );
      } catch (err) {
        console.error('Error checking user profile:', err);
      }
    };

    const fetchFavorites = async () => {
      try {
        const response = await axios.get(`/api/users/${currentUser.id}/favourites`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value
          }
        });
        favorites.value = response.data.favourites || [];
      } catch (err) {
        console.error('Error fetching favorites:', err);
      }
    };

    const searchProfiles = async () => {
      loading.value = true;
      error.value = null;
      
      try {
        const params = new URLSearchParams();
        Object.entries(searchParams.value).forEach(([key, value]) => {
          if (value) params.append(key, value);
        });

        const response = await axios.get(`/api/search?${params.toString()}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value
          }
        });
        
        const profilesWithUsers = await Promise.all(
          response.data.results
            .filter(profile => profile.user_id !== currentUser.id)
            .map(async (profile) => {
              try {
                const userResponse = await axios.get(`/api/users/${profile.user_id}`, {
                  headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                  }
                });
                return {
                  ...profile,
                  photo: userResponse.data.user.photo
                };
              } catch (err) {
                console.error('Error fetching user:', err);
                return profile;
              }
            })
        );
        
        profiles.value = profilesWithUsers;
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to fetch profiles';
        console.error('Search error:', err);
      } finally {
        loading.value = false;
      }
    };

    const viewProfile = (profileId) => {
      router.push(`/profile/${profileId}`);
    };

    const favoriteProfile = async (userId) => {
      try {
        await axios.post(`/api/profiles/${userId}/favourite`, {
          user_id: currentUser.id  
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value
          }
        });
        
        await fetchFavorites();
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to favorite profile';
      }
    };

    const canFavorite = (profile) => {
      return currentUser && currentUser.id !== profile.user_id;
    };

    const isFavorited = (profileUserId) => {
      return favorites.value.some(fav => fav.id === profileUserId);
    };

    const hasProfile = computed(() => {
      return userProfile.value !== null;
    });

    onMounted(async () => {
      await getCsrfToken();
      await checkUserProfile();
      await fetchFavorites();
      await searchProfiles();
    });

    return {
      profiles,
      loading,
      error,
      searchParams,
      searchProfiles,
      viewProfile,
      favoriteProfile,
      canFavorite,
      hasProfile,
      isFavorited,
      favorites,
      csrf_token
    };
  }
};
</script>

<style scoped>
.profiles {
  padding-top: 2rem;
}

.search-form {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.profiles-grid {
  margin-top: 2rem;
}

.card {
  height: 100%;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.profile-thumb {
  height: 200px;
  object-fit: cover;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
}

.btn i {
  margin-right: 0.5rem;
}
</style>