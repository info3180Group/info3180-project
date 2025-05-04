<template>
  <div class="matches container">
    <h2>Your Matches</h2>
    
    <div v-if="loading" class="text-center">
      <p>Finding your matches...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else-if="Object.keys(profileMatches).length === 0" class="text-center">
      <p>No matches found. Try updating your profile preferences!</p>
    </div>
    
    <div v-else>
     
      <div v-for="(matches, profileId) in profileMatches" :key="profileId" class="profile-matches mb-5">
        <h3 class="mb-4">Matches for Profile #{{ profileId }}</h3>
        
        <div class="row">
          <div v-for="match in matches" :key="match.id" class="col-md-4 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <div class="d-flex align-items-center mb-3">
                  <img 
                    :src="match.user?.photo ? `/uploads/${match.user.photo}` : '/default-profile.jpg'" 
                    class="profile-img me-3"
                    :alt="match.user?.name"
                  />
                  <div>
                    <h5 class="card-title mb-0">{{ match.user?.name }}</h5>
                    <small class="text-muted">@{{ match.user?.username }}</small>
                  </div>
                </div>

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
    const userProfiles = ref([]);
    const profileMatches = ref({});
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

    const getUserProfiles = async () => {
      try {
        const response = await axios.get('/api/profiles', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        userProfiles.value = response.data.filter(profile => 
          profile.user_id_fk === currentUser.id
        );
        
        if (userProfiles.value.length > 0) {
          await fetchAllMatches();
        } else {
          error.value = 'Please create a profile first';
          loading.value = false;
        }
      } catch (err) {
        error.value = 'Failed to fetch user profiles';
        loading.value = false;
        console.error('Error getting user profiles:', err);
      }
    };

    const fetchAllMatches = async () => {
      try {
        const matchPromises = userProfiles.value.map(profile => 
          axios.get(`/api/profiles/matches/${profile.id}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          })
        );
        
        const responses = await Promise.all(matchPromises);
        
       
        for (let i = 0; i < responses.length; i++) {
          const profileId = userProfiles.value[i].id;
          const matches = responses[i].data.matches;
          
          
          const matchesWithUsers = await Promise.all(
            matches
              .filter(match => match.user_id_fk !== currentUser.id) 
              .map(async (match) => {
                try {
                  const userResponse = await axios.get(`/api/users/${match.user_id_fk}`, {
                    headers: {
                      'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                  });
                  return {
                    ...match,
                    user: userResponse.data.user
                  };
                } catch (err) {
                  console.error(`Error fetching user for match ${match.id}:`, err);
                  return match;
                }
              })
          );
          
          profileMatches.value[profileId] = matchesWithUsers;
        }
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
      await getUserProfiles();
    });

    return {
      matches,
      loading,
      error,
      isFavorited,
      handleFavorite,
      viewProfile,
      profileMatches
    };
  }
};
</script>

<style scoped>
.matches {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.matches h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  font-weight: bold;
}

.card {
  box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
  border: none;
  border-radius: 12px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: scale(1.02);
}

.card-body {
  padding: 1.5rem;
}

.card-title {
  font-size: 1.2rem;
  line-height: 1.2;
}

.card-text {
  margin-top: 1rem;
  font-size: 0.95rem;
  color: #555;
}

.list-unstyled li {
  padding: 0.3rem 0;
}

.interests-badges {
  margin-top: 0.5rem;
}

.badge {
  font-size: 0.85rem;
  padding: 0.5em 0.75em;
  border-radius: 20px;
}

.btn {
  font-size: 0.9rem;
  padding: 0.45rem 1rem;
  border-radius: 6px;
}

.text-danger {
  font-weight: 500;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

.profile-matches {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 12px;
}

.profile-matches h3 {
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
}

.profile-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e9ecef;
}

.text-muted {
  font-size: 0.9rem;
}
</style>

