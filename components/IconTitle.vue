<script setup lang="ts">
defineProps<{ icon: string }>()
</script>

<template>
  <div class="title-icon">
    <img :src="`/images/${icon}.svg`" alt="" />
    <h1><slot /></h1>
  </div>
</template>
