<template>
  <div v-if="isVendorLoaded" class="sale-form-container">
    <h2>Create Sale</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="vendor">Vendor:</label>
        <input v-model="sale.vendor" type="text" id="vendor" readonly />
      </div>
      <div class="form-group">
        <label for="client">Client:</label>
        <select v-model="sale.client" id="client" required>
          <option v-for="client in clients" :key="client.id" :value="client.id">
            {{ client.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="payment_method">Payment Method:</label>
        <select v-model="sale.payment_method" id="payment_method" required>
          <option v-for="method in paymentMethods" :key="method.value" :value="method.value">
            {{ method.label }}
          </option>
        </select>
      </div>
      <div v-for="(item, index) in saleItems" :key="index" class="sale-item">
        <h3>Sale Item {{ index + 1 }}</h3>
        <div class="form-group">
          <label for="product">Product:</label>
          <select v-model="item.product" id="product" required>
            <option v-for="product in getAvailableProducts(index)" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="quantity">Quantity:</label>
          <input v-model="item.quantity" type="number" placeholder="Enter quantity" required min="1" />
        </div>
        <button type="button" @click="removeItem(index)" class="remove-item-button">Remove Item</button>
      </div>
      <button type="button" @click="addItem" class="add-item-button">Add Item</button>
      <button type="submit" class="submit-button">Submit Sale</button>
      <p v-if="errorMessages.length" class="error">
        <span v-for="(msg, index) in errorMessages" :key="index">{{ msg }}<br /></span>
      </p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </form>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import axios from '../.././axios';
  import { useRouter } from 'vue-router';
  import Header from '../.././components/Header.vue';

  const router = useRouter();
  const sale = ref({
    client: '',
    vendor: '',
    payment_method: '',
    is_finalized: false,
    id: null
  });

  const saleItems = ref([{ product: '', quantity: null }]);
  const clients = ref([]);
  const products = ref([]);
  const paymentMethods = ref([]);
  const errorMessages = ref([]);
  const successMessage = ref('');
  const isVendorLoaded = ref(false);

  const fetchInitialData = async () => {
    try {
      const clientsResponse = await axios.get('/clients/');
      clients.value = clientsResponse.data.results;

      const productsResponse = await axios.get('/products/');
      products.value = productsResponse.data.results;

      const paymentMethodsResponse = await axios.get('/payment-methods/');
      paymentMethods.value = paymentMethodsResponse.data.payment_methods;

      const vendorResponse = await axios.get('/user/vendor/');
      sale.value.vendor = vendorResponse.data.name;
    } catch (error) {
      console.error('Error fetching initial data:', error);
      alert('Failed to load data.');
      router.push('/products');
    } finally {
      isVendorLoaded.value = true;
    }
  };

  const addItem = () => {
    saleItems.value.push({ product: '', quantity: null });
  };

  const removeItem = (index) => {
    saleItems.value.splice(index, 1);
  };

  const getAvailableProducts = (currentIndex) => {
    const selectedProductIds = saleItems.value
      .filter((item, index) => index !== currentIndex)
      .map(item => item.product);
    
    return products.value.filter(product => !selectedProductIds.includes(product.id));
  };

  const handleSubmit = async () => {
    if (saleItems.value.length === 0) {
      alert('At least one sale item is required.');
      return;
    }

    let saleId = null;

    try {
      const saleResponse = await axios.post('/sales/', sale.value);
      saleId = saleResponse.data.id;
      sale.value.id = saleId;

      const saleItemsPromises = saleItems.value.map(item =>
        axios.post('/sale-items/', { ...item, sale: saleId })
      );
      
      await Promise.all(saleItemsPromises);
      await axios.patch(`/sales/${saleId}/`, { is_finalized: true });

      successMessage.value = 'Sale created successfully!';
      errorMessages.value = [];
    } catch (error) {
      successMessage.value = '';
      errorMessages.value = [];
      if (error.response && error.response.status === 400) {
        const apiErrors = error.response.data;
        for (const [field, messages] of Object.entries(apiErrors)) {
          messages.forEach(message => errorMessages.value.push(`${field}: ${message}`));
        }
      } else {
        errorMessages.value.push('Failed to create sale.');
      }

      if (saleId) {
        try {
          await axios.delete(`/sales/${saleId}/`);
        } catch (deleteError) {
          console.error('Error deleting sale:', deleteError);
        }
      }
    }
  };

  onMounted(fetchInitialData);
</script>

<style scoped>
  .sale-form-container {
    max-width: 600px;
    margin: auto;
    padding: 2em;
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(129, 84, 84, 0.1);
  }

  h2 {
    text-align: center;
    margin-bottom: 1em;
  }

  .form-group {
    margin-bottom: 0.2em;
  }

  label {
    display: block;
    margin-bottom: 0.5em;
  }

  input,
  select {
    width: 100%;
    padding: 0.8em;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }

  button {
    margin-right: 0.2em;
    margin-top: 1em;
  }

  .remove-item-button {
    background-color: #d9534f;
  }

  .remove-item-button:hover {
    background-color: #c9302c;
  }

  .sale-item {
    padding: 1em;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f9f9f9;
    margin-bottom: 1em;
  }

  .sale-item h3 {
    margin-top: 0;
    margin-bottom: 1em;
  }

  .error {
    color: red;
    text-align: center;
    margin-top: 1em;
  }

  .success {
    color: green;
    text-align: center;
    margin-top: 1em;
    font-weight: bold
  }
</style>
