<template>
  <div class="configuracion">
    <h2>Configuración</h2>

    <section class="usuario-info" v-if="usuario">
      <h3>Mi perfil</h3>
      <p><strong>Usuario:</strong> {{ usuario.username }}</p>
      <p><strong>Email:</strong> {{ usuario.email || "No disponible" }}</p>
    </section>

    <section class="config-radio">
      <h3>Radio de búsqueda (km)</h3>
      <input type="number" step="0.1" min="0.1" v-model="radio" />
      <button @click="guardarRadio">Guardar</button>
      <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
    </section>
    <section v-if="!cargando" class="mis-comercios">
  <h3>Mis comercios</h3>
  <ul v-if="misComercios.length">
    <li v-for="comercio in misComercios" :key="comercio.id">
      <button @click="editarComercio(comercio.id)">✏️</button>  
      <button @click="eliminarComercio(comercio.id)">🗑️</button>
      <button @click="verProductos(comercio.id)">📦</button>
      <button @click="editarHorarios(comercio.id)">🕒</button>
      <strong> - {{ comercio.nombre }}</strong> - {{ comercio.direccion }}
    </li>
  </ul>
  <p v-else>No tenés comercios creados.</p>
</section>

    <p v-else>Cargando comercios...</p>

    <button @click="irACrear">+ Crear comercio</button>
  </div>
  <router-link to="/pedidos-recibidos">📦 Pedidos recibidos</router-link>
</template>

<script setup>
import { onMounted, ref } from "vue";
import api from "../services/api";
import { useRouter } from 'vue-router'

const router = useRouter()

const usuario = ref(null);
const radio = ref("1.0"); // valor por defecto
const mensaje = ref("");
const cargando = ref(true)
const misComercios = ref([])


onMounted(async () => {
  try {
    const res = await api.get("/auth/me/");
    usuario.value = res.data;
  } catch (err) {
    console.error("Error al cargar usuario");
  }

 try {
    const res = await api.get('/comercio/mis-comercios/')
    misComercios.value = res.data
  } catch (err) {
    console.error('Error al cargar comercios del usuario')
  } finally {
    cargando.value = false
  }
  const almacenado = localStorage.getItem("radio_busqueda");
  if (almacenado) {
    radio.value = almacenado;
  }
});

const guardarRadio = () => {
  localStorage.setItem("radio_busqueda", radio.value);
  mensaje.value = `Radio guardado: ${radio.value} km`;
  setTimeout(() => (mensaje.value = ""), 2000);
};

const eliminarComercio = async (id) => {
  if (!confirm("¿Seguro que querés eliminar este comercio?")) return;
  try {
    await api.delete(`/comercio/mis-comercios/${id}/`);
    misComercios.value = misComercios.value.filter((c) => c.id !== id);
  } catch (err) {
    console.log(err)
    alert(err);
  }
};

const irACrear = () => {
  console.log("yendo a un nuevo comercio...")
  router.push("/mis-comercios/nuevo");
};
const editarComercio = (id) => {
  router.push(`/mis-comercios/${id}`)
}
const verProductos = (comercioId) => {
  router.push(`/mis-comercios/${comercioId}/productos`)
}
const editarHorarios = (comercioId) => {
  router.push(`/mis-comercios/${comercioId}/horarios`)
}
</script>

<style scoped>
.config-radio {
  margin-top: 2rem;
}

input {
  width: 100px;
  padding: 0.4rem;
  margin-right: 1rem;
}

button {
  padding: 0.4rem 1rem;
}

.mensaje {
  margin-top: 0.5rem;
  color: green;
  font-weight: bold;
}
</style>
