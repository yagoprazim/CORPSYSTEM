<template>
  <div class="sales-container">
    <h2>Sales</h2>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search by client name or date"
      class="search-input"
    />
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="filteredSales.length" class="sales-table">
      <thead>
        <tr>
          <th>Vendor</th>
          <th>Client</th>
          <th>Payment Method</th>
          <th>Date</th>
          <th>Total Amount</th>
          <th>Finalized</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sale in filteredSales" :key="sale.id">
          <td>{{ sale.vendor_info.name }}</td>
          <td>{{ sale.client_info.name }}</td>
          <td>{{ sale.payment_method }}</td>
          <td>{{ sale.date }}</td>
          <td>{{ `R$ ${sale.total_amount}` }}</td>
          <td>{{ sale.is_finalized ? 'Yes' : 'No' }}</td>
          <td>
            <button @click="openModal(sale.id)" class="btn btn-primary">Details</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && !filteredSales.length">No sales available</p>

    <div v-if="modalVisible" class="modal fade show">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Sale Items</h5>
          </div>
          <div class="modal-body">
            <div v-if="saleItems.length">
              <ul>
                <li v-for="item in saleItems" :key="item.id">
                  {{ item.product_info.name }} - {{ `R$ ${item.total_price}` }} (Quantity: {{ item.quantity }})
                </li>
              </ul>
            </div>
            <div v-else>No items found</div>
          </div>
          <div class="modal-footer">
            <button type="button" class="close" @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="modalVisible" class="modal-backdrop fade"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from '../.././axios';
import Header from '../.././components/Header.vue';

const sales = ref([]);
const saleItems = ref([]);
const loading = ref(true);
const error = ref('');
const searchQuery = ref('');
const vendorId = ref(null);
const modalVisible = ref(false);
const currentSaleId = ref(null);

const fetchVendorId = async () => {
  try {
    const response = await axios.get('/user/vendor/');
    vendorId.value = response.data.id;
    fetchSales();
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = 'You need to be logged in to access this resource.';
    } else {
      error.value = 'Failed to load vendor information';
    }
    loading.value = false;
  }
};

const fetchSales = async () => {
  if (!vendorId.value) {
    console.error('Vendor ID is not set.');
    return;
  }

  try {
    const response = await axios.get(`/sales/?filter="vendor":${vendorId.value}`);
    sales.value = response.data.results;
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = 'You need to be logged in to access this resource.';
    } else {
      error.value = 'Failed to load sales';
    }
  } finally {
    loading.value = false;
  }
};

const fetchSaleItems = async (saleId) => {
  try {
    console.log(`Fetching sale items for saleId: ${saleId}`);
    const response = await axios.get(`/sale-items/?filter="sale":${saleId}`);
    console.log('Sale items response:', response.data);
    saleItems.value = response.data.results; 
  } catch (err) {
    console.error('Failed to load sale items', err);
  }
};

const openModal = (saleId) => {
  currentSaleId.value = saleId;
  fetchSaleItems(saleId);
  modalVisible.value = true;
};

const closeModal = () => {
  modalVisible.value = false;
  saleItems.value = []; 
};

const filteredSales = computed(() => {
  if (!searchQuery.value) {
    return sales.value;
  }
  return sales.value.filter(sale =>
    sale.client_info.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    sale.date.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

onMounted(fetchVendorId);
</script>

<style scoped>
.search-input {
  width: 100%;
  padding: 0.8em;
  margin-bottom: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.sales-container {
  max-width: 80%;
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

.sales-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
}

.sales-table th,
.sales-table td {
  padding: 0.8em;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.sales-table th {
  background: linear-gradient(135deg, #dfdfdf, #c0c0c0);
  font-weight: bold;
}

.sales-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.sales-table tr:hover {
  background-color: #eaeaea;
}

.error {
  color: red;
  text-align: center;
  margin-top: 1em;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040; 
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  border-radius: 0.3rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  z-index: 1050; 
  max-width: 500px;
  width: 100%;
  display: none; 
}

.modal.show {
  display: block;
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #e9ecef;
  text-align: right;
}

.modal-title {
  margin: 0;
}

.close {
  background-color: rgb(124, 2, 2);
}

.modal-body {
  padding: 1rem;
}
</style>
