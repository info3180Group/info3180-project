<template>
  <div class="edit-profile container">
    <h2>{{ isNewProfile ? 'Create Profile' : 'Edit Profile' }}</h2>
    
    <form @submit.prevent="handleSubmit" class="profile-form">
      <div class="row g-3">
        <div class="col-md-6">
          <div class="mb-3">
            <label class="form-label">Description</label>
            <textarea 
              v-model="profileData.description" 
              class="form-control" 
              required
            ></textarea>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Parish</label>
            <select v-model="profileData.parish" class="form-select" required>
              <option value="">Select Parish</option>
              <option value="Kingston">Kingston</option>
              <option value="St. Andrew">St. Andrew</option>
              <option value="St. Catherine">St. Catherine</option>
              <!-- Add other parishes -->
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Biography</label>
            <textarea 
              v-model="profileData.biography" 
              class="form-control" 
              rows="4"
              required
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Gender</label>
            <select v-model="profileData.sex" class="form-select" required>
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        <div class="col-md-6">
          <div class="mb-3">
            <label class="form-label">Race</label>
            <input 
              type="text" 
              v-model="profileData.race" 
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Birth Year</label>
            <input 
              type="number" 
              v-model="profileData.birth_year" 
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Height (cm)</label>
            <input 
              type="number" 
              v-model="profileData.height" 
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Favorite Cuisine</label>
            <input 
              type="text" 
              v-model="profileData.fav_cuisine" 
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Favorite Color</label>
            <input 
              type="text" 
              v-model="profileData.fav_colour" 
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Favorite School Subject</label>
            <input 
              type="text" 
              v-model="profileData.fav_school_subject" 
              class="form-control"
              required
            />
          </div>
        </div>

        <div class="col-12">
          <div class="mb-3">
            <label class="form-label">Values</label>
            <div class="form-check">
              <input 
                type="checkbox" 
                v-model="profileData.political" 
                class="form-check-input" 
                id="political"
              />
              <label class="form-check-label" for="political">Political</label>
            </div>
            <div class="form-check">
              <input 
                type="checkbox" 
                v-model="profileData.religious" 
                class="form-check-input" 
                id="religious"
              />
              <label class="form-check-label" for="religious">Religious</label>
            </div>
            <div class="form-check">
              <input 
                type="checkbox" 
                v-model="profileData.family_oriented" 
                class="form-check-input" 
                id="family"
              />
              <label class="form-check-label" for="family">Family Oriented</label>
            </div>
          </div>
        </div>
      </div>

      <div class="alert alert-danger" v-if="error">{{ error }}</div>
      
      <button type="submit" class="btn btn-primary">
        {{ isNewProfile ? 'Create Profile' : 'Save Changes' }}
      </button>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'EditProfile',
  setup() {
    const router = useRouter();
    const currentUser = JSON.parse(localStorage.getItem('user') || 'null');
    const error = ref(null);
    const isNewProfile = ref(true);
    const csrf_token = ref('');
    
    const profileData = ref({
      description: '',
      parish: '',  // Add parish field
      biography: '',
      sex: '',
      race: '',
      birth_year: null,
      height: null,
      fav_cuisine: '',
      fav_colour: '',
      fav_school_subject: '',
      political: false,
      religious: false,
      family_oriented: false,
      user_id_fk: null
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

    const checkExistingProfile = async () => {
      try {
        const response = await axios.get('/api/profiles', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value
          }
        });
        
        const userProfile = response.data.find(profile => 
          profile.user_id_fk === currentUser.id
        );
        
        if (userProfile) {
          isNewProfile.value = false;
          profileData.value = {
            id: userProfile.id,
            description: userProfile.description || '',
            parish: userProfile.parish || '',  // Add parish field
            biography: userProfile.biography || '',
            sex: userProfile.sex || '',
            race: userProfile.race || '',
            birth_year: parseInt(userProfile.birth_year) || null,
            height: parseFloat(userProfile.height) || null,
            fav_cuisine: userProfile.fav_cuisine || '',
            fav_colour: userProfile.fav_colour || '',
            fav_school_subject: userProfile.fav_school_subject || '',
            political: Boolean(userProfile.political),
            religious: Boolean(userProfile.religious),
            family_oriented: Boolean(userProfile.family_oriented),
            user_id_fk: userProfile.user_id_fk
          };
        }
      } catch (err) {
        console.error('Error checking profile:', err);
        error.value = 'Failed to load profile data';
      }
    };

    const handleSubmit = async () => {
      try {
        const payload = {
          description: profileData.value.description,
          parish: profileData.value.parish,  // Add parish field
          biography: profileData.value.biography,
          sex: profileData.value.sex,
          race: profileData.value.race,
          birth_year: parseInt(profileData.value.birth_year),
          height: parseFloat(profileData.value.height),
          fav_cuisine: profileData.value.fav_cuisine,
          fav_colour: profileData.value.fav_colour,
          fav_school_subject: profileData.value.fav_school_subject,
          political: profileData.value.political ? 1 : 0,
          religious: profileData.value.religious ? 1 : 0,
          family_oriented: profileData.value.family_oriented ? 1 : 0,
          user_id_fk: currentUser.id
        };

        if (!isNewProfile.value) {
          payload.id = profileData.value.id;
        }

        const config = {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRF-Token': csrf_token.value,
            'Content-Type': 'application/json'
          }
        };

        if (isNewProfile.value) {
          await axios.post('/api/profiles', payload, config);
        } else {
          await axios.put(`/api/profiles/${profileData.value.id}`, payload, config);
        }

        router.push('/profiles');
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to save profile';
        console.error('Profile save error:', err);
      }
    };

    onMounted(async () => {
      await getCsrfToken();
      await checkExistingProfile();
    });

    return {
      profileData,
      error,
      isNewProfile,
      handleSubmit
    };
  }
};
</script>

<style scoped>
.edit-profile.container {
  max-width: 1000px;
  margin: 50px auto;
  padding: 40px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.edit-profile h2 {
  font-size: 28px;
  margin-bottom: 30px;
  color: #0d6efd;
  text-align: center;
}

.profile-form .form-label {
  font-weight: 600;
  color: #333;
}

.profile-form textarea,
.profile-form input,
.profile-form select {
  font-size: 15px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  transition: border-color 0.3s ease;
}

.profile-form textarea:focus,
.profile-form input:focus,
.profile-form select:focus {
  outline: none;
  border-color: #0d6efd;
  box-shadow: 0 0 4px rgba(13, 110, 253, 0.3);
}

.profile-form .form-check-label {
  font-weight: 500;
  margin-left: 8px;
}

.profile-form .form-check {
  margin-bottom: 10px;
}

.alert-danger {
  margin-top: 15px;
  font-size: 15px;
}

.btn-primary {
  margin-top: 20px;
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0b5ed7;
}

@media (max-width: 768px) {
  .edit-profile.container {
    padding: 20px;
  }

  .profile-form .col-md-6 {
    width: 100%;
  }

  .btn-primary {
    font-size: 15px;
  }
}
</style>
