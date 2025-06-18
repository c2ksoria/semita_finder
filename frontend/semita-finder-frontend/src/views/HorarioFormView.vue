<template>
  <section class="editar-horarios">
    <h2>Editar horarios de atención</h2>

    <div v-if="cargando">Cargando horarios...</div>
    <div v-else>
      <DiaHorario
        v-for="(nombreDia, dia) in diasSemana"
        :key="dia"
        :dia="dia"
        :nombreDia="nombreDia"
        v-model:franjas="horariosPorDia[dia]"
      />
      <button @click="guardarHorarios">💾 Guardar horarios</button>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from "../services/api";
import { useAuthStore } from "../store/auth";
import DiaHorario from '../components/DiaHorario.vue'

const authStore = useAuthStore();

const route = useRoute()
const comercioId = route.params.id

const cargando = ref(true)
const horariosPorDia = ref({})  // { 0: [{apertura, cierre}], ... }

const diasSemana = {
  0: 'Lunes',
  1: 'Martes',
  2: 'Miércoles',
  3: 'Jueves',
  4: 'Viernes',
  5: 'Sábado',
  6: 'Domingo'
}

// Cargar horarios actuales
onMounted(async () => {
  try {
    const res = await api.get(`/comercio/${comercioId}/horarios/`)
    console.log(res.data)
    const agrupados = {}
    for (const franja of res.data) {
      if (!agrupados[franja.dia]) agrupados[franja.dia] = []
      agrupados[franja.dia].push({
        apertura: franja.apertura,
        cierre: franja.cierre
      })
    }
    horariosPorDia.value = agrupados
  } finally {
    cargando.value = false
  }
})

const guardarHorarios = async () => {
  const payload = []
  for (const [dia, franjas] of Object.entries(horariosPorDia.value)) {
    franjas.forEach(({ apertura, cierre }) => {
      payload.push({ dia: Number(dia), apertura, cierre })
    })
  }

  try {
    await api.post(`/comercio/${comercioId}/horarios/`, payload)
    alert('Horarios guardados correctamente')
  } catch (err) {
    console.error(err)
    alert('Error al guardar horarios')
  }
}
</script>
