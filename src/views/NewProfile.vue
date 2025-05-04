<template>
  <div class="new-profile container">
    <h2>Create New Profile</h2>
    
    <form @submit.prevent="handleSubmit" class="profile-form">
      <div class="row g-3">
        <div class="col-md-12">
          <label for="description" class="form-label">Description</label>
          <input 
            type="text" 
            class="form-control" 
            id="description"
            v-model="profileData.description" 
            required
          />
        </div>

        <div class="col-md-6">
          <label for="parish" class="form-label">Parish</label>
          <select 
            class="form-select" 
            id="parish"
            v-model="profileData.parish" 
            required
          >
            <option value="">Choose...</option>
            <option value="Kingston">Kingston</option>
            <option value="St. Andrew">St. Andrew</option>
            <!-- Add other parishes -->
          </select>
        </div>

        <div class="col-md-6">
          <label for="age" class="form-label">Age</label>
          <input 
            type="number" 
            class="form-control" 
            id="age"
            v-model="age" 
            min="18"
            max="100"
            required
            @input="updateBirthYear"
          />
        </div>

        <div class="col-md-6">
          <label for="sex" class="form-label">Gender</label>
          <select 
            class="form-select" 
            id="sex"
            v-model="profileData.sex" 
            required
          >
            <option value="">Choose...</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <!-- Add other form fields following the same pattern -->
        
        <div class="col-12">
          <label for="biography" class="form-label">Biography</label>
          <textarea 
            class="form-control" 
            id="biography"
            v-model="profileData.biography" 
            rows="3"
            required
          ></textarea>
        </div>

        <div class="col-md-6">
          <label for="race" class="form-label">Race</label>
          <input 
            type="text" 
            class="form-control" 
            id="race"
            v-model="profileData.race" 
            required
          />
        </div>

        <div class="col-md-6">
          <label for="height" class="form-label">Height (cm)</label>
          <input 
            type="number" 
            class="form-control" 
            id="height"
            v-model="profileData.height" 
            required
          />
        </div>

        <div class="col-md-4">
          <label for="fav_cuisine" class="form-label">Favorite Cuisine</label>
          <input 
            type="text" 
            class="form-control" 
            id="fav_cuisine"
            v-model="profileData.fav_cuisine" 
            required
          />
        </div>

        <div class="col-md-4">
          <label for="fav_colour" class="form-label">Favorite Color</label>
          <input 
            type="text" 
            class="form-control" 
            id="fav_colour"
            v-model="profileData.fav_colour" 
            required
          />
        </div>

        <div class="col-md-4">
          <label for="fav_school_subject" class="form-label">Favorite Subject</label>
          <input 
            type="text" 
            class="form-control" 
            id="fav_school_subject"
            v-model="profileData.fav_school_subject" 
            required
          />
        </div>

        <div class="col-12">
          <div class="form-check">
            <input 
              type="checkbox" 
              class="form-check-input" 
              id="political"
              v-model="profileData.political"
            />
            <label class="form-check-label" for="political">Political</label>
          </div>
          <div class="form-check">
            <input 
              type="checkbox" 
              class="form-check-input" 
              id="religious"
              v-model="profileData.religious"
            />
            <label class="form-check-label" for="religious">Religious</label>
          </div>
          <div class="form-check">
            <input 
              type="checkbox" 
              class="form-check-input" 
              id="family_oriented"
              v-model="profileData.family_oriented"
            />
            <label class="form-check-label" for="family_oriented">Family Oriented</label>
          </div>
        </div>
      </div>

      <div class="alert alert-danger" v-if="error">{{ error }}</div>
      
      <div class="mt-4">
        <button type="submit" class="btn btn-primary me-2">Create Profile</button>
        <RouterLink to="/my-profiles" class="btn btn-secondary">Cancel</RouterLink>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'NewProfile',
  setup() {
    const router = useRouter();
    const currentUser = JSON.parse(localStorage.getItem('user') || 'null');
    const error = ref(null);
    const csrf_token = ref('');
    const age = ref(18); // Default age

    const profileData = ref({
      user_id_fk: currentUser?.id,
      description: '',
      parish: '',
      biography: '',
      sex: '',
      race: '',
      birth_year: null, // We'll calculate this from age
      height: '',
      fav_cuisine: '',
      fav_colour: '',
      fav_school_subject: '',
      political: false,
      religious: false,
      family_oriented: false
    });

    const getCsrfToken = async () => {
      try {
        const res = await fetch("/api/v1/csrf-token");
        const data = await res.json();
        csrf_token.value = data.csrf_token;
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
      }
    };

    const updateBirthYear = () => {
      const currentYear = new Date().getFullYear();
      profileData.value.birth_year = currentYear - age.value;
    };

    const handleSubmit = async () => {
      try {
        // Get CSRF token before submitting
        await getCsrfToken();
        
        const response = await axios.post('/api/profiles', profileData.value, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value,
            'Content-Type': 'application/json'
          }
        });

        if (response.status === 201) {
          router.push('/my-profiles');
        }
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to create profile';
        console.error('Profile creation error:', err);
      }
    };

    // Get CSRF token and initialize birth year when component mounts
    onMounted(() => {
      updateBirthYear();
      getCsrfToken();
    });

    return {
      profileData,
      error,
      handleSubmit,
      age,
      updateBirthYear
    };
  }
};
</script>

<style scoped>
.new-profile {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.profile-form {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-top: 1rem;
}
</style>