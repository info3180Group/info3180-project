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

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
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
          localStorage.setItem("token", data.token);
          localStorage.setItem(
              "user",
              JSON.stringify({ name: data.user.name, username: data.user.username, email: data.user.email, id: data.user.id , photo: data.user.photo, date_joined: data.user.date_joined })
          );
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
  margin: auto;
  padding: 20px;
}

.register-link {
  margin-top: 20px;
  text-align: center;
}

.register-link a {
  color: #4CAF50;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
