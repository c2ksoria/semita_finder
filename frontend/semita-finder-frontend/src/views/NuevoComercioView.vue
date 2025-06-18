<template>
  <div>
    <h2>Crear nuevo comercio</h2>
    <ComercioForm :modo="'crear'" :onSubmit="crearComercio" />
  </div>
</template>

<script setup>
import ComercioForm from '../components/ComercioForm.vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const crearComercio = async (formData) => {
  try {
    await api.post('/comercio/mis-comercios/', formData)
    router.push('/configuracion') // o /mis-comercios si lo separás
  } catch (error) {
    alert('Error al crear el comercio')
    console.error(error)
  }
}
</script>
