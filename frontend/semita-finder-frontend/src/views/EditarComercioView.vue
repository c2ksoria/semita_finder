<template>
  <div>
    <h2>Editar comercio</h2>

    <ComercioForm
      v-if="comercio"
      :modo="'editar'"
      :comercioInicial="comercio"
      :onSubmit="actualizarComercio"
    />

    <p v-else>Cargando comercio...</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ComercioForm from '../components/ComercioForm.vue'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const comercio = ref(null)

onMounted(async () => {
  try {
    const res = await api.get(`/comercio/mis-comercios/${route.params.id}/`)
    comercio.value = res.data
  } catch (err) {
    alert('No se pudo cargar el comercio')
    router.push('/configuracion')
  }
})

const actualizarComercio = async (formData) => {
  try {
    await api.patch(`/comercio/mis-comercios/${route.params.id}/`, formData)
    router.push('/configuracion')
  } catch (err) {
    console.log(err)
    alert('No se pudo actualizar el comercio')
  }
}
</script>
