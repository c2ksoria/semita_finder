<template>
  <div>
    <!-- <h2>Comercios cercanos</h2> -->
    <Mapa />
<ComerciosCercanos/>

<!-- <p v-else class="sin-comercios">No hay comercios en el radio de búsqueda.</p> -->

  </div>
</template>

<script setup>
import Mapa from '../components/Mapa.vue'
import ComerciosCercanos from '../components/ComerciosCercanos.vue';
import { ref, onMounted } from 'vue'



</script>
