<template>
  <div class="clients-container">
    <h2>Clients</h2>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search by name or cpf"
      class="search-input"
    />
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="filteredClients.length" class="clients-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>CPF</th>
          <th>Email</th>
          <th>Phone</th>
          <th>CEP</th>
          <th>Street</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="client in filteredClients" :key="client.id">
          <td>{{ client.name }}</td>
          <td>{{ client.cpf }}</td>
          <td>{{ client.email }}</td>
          <td>{{ client.phone }}</td>
          <td>{{ client.cep }}</td>
          <td>{{ client.street }}</td>
          <td>
            <button @click="editClient(client.id)" id="edit">Edit</button>
            <button @click="deleteClient(client.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && !filteredClients.length">No clients available</p>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import axios from '../.././axios';
  import { useRouter } from 'vue-router';
  import Header from '../.././components/Header.vue';

  const router = useRouter();

  const clients = ref([]);
  const loading = ref(true);
  const error = ref('');
  const searchQuery = ref('');

  const fetchClients = async () => {
    try {
      const response = await axios.get('clients');
      clients.value = response.data.results;
    } catch (err) {
      error.value = 'Failed to load clients';
    } finally {
      loading.value = false;
    }
  };

  const filteredClients = computed(() => {
    if (!searchQuery.value) {
      return clients.value;
    }
    return clients.value.filter(client => 
      client.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      client.cpf.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  });

  const editClient = (id) => {
    router.push(`/clients/${id}/edit`);
  };

  const deleteClient = async (id) => {
    if (confirm('Are you sure you want to delete this client?')) {
      try {
        await axios.delete(`clients/${id}/`);
        fetchClients();
      } catch (err) {
        error.value = 'Failed to delete client';
      }
    }
  };

  onMounted(fetchClients);
</script>

<style scoped>
#edit {
  margin: 0.2em;
}

.search-input {
  width: 100%;
  padding: 0.8em;
  margin-bottom: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.clients-container {
  max-width: 90%;
  margin: auto;
  padding: 1em;
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
}

h2 {
  text-align: center;
  margin-bottom: 1em;
}

.clients-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
}

.clients-table th,
.clients-table td {
  padding: 0.8em;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.clients-table th {
  background: linear-gradient(135deg, #dfdfdf, #c0c0c0);
  font-weight: bold;
}

.clients-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.clients-table tr:hover {
  background-color: #eaeaea;
}

.error {
  color: red;
  text-align: center;
  margin-top: 1em;
}
</style>
