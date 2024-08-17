<template>
    <div class="client-form-container">
      <h2>{{ title }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" v-model="form.name" id="name" maxlength="100" placeholder="Enter your first and last name" required/>
        </div>
        <div class="form-group">
          <label for="cpf">CPF:</label>
          <input type="text" v-model="form.cpf" id="cpf" maxlength="14" placeholder="example: 000.000.000-00" required/>
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" v-model="form.email" id="email" placeholder="example: xxxx@gmail.com"/>
        </div>
        <div class="form-group">
          <label for="phone">Phone:</label>
          <input type="tel" v-model="form.phone" id="phone" maxlength="13" placeholder="example: 5583900000000"/>
        </div>
        <div class="form-group">
          <label for="cep">CEP:</label>
          <input type="text" v-model="form.cep" id="cep" maxlength="9" placeholder="example: 00000-000"/>
        </div>
        <div class="form-group">
          <label for="street">Street:</label>
          <input type="text" v-model="form.street" id="street" maxlength="100" placeholder="example: xxxxxxxxxxxx,000"/>
        </div>
        <button type="submit">{{ buttonText }}</button>
        <p v-if="errorMessages.length" class="error">
          <span v-for="(msg, index) in errorMessages" :key="index">{{ msg }}<br /></span>
        </p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
      </form>
    </div>
  </template>
  
<script setup>
  import { ref, watch } from 'vue';
  
  const props = defineProps({
    initialData: Object,
    title: String,
    buttonText: String,
    submitAction: Function
  });
  
  const form = ref({ ...props.initialData });
  const errorMessages = ref([]);
  const successMessage = ref('');
  
  watch(() => props.initialData, (newData) => {
    form.value = { ...newData };
  }, { deep: true });
  
  const handleSubmit = async () => {
    try {
      await props.submitAction(form.value);
      successMessage.value = 'Successful!';
      errorMessages.value = [];
    } catch (error) {
      successMessage.value = '';
      if (error.response && error.response.status === 400) {
        errorMessages.value = [];
        const apiErrors = error.response.data;
        for (const [field, messages] of Object.entries(apiErrors)) {
          messages.forEach(message => errorMessages.value.push(`${field}: ${message}`));
        }
      } else {
        errorMessages.value = ['Failed to perform operation.'];
      }
    }
  };
</script>
  
<style scoped>
  .client-form-container {
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
  
  input {
    width: 100%;
    padding: 0.8em;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    margin-top: 1em;
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
