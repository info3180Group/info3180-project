<template>
  <div class="top-profiles container">
    <h2>Top 20 Most Favorited Profiles</h2>
    
    <div v-if="loading" class="text-center">
      <p>Loading top profiles...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else-if="topProfiles.length === 0" class="text-center">
      <p>No profiles found.</p>
    </div>
    
    <div v-else class="row">
      <div v-for="(profile, index) in topProfiles" :key="profile.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-header d-flex justify-content-between align-items-center">
            <span class="rank">#{{ index + 1 }}</span>
            <span class="favorites-count">
              <i class="bi bi-heart-fill text-danger"></i>
              {{ profile.favoured_count }} favorites
            </span>
          </div>
          <img 
            :src="profile.photo ? `/uploads/${profile.photo}` : '/default-profile.jpg'" 
            class="card-img-top profile-thumb" 
            :alt="profile.name"
          />
          <div class="card-body">
            <h5 class="card-title">{{ profile.name }}</h5>
            <p class="card-text text-muted">@{{ profile.username }}</p>
            
            <div class="profile-details mb-3" v-if="profile.profile">
              <ul class="list-unstyled">
                <li><strong>Parish:</strong> {{ profile.profile.parish }}</li>
                <li><strong>Age:</strong> {{ new Date().getFullYear() - profile.profile.birth_year }}</li>
                <li><strong>Interests:</strong> {{ profile.profile.fav_cuisine }}</li>
              </ul>
            </div>
            
            <div class="d-grid gap-2">
              <button 
                v-if="profile.profile"
                @click="viewProfile(profile)" 
                class="btn btn-primary me-2"
              >
                View Profile
              </button>
              <button 
                v-if="canFavorite(profile) && !isFavorited(profile.id)"
                @click="handleFavorite(profile.id)" 
                class="btn btn-outline-danger"
              >
                <i class="bi bi-heart"></i>
                Add to Favorites
              </button>
              <span v-else-if="isFavorited(profile.id)" class="text-danger text-center">
                <i class="bi bi-heart-fill"></i>
                Favorited
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'TopProfiles',
  setup() {
    const router = useRouter();
    const topProfiles = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const currentUser = JSON.parse(localStorage.getItem('user') || 'null');
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

    const fetchTopProfiles = async () => {
      try {
        const response = await axios.get('/api/users/favourites/20', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        
        const profilesWithDetails = await Promise.all(
          response.data.top_favoured_users.map(async (user) => {
            try {
            
              const profilesResponse = await axios.get('/api/profiles', {
                headers: {
                  'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
              });
              
              
              const userProfile = profilesResponse.data.find(
                profile => profile.user_id_fk === user.id
              );
              
              if (userProfile) {
                return {
                  ...user,
                  profile: userProfile
                };
              }
              return user;
            } catch (err) {
              console.error(`Error fetching profile for user ${user.id}:`, err);
              return user;
            }
          })
        );
        
       
        topProfiles.value = profilesWithDetails.filter(profile => profile.profile);
      } catch (err) {
        if (err.response?.status === 500) {
          error.value = 'Server error occurred while fetching profiles';
        } else {
          error.value = err.response?.data?.error || 'Failed to fetch top profiles';
        }
        console.error('Error fetching top profiles:', err);
      } finally {
        loading.value = false;
      }
    };

    const fetchFavorites = async () => {
      try {
        const response = await axios.get(`/api/users/${currentUser.id}/favourites`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        favorites.value = response.data.favourites || [];
      } catch (err) {
        console.error('Error fetching favorites:', err);
      }
    };

    const isFavorited = (userId) => {
      return favorites.value.some(fav => parseInt(fav.id) === parseInt(userId));
    };

    const canFavorite = (profile) => {
      return currentUser && currentUser.id !== profile.id;
    };

    const handleFavorite = async (userId) => {
      try {
        const response = await axios.post(`/api/profiles/${userId}/favourite`, {
          user_id: currentUser.id
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value,
            'Content-Type': 'application/json'
          }
        });

        if (response.status === 201 || response.status === 200) {
          await fetchFavorites();
          await fetchTopProfiles(); 
        }
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to favorite profile';
        console.error('Favorite error:', err);
      }
    };

    const viewProfile = (profile) => {
      if (profile.profile?.id) {
        router.push(`/profile/${profile.profile.id}`);
      } else {
        error.value = 'Profile not found';
        console.error('Profile not found for user:', profile);
      }
    };

    onMounted(async () => {
      await getCsrfToken();
      await fetchFavorites();
      await fetchTopProfiles();
    });

    return {
      topProfiles,
      loading,
      error,
      isFavorited,
      canFavorite,
      handleFavorite,
      viewProfile
    };
  }
};

</script>
<style scoped>
.top-profiles {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.top-profiles h2 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: scale(1.02);
}

.card-header {
  background-color: #f8f9fa;
  font-weight: 600;
  font-size: 0.95rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #dee2e6;
}

.rank {
  font-size: 1rem;
  font-weight: bold;
  color: #343a40;
}

.favorites-count {
  font-size: 0.9rem;
  color: #dc3545;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.profile-thumb {
  height: 240px;
  object-fit: cover;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.card-text {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.profile-details ul {
  margin: 0;
  padding: 0;
  font-size: 0.9rem;
}

.profile-details li {
  padding: 0.25rem 0;
}

.btn {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
}

.text-danger {
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
}
</style>