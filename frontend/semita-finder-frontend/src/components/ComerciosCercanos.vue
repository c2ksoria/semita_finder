<template>
  <div class="comercios-lista">
    <h3>Comercios en el radio de búsqueda</h3>

    <ul v-if="comercios.length">
      <li
        v-for="comercio in comercios"
        :key="comercio.id"
        @click="seleccionar(comercio)"
        class="comercio-item"
      >
        <div class="info">
          <button  @click="irADetalleComercio(comercio.id)">
             <strong>{{ comercio.nombre }}</strong><br />
          </button>
          <br>
          <span>{{ comercio.direccion }}</span>
        </div>

        <EstadoComercio v-if="comercio.horarios" :horarios="comercio.horarios" />
        <button @click.stop="comprar(comercio)">Comprar</button>
      </li>
    </ul>

    <p v-else>No se encontraron comercios cercanos.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth' // si usás Pinia
import { useComercioStore } from '../store/comercioStore'
import EstadoComercio from './EstadoComercio.vue'

const comercioStore = useComercioStore()
const router = useRouter()
const auth = useAuthStore()

const comercios = computed(() => comercioStore.comercios)

const seleccionar = (comercio) => {
  comercioStore.comercioSeleccionado = comercio // opcional si querés guardar
  // Emitir evento, llamar función o usar store para que el mapa lo enfoque
  // Eso depende de cómo lo quieras conectar con Mapa.vue
}

const comprar = (comercio) => {
  console.log("comprar.....")
   if (!auth.token) {
    alert('Necesitás iniciar sesión para realizar un pedido')
    router.push('/login')
    return
  }

  router.push(`/pedido/nuevo/${comercio.id}`)
}

const estaAbierto = (comercio) => {
  // Por ahora simple, reemplazable si el backend devuelve estado
  return comercio.abierto ?? true
}

const irADetalleComercio = (id) => {
  router.push(`/comercio/${id}`)
}
</script>

<style scoped>
.comercios-lista {
  margin-top: 2rem;
}

.comercio-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
}

.estado {
  font-weight: bold;
  color: red;
}

.estado.abierto {
  color: green;
}

button {
  padding: 0.4rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
}

.info {
  flex: 1;
}
</style>
