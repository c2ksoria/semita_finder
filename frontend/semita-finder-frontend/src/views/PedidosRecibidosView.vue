<template>
  <div class="pedidos-recibidos">
    <h2>Pedidos recibidos</h2>

    <div v-if="cargando">Cargando pedidos...</div>

    <div v-else-if="pedidos.length === 0">
      <p>No tenés pedidos recibidos aún.</p>
    </div>

    <table v-else class="tabla-pedidos">
      <thead>
        <tr>
          <th>#</th>
          <th>Usuario</th>
          <th>Fecha retiro</th>
          <th>Total</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pedido in pedidos" :key="pedido.id">
          <td>{{ pedido.id }}</td>
          <td>{{ pedido.cliente_nombre }}</td>
          <td>{{ formatoFecha(pedido.fecha_hora_retiro) }}</td>
          <td>$ {{ parseFloat(pedido.total).toFixed(2) }}</td>
          <td>{{ pedido.estado }}</td>
          <td>
            <router-link :to="`/pedidos-recibidos/${pedido.id}`">Ver detalle</router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const pedidos = ref([])
const cargando = ref(true)
const router = useRouter()

onMounted(async () => {
  try {
    const res = await api.get('/pedido/pedidos-recibidos/')
    pedidos.value = res.data
  } catch (err) {
    alert('Error al obtener pedidos')
    router.push('/login')
  } finally {
    cargando.value = false
  }
})

const formatoFecha = (fechaIso) => {
  const f = new Date(fechaIso)
  return f.toLocaleString()
}
</script>

<style scoped>
.tabla-pedidos {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.tabla-pedidos th,
.tabla-pedidos td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}
</style>
