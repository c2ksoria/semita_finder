<template>
  <div class="dia-horario">
    <h4>{{ nombreDia }}</h4>

    <div v-for="(franja, index) in franjasLocal" :key="index" class="franja">
      <label>
        Apertura:
        <input type="time" v-model="franja.apertura" />
      </label>
      <label>
        Cierre:
        <input type="time" v-model="franja.cierre" />
      </label>
      <button @click="eliminar(index)">🗑️</button>
    </div>

    <button
      v-if="franjasLocal.length < 2"
      @click="agregar"
    >
      ➕ Agregar franja
    </button>
  </div>
</template>

<script setup>
import { watch, ref } from 'vue'

const props = defineProps(['dia', 'nombreDia', 'franjas'])
const emit = defineEmits(['update:franjas'])

const franjasLocal = ref(props.franjas || [])

watch(franjasLocal, () => {
  emit('update:franjas', franjasLocal.value)
}, { deep: true })

const agregar = () => {
  franjasLocal.value.push({ apertura: '', cierre: '' })
}

const eliminar = (index) => {
  franjasLocal.value.splice(index, 1)
}
</script>
