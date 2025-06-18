<template>
  <nav class="navbar">
    <div class="logo">
      <RouterLink to="/">Semita Finder</RouterLink>
    </div>

    <ul class="nav-links">
      <li><RouterLink to="/nosotros">Nosotros</RouterLink></li>
      <li><RouterLink to="/mis-pedidos">Pedidos</RouterLink></li>

      <li><RouterLink to="/configuracion">Configuración</RouterLink></li>
      <li v-if="!isAuthenticated">
        <RouterLink to="/login">Login</RouterLink>
      </li>
      <li v-else>
        <button @click="logout">Cerrar sesión ({{ username }})</button>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Token y nombre desde localStorage (más adelante podemos usar Pinia)
const isAuthenticated = computed(() => !!localStorage.getItem('token'))
// console.log(isAuthenticated)
const username = localStorage.getItem('username') || 'Usuario'

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  router.push('/login')
  window.location.reload()  // ⚠️ fuerza recarga y refresca estado
}
</script>

<style scoped>
.navbar {
  background-color: #f3f3f3;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo a {
  font-weight: bold;
  font-size: 1.2rem;
  color: #333;
  text-decoration: none;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 1rem;
}

.nav-links a,
.nav-links button {
  text-decoration: none;
  color: #333;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
}
</style>
