<template>
  <div class="matches container">
    <h2>Your Matches</h2>
    
    <div v-if="loading" class="text-center">
      <p>Finding your matches...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else-if="matches.length === 0" class="text-center">
      <p>No matches found. Try updating your profile preferences!</p>
    </div>
    
    <div v-else class="row">
      <div v-for="match in matches" :key="match.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">Match Details</h5>
            <ul class="list-unstyled">
              <li><strong>Parish:</strong> {{ match.parish }}</li>
              <li><strong>Age:</strong> {{ new Date().getFullYear() - match.birth_year }}</li>
              <li><strong>Gender:</strong> {{ match.sex }}</li>
              <li><strong>Favorite Cuisine:</strong> {{ match.fav_cuisine }}</li>
              <li><strong>Race:</strong> {{ match.race }}</li>
            </ul>
            
            <p class="card-text">{{ match.description }}</p>
            
            <div class="mt-3">
              <h6>Interests</h6>
              <div class="interests-badges">
                <span v-if="match.political" class="badge bg-info me-2">Political</span>
                <span v-if="match.religious" class="badge bg-info me-2">Religious</span>
                <span v-if="match.family_oriented" class="badge bg-info me-2">Family Oriented</span>
              </div>
            </div>
            
            <div class="mt-3">
              <button 
                @click="viewProfile(match.id)" 
                class="btn btn-primary me-2"
              >
                View Profile
              </button>
              <button 
                v-if="!isFavorited(match.user_id_fk)"
                @click="handleFavorite(match.user_id_fk)" 
                class="btn btn-outline-danger"
              >
                <i class="bi bi-heart"></i>
                Add to Favorites
              </button>
              <span v-else class="text-danger">
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
  name: 'MatchProfiles',
  setup() {
    const router = useRouter();
    const matches = ref([]);
    const loading = ref(true);
    const error = ref(null);
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
        }
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to favorite profile';
        console.error('Favorite error:', err);
      }
    };

    const getUserProfile = async () => {
      try {
        const response = await axios.get('/api/profiles', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        userProfile.value = response.data.find(profile => 
          profile.user_id_fk === currentUser.id
        );
        
        if (userProfile.value) {
          await fetchMatches();
        } else {
          error.value = 'Please create a profile first';
          loading.value = false;
        }
      } catch (err) {
        error.value = 'Failed to fetch user profile';
        loading.value = false;
        console.error('Error getting user profile:', err);
      }
    };

    const fetchMatches = async () => {
      try {
        const response = await axios.get(`/api/profiles/matches/${userProfile.value.id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        matches.value = response.data.matches;
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to fetch matches';
        console.error('Error fetching matches:', err);
      } finally {
        loading.value = false;
      }
    };

    const viewProfile = (profileId) => {
      router.push(`/profile/${profileId}`);
    };

    onMounted(async () => {
      await getCsrfToken();
      await fetchFavorites();
      getUserProfile();
    });

    return {
      matches,
      loading,
      error,
      isFavorited,
      handleFavorite,
      viewProfile
    };
  }
};
</script>

<style scoped>
.matches {
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

.interests-badges {
  margin-bottom: 1rem;
}

.badge {
  font-size: 0.8rem;
}
</style>

