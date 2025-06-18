import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useComercioStore = defineStore('comercios', () => {
  const comercios = ref([])

  const setComercios = (lista) => {
    console.log(lista)
    comercios.value = lista
  }

  return {
    comercios,
    setComercios,
  }
})
