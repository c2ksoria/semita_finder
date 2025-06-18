<template>
  <div v-if="pedido">
    <!-- resto del contenido -->

    <div class="pedido-detalle" v-if="pedido">
      <h2>Pedido #{{ pedido.id }}</h2>
      <p><strong>Comercio:</strong> {{ pedido.comercio_nombre }}</p>
      <p><strong>Estado:</strong> {{ pedido.estado }}</p>
      <p>
        <strong>Fecha de retiro:</strong>
        {{ formatoFecha(pedido.fecha_hora_retiro) }}
      </p>
      <p><strong>Comentario:</strong> {{ pedido.comentario || "-" }}</p>

      <h3>Productos:</h3>
      <table class="tabla-productos">
        <thead>
          <tr>
            <th>Producto</th>
            <th>Tipo</th>
            <th>Cantidad</th>
            <th>Subtotal</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in pedido.items" :key="item.id">
            <td>{{ item.producto_nombre }}</td>
            <td>{{ item.tipo_nombre }}</td>
            <td>{{ item.cantidad }}</td>
            <td>$ {{ parseFloat(item.precio_item).toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>

      <p class="total">
        <strong>Total:</strong> $ {{ parseFloat(pedido.total).toFixed(2) }}
      </p>

      <h3>Historial del Pedido</h3>
      <table
        class="tabla-movimientos"
        v-if="pedido.movimientos && pedido.movimientos.length"
      >
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Estado</th>
            <th>Comentario</th>
            <th>Usuario</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="mov in pedido.movimientos" :key="mov.id">
            <td>{{ formatoFecha(mov.fecha_moviminto) }}</td>
            <td>{{ mov.estado }}</td>
            <td>{{ mov.comentario || "-" }}</td>
            <td>{{ mov.usuario_nombre || "-" }}</td>
          </tr>
        </tbody>
        <p v-if="!puedeCambiarEstado" class="info-entregado">
          <strong>
            Este pedido ya fue entregado y no puede modificarse.
          </strong>
</p>
        <div v-if="puedeCambiarEstado">
          <h3>Cambiar estado del pedido</h3>

          <form @submit.prevent="cambiarEstado" class="estado-form">
            <label for="estado">Nuevo estado:</label>
            <select v-model="nuevoEstado">
              <option disabled value="">Seleccionar estado</option>
              <option
                v-for="estado in estadosPedido"
                :key="estado.value"
                :value="estado.value"
              >
                {{ estado.label }}
              </option>
            </select>
            <label for="comentario">Comentario (opcional):</label>
            <textarea id="comentario" v-model="comentario"></textarea>

            <button type="submit" :disabled="enviando">
              Actualizar estado
            </button>
          </form>
        </div>
      </table>

      <p v-else>No hay historial disponible.</p>
    </div>

    <div v-else>
      <p>Cargando pedido...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import { useAuthStore } from "../store/auth";

const pedido = ref(null);
const nuevoEstado = ref("");
const comentario = ref("");
const enviando = ref(false);
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const estadosPedido = ref([]);

const formatoFecha = (fechaIso) => {
  if (!fechaIso) return "";
  const fecha = new Date(fechaIso);
  return fecha.toLocaleString("es-AR", {
    dateStyle: "medium",
    timeStyle: "short",
  });
};

const cargarEstadosPedido = async () => {
  try {
    const res = await api.get("/pedido/estados/");
    estadosPedido.value = res.data;
  } catch (err) {
    console.error("Error al cargar estados de pedido", err);
  }
};

// 🧠 Nuevo: endpoint dinámico según la ruta actual
const endpoint = computed(() => {
  if (route.path.startsWith("/pedidos-recibidos/")) {
    return `/pedido/pedidos-recibidos/${route.params.id}/`;
  } else {
    return `/pedido/mis-pedidos/${route.params.id}/`;
  }
});

const esVistaVendedor = computed(() =>
  route.path.startsWith("/pedidos-recibidos/")
);

const puedeCambiarEstado = computed(() => {
  return (
    esVistaVendedor.value &&
    pedido.value?.comercio_usuario === authStore.usuario?.username &&
    pedido.value.estado !== 'entregado'
  );
});

const cargarPedido = async () => {
  try {
    const res = await api.get(endpoint.value);
    console.log("respueta ....", res.data);
    pedido.value = res.data;
  } catch (err) {
    alert("No se pudo cargar el pedido.");
    router.push("/");
  }
};

onMounted(() => {
  cargarPedido();
  cargarEstadosPedido();
});

const cambiarEstado = async () => {
  if (!nuevoEstado.value) return alert("Seleccioná un estado.");

  enviando.value = true;
  try {
    await api.post(`/pedido/${pedido.value.id}/cambiar-estado/`, {
      estado: nuevoEstado.value,
      comentario: comentario.value,
    });
    alert("Estado actualizado correctamente");
    await cargarPedido();
    nuevoEstado.value = "";
    comentario.value = "";
  } catch (err) {
    alert("Error al actualizar el estado");
  } finally {
    enviando.value = false;
  }
};
</script>

<style scoped>
.tabla-productos {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.tabla-productos th,
.tabla-productos td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}
.total {
  margin-top: 1rem;
  font-size: 1.2rem;
}
.tabla-movimientos {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
}
.tabla-movimientos th,
.tabla-movimientos td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}
.estado-form {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.estado-form select,
.estado-form textarea,
.estado-form button {
  padding: 0.5rem;
  font-size: 1rem;
}
</style>
