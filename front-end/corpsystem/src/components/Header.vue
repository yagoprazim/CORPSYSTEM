<template>
  <div class="page-content">
    <header class="header">
      <div class="nav-buttons">
        <button @click="goTo('/products')" class="navigation-button">Products</button>
        <button @click="goTo('/clients')" class="navigation-button">Clients List</button>
        <button @click="goTo('/clients/register')" class="navigation-button">Register Client</button>
        <button :class="{'disabled': !isVendor}" :disabled="!isVendor" @click="goTo('/sale/create')" class="navigation-button">Create Sale</button>
        <button :class="{'disabled': !isVendor}" :disabled="!isVendor" @click="goTo('/sales/list')" class="navigation-button">Your Sales</button>
        <button @click="goTo('/reports')" class="navigation-button">Sales Reports</button>
        <button @click="logout" class="logout-button">Logout</button>
      </div>
      <div v-if="message" class="message">{{ message }}</div>
    </header>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import axios from '.././axios';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const message = ref('');
  const isVendor = ref(false);

  const checkVendorStatus = async () => {
    try {
      const response = await axios.get('user/vendor/');
      if (response.status === 200) {
        message.value = `Welcome, ${response.data.name}. Credential Code: ${response.data.credential_code}`;
        isVendor.value = true;
      }
    } catch (err) {
      if (err.response && err.response.status === 404) {
        message.value = 'You are not registered as a seller. Some sales functions will be blocked!';
      } else {
        message.value = 'Failed to load vendor information';
      }
    }
  };

  const goTo = (path) => {
    router.push(path);
  };

  const logout = async () => {
    try {
      await axios.delete('logout/');
      localStorage.removeItem('token');
      router.push('/login');
    } catch (err) {
      message.value = 'Failed to log out';
    }
  }

  onMounted(checkVendorStatus);
</script>

<style scoped>
  .page-content {
    padding-top: 6em;
  }
  .header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1em 2em;
    background: linear-gradient(135deg, #3a3a3a, #000000);
    color: white;
    box-shadow: rgba(0, 0, 0, 0.24) 0px 10px 15px;
    z-index: 1000;
    height: 4em;
    overflow: hidden;
  }

  .nav-buttons {
    display: flex;
    gap: 1em;
  }

  .message {
    flex-grow: 1;
    text-align: center;
    font-size: 1em;
  }

  .logout-button{
    background-color: rgb(124, 2, 2);
  }
</style>
