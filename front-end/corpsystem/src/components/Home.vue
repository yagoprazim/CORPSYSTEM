<template>
    <div class="page-content">
      <h1>CORPSYSTEM</h1>
      <p>Connect in:</p>
      <router-link to="/login">
            <button class="login-button">Login</button>
        </router-link>
    </div>  
  </template>
  
  <script setup>
  </script>
  
  <style scoped>
  .page-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 90vh;
    margin: 0;
    text-align: center;
  }
  
  h1 {
    margin: 0;
    font-size: 3em;
  }
  
  p {
    font-size: 1.5em;
    margin: 0.5em 0;
    color: white;
  }

  .login-button {
  margin-top: 1em;
  padding: 0.5em 2em;
  font-size: 1.2em;
  color: #ffffff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #0056b3;
}

  </style>
  