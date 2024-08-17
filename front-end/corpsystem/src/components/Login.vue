<template>
  <div class="login-page">
    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="align-lb">
          <label for="username">Username:</label>
          <input type="text" v-model="username" id="username" placeholder="Enter your username" required/>
        </div>
        <div class="align-lb">
          <label for="password">Password:</label>
          <input type="password" v-model="password" id="password" placeholder="Enter your password" required/>
        </div>
        <button type="submit">Login</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>
  
<script setup>
  import { ref } from 'vue';
  import axios from '.././axios'

  const username = ref('');
  const password = ref('');
  const errorMessage = ref('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('login/', {
        username: username.value,
        password: password.value
      });

      const token = response.data.access;
      localStorage.setItem('token', token);

      window.location.href = '/products';
    } catch (error) {
      errorMessage.value = 'Invalid username or password';
    }
  };
</script>
  
  <style scoped>
    .login-container {
      background-color: rgb(255, 255, 255);
      padding: 2em;
      border: 6px solid #ccc;
      border-radius: 5px;
      box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
      text-align: center;
    }

    .login-page {
      display: flex;
      justify-content: center;
      place-items: center;
      min-height: 90vh;
    }
    
    .align-lb{
      text-align: left;
    }

    input {
      width: 100%;
      padding: 0.5em;
      margin-bottom: 1em;
      border: 1px solid #ccc;
      border-radius: 4px;
    }

    .error {
      color: red;
    }
  </style>