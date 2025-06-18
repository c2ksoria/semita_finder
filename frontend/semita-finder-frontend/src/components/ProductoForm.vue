<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label>Nombre:</label>
      <input v-model="form.nombre" required />
    </div>

    <div>
      <label>Tipo de semita:</label>
      <select v-model="form.tipo_id" required>
        <option v-for="tipo in tipos" :key="tipo.id" :value="tipo.id">{{ tipo.nombre }}</option>
      </select>
    </div>

    <div>
      <label>Precio:</label>
      <input type="number" v-model.number="form.precio" step="0.01" required />
    </div>

    <div>
      <label>¿En stock?</label>
      <input type="checkbox" v-model="form.en_stock" />
    </div>

    <div>
      <label>¿Activo?</label>
      <input type="checkbox" v-model="form.activo" />
    </div>

    <button type="submit">{{ modo === 'editar' ? 'Actualizar' : 'Crear' }}</button>
  </form>
</template>

<script setup>
import { reactive, ref, onMounted, watch } from 'vue'
import api from '../services/api'

const props = defineProps({
  modo: { type: String, default: 'crear' },
  productoInicial: Object,
  comercioId: Number,
  onSubmit: Function,
})

const tipos = ref([])

const form = reactive({
  nombre: '',
  tipo_id: null,
  precio: 0,
  en_stock: true,
  activo: true,
})

onMounted(async () => {
  const res = await api.get('/producto/tiposemita/')
  tipos.value = res.data
})

watch(
  () => props.productoInicial,
  (nuevo) => {
    if (nuevo) {
      Object.assign(form, {
        nombre: nuevo.nombre,
        tipo_id: nuevo.tipo?.id,
        precio: nuevo.precio,
        en_stock: nuevo.en_stock,
        activo: nuevo.activo,
      })
    }
  },
  { immediate: true }
)

const handleSubmit = () => {
  props.onSubmit({
    ...form,
    comercio: props.comercioId
  })
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 600px;
  margin: auto;
}
input, select {
  padding: 0.5rem;
}
button {
  padding: 0.6rem 1.2rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 5px;
}
</style>
