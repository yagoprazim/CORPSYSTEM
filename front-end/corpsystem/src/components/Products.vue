<template>
    <div class="products-container">
      <h2>Products</h2>
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search by name or group"
        class="search-input"
      />
      <div v-if="loading">Loading...</div>
      <div v-if="error" class="error">{{ error }}</div>
      <table v-if="filteredProducts.length" class="products-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Group</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td>{{ product.name }}</td>
            <td>{{ product.description || 'No description available' }}</td>
            <td>{{ product.price }}</td>
            <td>{{ product.stock }}</td>
            <td>{{ product.group_info.name }}</td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && !filteredProducts.length">No products available</p>
    </div>
  </template>
  
<script setup>
  import { ref, onMounted, computed } from 'vue';
  import axios from '.././axios';
  import Header from '.././components/Header.vue';
  
  const products = ref([]);
  const loading = ref(true);
  const error = ref('');
  const searchQuery = ref('');
  
  const fetchProducts = async () => {
    try {
      const response = await axios.get('products');
      products.value = response.data.results;
    } catch (err) {
      error.value = 'Failed to load products';
    } finally {
      loading.value = false;
    }
  };
  
  const filteredProducts = computed(() => {
    if (!searchQuery.value) {
      return products.value;
    }
    return products.value.filter(product => 
      product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      product.group_info.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  });
  
  onMounted(fetchProducts);
</script>
  
  <style scoped>
    .search-input {
      width: 100%;
      padding: 0.8em;
      margin-bottom: 1em;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  
    .products-container {
      max-width: 800px;
      margin: auto;
      padding: 1em;
      background-color: #f9f9f9;
      border-radius: 8px;
    }
    
    h2 {
      text-align: center;
      margin-bottom: 1em;
    }
    
    .products-table {
      width: 100%;
      border-collapse: collapse;
      background-color: #ffffff;
      border-radius: 8px;
      overflow: hidden;
    }
    
    .products-table th,
    .products-table td {
      padding: 0.8em;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    
    .products-table th {
      background: linear-gradient(135deg, #dfdfdf, #c0c0c0);
      font-weight: bold;
    }
    
    .products-table tr:nth-child(even) {
      background-color: #f9f9f9;
    }
    
    .products-table tr:hover {
      background-color: #eaeaea;
    }
    
    .error {
      color: red;
      text-align: center;
      margin-top: 1em;
    }
  </style>
  