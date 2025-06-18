<template>
  <div class="estado-comercio">
    <span v-if="estado === 'abierto'" class="abierto">🟢 Abierto ahora</span>
    <span v-else-if="minutosFaltantes !== null" class="espera">
      🕒 Abre en {{ minutosFaltantes }} min ({{ formatoHora(proximaHora) }})
    </span>
    <span v-else class="cerrado">🔴 Cerrado por hoy</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  horarios: {
    type: Array,
    required: true
  }
})

const ahora = new Date()
const diaActual = ((ahora.getDay() + 6) % 7)  // convierte JS -> Django
const minutosActuales = ahora.getHours() * 60 + ahora.getMinutes()

const franjasHoy = props.horarios.filter(h => h.dia === diaActual)

let estado = 'cerrado'
let minutosFaltantes = null
let proximaHora = null

for (const franja of franjasHoy) {
  const [hA, mA] = franja.apertura.split(':').map(Number)
  const [hC, mC] = franja.cierre.split(':').map(Number)
  const aperturaMin = hA * 60 + mA
  const cierreMin = hC * 60 + mC

  if (minutosActuales >= aperturaMin && minutosActuales < cierreMin) {
    estado = 'abierto'
    break
  }

  if (minutosActuales < aperturaMin) {
    minutosFaltantes = aperturaMin - minutosActuales
    proximaHora = franja.apertura
    break
  }
}

const formatoHora = (horaStr) => {
  if (!horaStr) return ''
  const [h, m] = horaStr.split(':')
  return `${h}:${m}`
}
</script>

<style scoped>
.estado-comercio {
  font-weight: bold;
  margin-top: 8px;
}
.abierto {
  color: green;
}
.cerrado {
  color: red;
}
.espera {
  color: orange;
}
</style>
