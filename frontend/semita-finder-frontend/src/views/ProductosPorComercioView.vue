<template>
  <div class="productos-comercio">
    <h2>Productos de "{{ nombreComercio }}"</h2>

    <p v-if="cargando">Cargando productos...</p>

    <table v-else>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Tipo</th>
          <th>Precio</th>
          <th>Stock</th>
          <th>Activo</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="producto in productos" :key="producto.id">
          <td>{{ producto.nombre }}</td>
          <td>{{ producto.tipo.nombre }}</td>
          <td>${{ producto.precio }}</td>
          <td>{{ producto.en_stock ? 'Sí' : 'No' }}</td>
          <td>{{ producto.activo ? 'Sí' : 'No' }}</td>
          <td>
            <button @click="editarProducto(producto.id)">✏️</button>
            <button @click="eliminarProducto(producto.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>

    <button class="agregar" @click="agregarProducto">+ Agregar producto</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const productos = ref([])
const nombreComercio = ref('')
const comercioId = parseInt(route.params.id)
const cargando = ref(true)

onMounted(async () => {
  try {
    const res = await api.get(`producto/comercio/${comercioId}`)
    console.log(res)
    productos.value = res.data

    // opcional: traer nombre del comercio para mostrarlo arriba
    const comercio = await api.get(`comercio/mis-comercios/${comercioId}/`)
    nombreComercio.value = comercio.data.nombre

  } catch (err) {
    alert('Error al cargar productos')
    router.push('/configuracion')
  } finally {
    cargando.value = false
  }
})

const agregarProducto = () => {
  router.push(`/mis-comercios/${comercioId}/agregar-producto`)
}

const eliminarProducto = async (id) => {
  if (!confirm('¿Seguro que querés eliminar este producto?')) return
  try {
    await api.delete(`producto/mis-productos/${id}`)
    productos.value = productos.value.filter(p => p.id !== id)
  } catch (err) {
    alert('No se pudo eliminar el producto')
  }
}
const editarProducto = (productoId) => {
  router.push(`/mis-comercios/${comercioId}/productos/${productoId}`)
}
</script>

<style scoped>
.productos-comercio {
  max-width: 900px;
  margin: auto;
  padding: 2rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  padding: 0.5rem;
  border: 1px solid #ccc;
  text-align: left;
}
.agregar {
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
}
</style>
