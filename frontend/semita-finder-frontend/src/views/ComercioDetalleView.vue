<template>
  <div v-if="comercio">
    <EstadoComercio :horarios="comercio.horarios" />

    <TablaHorarios :horarios="comercio.horarios" />

    <h2>{{ comercio.nombre }}</h2>
    <p>{{ comercio.descripcion }}</p>
    <p><strong>Dirección:</strong> {{ comercio.direccion }}</p>

    <!-- Imágenes del comercio -->
    <div v-if="comercio.imagenes.length">
      <h3>Fotos del comercio</h3>
      <div class="imagenes-comercio">
        <img
          v-for="img in comercio.imagenes"
          :key="img.id"
          :src="img.imagen"
          alt="Foto del comercio"
        />
      </div>
    </div>

    <!-- Horarios -->
    <!-- <div v-if="comercio.horarios.length">
      <h3>Horarios de atención</h3>
      <ul>
        <li v-for="h in comercio.horarios" :key="`${h.dia_semana}-${h.hora_apertura}`">
          {{ diasSemana[h.dia_semana] }}: {{ h.hora_apertura }} - {{ h.hora_cierre }}
        </li>
      </ul>
    </div> -->

    <!-- Productos -->
    <div v-if="comercio.productos.length">
      <h3>Productos</h3>
      <div class="productos">
        <div v-for="prod in comercio.productos" :key="prod.id" class="producto">
          <h4>{{ prod.nombre }} - ${{ prod.precio }}</h4>
          <p>Tipo: {{ prod.tipo.nombre }}</p>
          <img
            v-if="prod.imagenes.length"
            :src="prod.imagenes[0].imagen"
            alt="Imagen del producto"
          />
        </div>
      </div>
    </div>
  </div>

  <div v-else>
    <p>Cargando comercio...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import EstadoComercio from "../components/EstadoComercio.vue";
import TablaHorarios from "../components/TablaHorarios.vue";
import api from "../services/api";

const route = useRoute();
const comercio = ref(null);
const router = useRouter();

const diasSemana = [
  "Domingo",
  "Lunes",
  "Martes",
  "Miércoles",
  "Jueves",
  "Viernes",
  "Sábado",
];

const cargarComercio = async () => {
  try {
    const res = await api.get(`/comercio/${route.params.id}/`);
    console.log(res.data);
    comercio.value = res.data;
  } catch (error) {
    alert("El comercio no existe o está inactivo");
    router.push("/");
  }
};

onMounted(cargarComercio);
</script>

<style scoped>
.imagenes-comercio img {
  width: 200px;
  margin: 5px;
  border-radius: 8px;
}
.productos {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.producto {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  width: 200px;
}
</style>
