<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>

    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Usuario</label>
        <input id="username" v-model="username" type="text" required />
      </div>

      <div class="form-group">
        <label for="password">Contraseña</label>
        <input id="password" v-model="password" type="password" required />
      </div>

      <button type="submit">Ingresar</button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref(null)

const login = async () => {
  error.value = null
  try {
    const response = await api.post('/auth/login/', {
      username: username.value,
      password: password.value,
    })

    localStorage.setItem('token', response.data.token)

    // Obtener nombre del usuario
    const me = await api.get('/auth/me/')
    localStorage.setItem('username', me.data.username)

    router.push('/')
  } catch (err) {
    error.value = 'Credenciales inválidas o error de conexión'
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.2rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.4rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error {
  margin-top: 1rem;
  color: red;
}
</style>
