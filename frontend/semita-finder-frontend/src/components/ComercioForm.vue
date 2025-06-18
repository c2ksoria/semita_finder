<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label>Nombre:</label>
      <input v-model="form.nombre" required />
    </div>

    <div>
      <label>Descripción:</label>
      <textarea v-model="form.descripcion"></textarea>
    </div>

    <div>
      <label>Dirección:</label>
      <input v-model="form.direccion" required />
    </div>

    <div>
      <label>Latitud:</label>
      <input v-model="form.latitud" type="number" step="any" required />
    </div>

    <div>
      <label>Longitud:</label>
      <input v-model="form.longitud" type="number" step="any" required />
    </div>

    <div>
      <label>Stock inicial de semitas:</label>
      <input v-model="form.stock_semitas" type="number" min="0" />
    </div>

    <div>
      <label>Año de inicio:</label>
      <input v-model="form.anio_inicio" type="number" min="1900" max="2100" required />
    </div>

    <div>
      <label>Mes de inicio:</label>
      <select v-model="form.mes_inicio" required>
        <option v-for="(nombre, numero) in meses" :key="numero" :value="numero">{{ nombre }}</option>
      </select>
    </div>
    <div>
      <label>Telefono:</label>
      <input v-model="form.telefono" required />
    </div>
    
    <div>
      <label>
        <input type="checkbox" v-model="form.activo" />
        ¿Comercio activo?
      </label>
    </div>

    <button type="submit">{{ modo === 'editar' ? 'Actualizar' : 'Crear' }}</button>
  </form>
</template>

<script setup>
import { reactive, watch, toRefs } from 'vue'

const props = defineProps({
  comercioInicial: Object,       // si viene, se usa para editar
  modo: { type: String, default: 'crear' }, // 'crear' o 'editar'
  onSubmit: Function,            // función que se ejecuta al enviar
})

const form = reactive({
  nombre: '',
  descripcion: '',
  direccion: '',
  latitud: '',
  longitud: '',
  stock_semitas: 0,
  anio_inicio: new Date().getFullYear(),
  mes_inicio: 1,
  activo: true,
})

const meses = {
  1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
  5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
  9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre',
}

// Rellenar si es modo edición
watch(
  () => props.comercioInicial,
  (nuevo) => {
    if (nuevo) {
      Object.assign(form, { ...nuevo })
    }
  },
  { immediate: true }
)

const handleSubmit = () => {
  props.onSubmit({ ...form })
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 600px;
  margin: 2rem auto;
}
label {
  font-weight: bold;
}
input, textarea, select {
  width: 100%;
  padding: 0.5rem;
}
button {
  padding: 0.6rem 1.2rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 5px;
}
</style>
