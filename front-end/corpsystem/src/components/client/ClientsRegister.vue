<template>
  <ClientForm
    title="Register New Client"
    buttonText="Register"
    :submitAction="registerClient"
  />
</template>

<script setup>
import Header from '../.././components/Header.vue';
import ClientForm from './ClientForm.vue';
import axios from '../.././axios';
import { ref } from 'vue';

const registerClient = async (formData) => {
  await axios.post('clients/', formData);
};

</script>