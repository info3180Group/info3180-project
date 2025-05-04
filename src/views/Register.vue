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
         
          router.push('/login');
        }
      } catch (error) {
        if (error.response && error.response.data) {
          
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
  max-width: 400px;
  margin: 60px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.register h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #333;
}

form div {
  margin-bottom: 18px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #444;
}

input[type="text"],
input[type="email"],
input[type="password"],
input[type="file"] {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #007BFF;
  outline: none;
}

button[type="submit"] {
  width: 100%;
  padding: 12px;
  background-color: #007BFF;
  border: none;
  color: white;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

.message,
.register p {
  text-align: center;
  margin-top: 10px;
  color: #d9534f; 
}

.login-link {
  margin-top: 20px;
  text-align: center;
}

.login-link a {
  color: #007BFF;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
