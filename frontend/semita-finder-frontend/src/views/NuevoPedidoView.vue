<template>
  <div class="pedido-nuevo">
    <h2>Nuevo pedido</h2>

    <p v-if="!productos.length">Cargando productos...</p>

    <form v-else @submit.prevent="confirmarPedido">
      <table>
        <thead>
          <tr>
            <th>Producto</th>
            <th>Precio</th>
            <th>Cantidad</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="producto in productos" :key="producto.id">
            <td>{{ producto.nombre }}</td>
            <td>${{ producto.precio }}</td>
            <td>
              <input
                type="number"
                min="0"
                v-model.number="cantidades[producto.id]"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <p class="total">Total: ${{ calcularTotal() }}</p>
      <div class="form-extra">
  <label for="fechaRetiro">Fecha y hora de retiro:</label>
  <input
    type="datetime-local"
    id="fechaRetiro"
    v-model="fechaRetiro"
    required
  />

  <label for="comentario">Comentario:</label>
  <textarea
    id="comentario"
    v-model="comentario"
    rows="3"
    placeholder="Opcional">
  </textarea>
</div>
      <button type="submit">Confirmar pedido</button>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const comercioId = route.params.id
const productos = ref([])
const cantidades = ref({})
const fechaRetiro = ref('')
const comentario = ref('')

onMounted(async () => {
  try {
    console.log("capibayaaa..")
    const res = await api.get(`/producto/comercio/${comercioId}/`)
    productos.value = res.data

    // Inicializar cantidades
    productos.value.forEach(p => {
      cantidades.value[p.id] = 0
    })
  } catch (err) {
    alert('No se pudieron cargar los productos')
    router.push('/')
  }
})

const calcularTotal = () => {
  return productos.value.reduce((total, p) => {
    const cantidad = cantidades.value[p.id] || 0
    return total + cantidad * parseFloat(p.precio)
  }, 0).toFixed(2)
}

// const confirmarPedido = async () => {
//   const items = productos.value
//     .filter(p => cantidades.value[p.id] > 0)
//     .map(p => ({
//       producto: p.id,
//       cantidad: cantidades.value[p.id],
//     }))

//   if (!items.length) {
//     alert('Debés seleccionar al menos un producto')
//     return
//   }

//   try {
//     console.log("pedidos..... : comercio: ",  items)
//     await api.post('/pedido/', {
//       comercio: parseInt(comercioId),
//       items: items,
//     })
//     alert('Pedido realizado con éxito')
//     router.push('/mis-pedidos')
//   } catch (err) {
//     alert('Error al realizar el pedido')
//     console.error(err)
//   }
// }

const confirmarPedido = async () => {
  const items = productos.value
    .filter(p => cantidades.value[p.id] > 0)
    .map(p => ({
      producto: p.id,
      cantidad: cantidades.value[p.id]
    }))

  if (items.length === 0) {
    alert('Seleccioná al menos un producto')
    return
  }

  if (!fechaRetiro.value) {
    alert('Debés indicar la fecha y hora de retiro')
    return
  }

  try {
    await api.post('/pedido/', {
      comercio: comercioId,
      fecha_hora_retiro: new Date(fechaRetiro.value).toISOString(),
      comentario: comentario.value,
      items: items
    })
    alert('Pedido creado con éxito')
    router.push('/mis-pedidos')
  } catch (err) {
    alert('Error al crear el pedido')
    console.error(err)
  }
}

</script>

<style scoped>
.pedido-nuevo {
  max-width: 700px;
  margin: 2rem auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 0.8rem;
  border: 1px solid #ddd;
}
.total {
  font-weight: bold;
  text-align: right;
  margin-top: 1rem;
}
button {
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 5px;
}
.form-extra {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
