<template>
  <div>
    <Header v-if="!$route.meta.hideHeader"></Header>
    <router-view></router-view>
  </div>
</template>

<script setup>
  import Header from './components/Header.vue';
</script>

<style>

</style>