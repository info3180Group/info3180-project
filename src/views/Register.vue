<template>
    <div class="register">
      <h2>Register</h2>
      <form @submit.prevent="handleRegister" enctype="multipart/form-data">
        <div>
          <label>Name:</label>
          <input v-model="name" type="text" required />
        </div>
        <div>
          <label>Username:</label>
          <input v-model="username" type="text" required />
        </div>
        <div>
          <label>Email:</label>
          <input v-model="email" type="email" required />
        </div>
        <div>
          <label>Password:</label>
          <input v-model="password" type="password" required />
        </div>
        <div>
          <label>Photo:</label>
          <input type="file" @change="handlePhotoUpload" accept="image/*" />
        </div>
        <button type="submit">Register</button>
        <p v-if="message">{{ message }}</p>
      </form>
      <div class="login-link">
        <p>Already have an account? <RouterLink to="/login">Login here</RouterLink></p>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'Register',
  setup() {
    const router = useRouter();
    const username = ref('');
    const password = ref('');
    const name = ref('');
    const email = ref('');
    const photo = ref(null);
    const message = ref('');
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

    const handlePhotoUpload = (e) => {
      photo.value = e.target.files[0];
    };

    const handleRegister = async () => {
      try {
        const formData = new FormData();
        formData.append('username', username.value);
        formData.append('password', password.value);
        formData.append('name', name.value);
        formData.append('email', email.value);
        if (photo.value) {
          formData.append('photo', photo.value);
        }

        const response = await axios.post('/api/register', formData, {
          headers: {
            'X-CSRF-Token': csrf_token.value,
            'Content-Type': 'multipart/form-data',
          },
        });

        message.value = response.data.message;
        if (response.status === 201) {
          // Redirect to login page after successful registration
          router.push('/login');
        }
      } catch (error) {
        if (error.response && error.response.data) {
          // Handle form validation errors from backend
          if (typeof error.response.data === 'object') {
            message.value = Object.values(error.response.data).join(', ');
          } else {
            message.value = error.response.data;
          }
        } else {
          message.value = 'Registration failed';
        }
        console.error("Registration error:", error);
      }
    };

    onMounted(() => {
      getCsrfToken();
    });

    return {
      username,
      password,
      name,
      email,
      message,
      handleRegister,
      handlePhotoUpload
    };
  }
};
</script>
  
<style scoped>
.register {
  max-width: 500px;
  margin: auto;
  padding: 20px;
}

.login-link {
  margin-top: 20px;
  text-align: center;
}

.login-link a {
  color: #4CAF50;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
