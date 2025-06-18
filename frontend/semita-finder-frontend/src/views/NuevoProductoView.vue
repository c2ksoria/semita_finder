<template>
  <div>
    <h2>Agregar producto al comercio</h2>
    <ProductoForm
      :modo="'crear'"
      :comercioId="comercioId"
      :onSubmit="crearProducto"
    />
  </div>
</template>

<script setup>
import ProductoForm from '../components/ProductoForm.vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const comercioId = parseInt(route.params.id)

const crearProducto = async (formData) => {
  try {
    await api.post('/producto/', formData)
    alert('Producto creado exitosamente')
    router.push('/configuracion')
  } catch (err) {
    alert('Error al crear el producto')
    console.error(err)
  }
}
</script>
