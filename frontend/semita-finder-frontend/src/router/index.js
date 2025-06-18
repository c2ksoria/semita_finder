import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import ConfiguracionView from '../views/ConfiguracionView.vue'
import NosotrosView from '../views/NosotrosView.vue'
import NuevoComercioView from '../views/NuevoComercioView.vue'
import EditarComercioView from '../views/EditarComercioView.vue'
import NuevoPedidoView from '../views/NuevoPedidoView.vue'
import NuevoProductoView from '../views/NuevoProductoView.vue'
import ProductosPorComercioView from '../views/ProductosPorComercioView.vue'
import EditarProductoView from '../views/EditarProductoView.vue'
import MisPedidosView from '../views/MisPedidosView.vue'
import PedidoDetalleView from '../views/PedidoDetalleView.vue'
import PedidosRecibidosView from '../views/PedidosRecibidosView.vue'
import ComercioDetalleView from '../views/ComercioDetalleView.vue'
import HorarioFormView from '../views/HorarioFormView.vue'


const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/configuracion', component: ConfiguracionView },
  { path: '/nosotros', component: NosotrosView },
  { path: '/pedido/nuevo/:id', component: NuevoPedidoView },
  { path: '/mis-pedidos', component: MisPedidosView },
  { path: '/mis-pedidos/:id', component: PedidoDetalleView },
  { path: '/pedidos-recibidos', component: PedidosRecibidosView},
  { path: '/pedidos-recibidos/:id', component: PedidoDetalleView},
  { path: '/mis-comercios/:id/agregar-producto', component: NuevoProductoView},
  { path: '/mis-comercios/nuevo', component: NuevoComercioView},
  { path: '/mis-comercios/:id',  component: EditarComercioView},
  { path: '/mis-comercios/:id/productos', component: ProductosPorComercioView },
  { path: '/mis-comercios/:comercioId/productos/:productoId', component: EditarProductoView },
  { path: '/comercio/:id', component: ComercioDetalleView },
  { path: '/mis-comercios/:id/horarios', component: HorarioFormView }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
