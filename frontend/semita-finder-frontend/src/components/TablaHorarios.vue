<template>
  <table class="tabla-horarios">
    <thead>
      <tr>
        <th>Día</th>
        <th>Horarios</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(nombre, dia) in diasSemana" :key="dia">
        <td>{{ nombre }}</td>
        <td>
          <span v-if="franjasAgrupadas[dia]?.length">
            {{ mostrarHorarios(dia) }}
          </span>
          <span v-else>—</span>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  horarios: {
    type: Array,
    required: true
  }
})

const diasSemana = {
  0: 'Lunes',
  1: 'Martes',
  2: 'Miércoles',
  3: 'Jueves',
  4: 'Viernes',
  5: 'Sábado',
  6: 'Domingo'
}

// Agrupar franjas por día
const franjasAgrupadas = computed(() => {
  const agrupado = {}
  for (const franja of props.horarios) {
    if (!agrupado[franja.dia]) agrupado[franja.dia] = []
    agrupado[franja.dia].push(franja)
  }
  return agrupado
})

// Formato: 08:00 - 12:00 / 17:00 - 20:00
const mostrarHorarios = (dia) => {
  return franjasAgrupadas.value[dia]
    .map(f => `${f.apertura} - ${f.cierre}`)
    .join(' / ')
}
</script>

<style scoped>
.tabla-horarios {
  border-collapse: collapse;
  width: 100%;
  margin-top: 1rem;
}
.tabla-horarios th,
.tabla-horarios td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}
.tabla-horarios th {
  background-color: #f5f5f5;
}
</style>
