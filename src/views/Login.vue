<template>
    <div class="login">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div>
          <label>Username:</label>
          <input v-model="username" type="text" required />
        </div>
        <div>
          <label>Password:</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit">Login</button>
        <p v-if="message">{{ message }}</p>
      </form>
      <div class="register-link">
        <p>Don't have an account? <RouterLink to="/register">Register here</RouterLink></p>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from '@/store/auth';

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const username = ref('');
    const password = ref('');
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

    const handleLogin = async () => {
      try {
        const response = await axios.post('/api/auth/login', {
          username: username.value,
          password: password.value,
        }, {
          headers: {
            'X-CSRF-Token': csrf_token.value,
          },
        });
        const data = response.data;
        
        if(response.status === 200) {
          authStore.setToken(data.token);
          authStore.setUser({
            name: data.user.name,
            username: data.user.username,
            email: data.user.email,
            id: data.user.id,
            photo: data.user.photo,
            date_joined: data.user.date_joined
          });
          router.push({ name: "home" });
        }
        message.value = response.data.message;
      } catch (error) {
        message.value = error.response?.data?.error || 'Login failed';
        console.error("Login error:", error);
      }
    };

    onMounted(() => {
      getCsrfToken();
    });

    return {
      username,
      password,
      message,
      handleLogin
    };
  }
};
</script>
  
<style scoped>
.login {
  max-width: 400px;
  margin: 60px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login h2 {
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
  font-weight: 600;
  color: #444;
}

input[type="text"],
input[type="password"] {
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

p {
  text-align: center;
  margin-top: 10px;
  color: #d9534f; /* red for error messages */
}

.register-link {
  margin-top: 20px;
  text-align: center;
}

.register-link a {
  color: #007BFF;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>

