<template>
  <div class="edit-client-container">
    <ClientForm
      :initialData="client"
      title="Edit Client"
      buttonText="Save"
      :submitAction="updateClient"
    />
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import Header from '../.././components/Header.vue';
import ClientForm from './ClientForm.vue';
import axios from '../.././axios';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const client = ref(null);
const loading = ref(true);
const error = ref('');

const fetchClient = async () => {
  const id = route.params.id;
  try {
    const response = await axios.get(`clients/${id}/`);
    client.value = response.data;
  } catch (err) {
    error.value = 'Failed to load client data';
  } finally {
    loading.value = false;
  }
};

const updateClient = async (formData) => {
  const id = route.params.id;
  await axios.put(`clients/${id}/`, formData);
};

onMounted(fetchClient);
</script>
