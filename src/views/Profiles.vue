<template>
  <div class="profiles container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Search Profiles</h2>

    </div>
    

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
.profiles.container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}


.profiles h2 {
  font-size: 28px;
  color: #0d6efd;
  margin-bottom: 0;
}

/* Search Form */
.search-form .form-control,
.search-form .form-select {
  border-radius: 8px;
  font-size: 14px;
  padding: 10px;
  transition: border-color 0.3s ease;
}

.search-form .form-control:focus,
.search-form .form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 5px rgba(13, 110, 253, 0.25);
  outline: none;
}

.search-form button {
  padding: 10px;
  font-weight: 600;
  border-radius: 8px;
}

/* Profile Grid */
.profiles-grid .card {
  border-radius: 12px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease-in-out;
}

.profiles-grid .card:hover {
  transform: translateY(-5px);
}

.profile-thumb {
  height: 220px;
  object-fit: cover;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}


.card-body {
  padding: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
}

.card-text {
  font-size: 14px;
  color: #555;
  margin-bottom: 12px;
}

.list-unstyled li {
  font-size: 13px;
  margin-bottom: 5px;
}

.btn-primary,
.btn-outline-danger,
.btn-danger {
  font-size: 14px;
  border-radius: 6px;
}

.btn-outline-danger {
  border: 1px solid #dc3545;
  color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
}

.profiles .btn-primary {
  font-size: 16px;
  padding: 10px 20px;
  border-radius: 8px;
}


@media (max-width: 768px) {
  .profiles.container {
    padding: 10px;
  }

  .search-form .row > div {
    width: 100%;
  }

  .btn {
    margin-bottom: 10px;
    width: 100%;
  }
}
</style>
