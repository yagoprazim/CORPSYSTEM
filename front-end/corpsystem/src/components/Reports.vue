<template>
    <div class="reports-container">
      <h2>Download Sales Reports</h2>
      <div class="filters-container">
        <label>
          Client:
          <select v-model="selectedClient">
            <option value="">All Clients</option>
            <option v-for="client in clients" :key="client.id" :value="client.id">
              {{ client.name }}
            </option>
          </select>
        </label>
        <label>
          Vendor:
          <select v-model="selectedVendor">
            <option value="">All Vendors</option>
            <option v-for="vendor in vendors" :key="vendor.id" :value="vendor.id">
              {{ vendor.name }}
            </option>
          </select>
        </label>
        <label>
          Date:
          <input type="date" v-model="selectedDate" />
        </label>
      </div>
      <div class="buttons-container">
        <button @click="downloadReport('csv')">Download CSV Report</button>
        <button @click="downloadReport('pdf')">Download PDF Report</button>
      </div>
      <div v-if="loading" class="loading">Processing...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from '.././axios';
  import Header from '.././components/Header.vue';
  
  const loading = ref(false);
  const error = ref('');
  const clients = ref([]);
  const vendors = ref([]);
  const selectedClient = ref('');
  const selectedVendor = ref('');
  const selectedDate = ref('');
  
  const fetchInitialData = async () => {
    try {
      const [clientsResponse, vendorsResponse] = await Promise.all([
        axios.get('/clients/'),
        axios.get('/vendors/')
      ]);
      clients.value = clientsResponse.data.results;
      vendors.value = vendorsResponse.data.results;
    } catch (err) {
      error.value = 'Failed to load initial data.';
      console.error(err);
    }
  };
  
  const downloadReport = async (format) => {
    loading.value = true;
    error.value = '';
  
    try {
      const url = `/export_sales/${format}/?client=${selectedClient.value}&vendor=${selectedVendor.value}&date=${selectedDate.value}`;
      const response = await axios({
        url: url,
        method: 'GET',
        responseType: 'blob',
      });
  
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(new Blob([response.data]));
      link.download = `sales_report.${format}`;
      link.click();
      window.URL.revokeObjectURL(link.href);
    } catch (err) {
      error.value = 'Download failed. Please try again.';
      console.error("Download failed:", err);
    } finally {
      loading.value = false;
    }
  };
  
  onMounted(fetchInitialData);
  </script>
  
  <style scoped>
  .reports-container {
    max-width: 600px;
    margin: auto;
    padding: 1em;
    background-color: #f9f9f9;
    border-radius: 8px;
    text-align: center;
  }
  
  .filters-container {
    display: flex;
    justify-content: space-around;
    margin-bottom: 1em;
    align-items: center;
  }
  
  .filters-container label {
    display: flex;
    flex-direction: column;
    margin: 0 1em;
  }
  
  select,
  input[type="date"] {
    padding: 0.5em;
    margin-top: 0.5em;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .buttons-container {
    display: flex;
    justify-content: space-around;
    margin-bottom: 1em;
  }
  
  .loading {
    margin-top: 1em;
    color: #3498db;
  }
  
  .error {
    margin-top: 1em;
    color: red;
  }
  </style>
  