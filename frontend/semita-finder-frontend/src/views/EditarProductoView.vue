<template>
  <div>
    <h2>Editar producto</h2>

    <ProductoForm
      v-if="producto"
      :modo="'editar'"
      :productoInicial="producto"
      :comercioId="comercioId"
      :onSubmit="actualizarProducto"
    />

    <p v-else>Cargando producto...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'
import ProductoForm from '../components/ProductoForm.vue'

const route = useRoute()
const router = useRouter()

const comercioId = parseInt(route.params.comercioId)
const productoId = parseInt(route.params.productoId)

const producto = ref(null)

onMounted(async () => {
  try {
    const res = await api.get(`/producto/mis-productos/${productoId}`)
    producto.value = res.data
  } catch (err) {
    alert('Error al cargar el producto')
    router.push('/configuracion')
  }
})

const actualizarProducto = async (formData) => {
  try {
    await api.patch(`/producto/mis-productos/${productoId}`, formData)
    alert('Producto actualizado con éxito')
    router.push(`/mis-comercios/${comercioId}/productos`)
  } catch (err) {
    alert('No se pudo actualizar el producto')
    console.error(err)
  }
}
</script>
