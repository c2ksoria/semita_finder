<template>
  <div ref="mapRef" class="mapa" style="height: 400px;"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import api from '../services/api'
import { useComercioStore } from '../store/comercioStore'
const comercioStore = useComercioStore()
// const comercios = ref([]);
const mapRef = ref(null)
let map = null

const DEFAULT_COORDS = [31.5400017,-68.536639] // 🧭 Ejemplo: San Miguel de Tucumán
const DEFAULT_ZOOM = 14
let RADIO_METROS = 1000
const radioGuardado = localStorage.getItem('radio_busqueda')
const RADIO_KM = parseFloat(radioGuardado || import.meta.env.VITE_DEFAULT_SEARCH_RADIUS || '1.0')

// Helper para crear controles personalizados
L.Control.Custom = L.Control.extend({
  onAdd: function () {
    const div = L.DomUtil.create('div')
    div.innerHTML = this.options.content
    Object.assign(div.style, this.options.style)
    return div
  },
  onRemove: function () {},
})

L.control.custom = function (opts) {
  return new L.Control.Custom(opts)
}



onMounted(() => {
  map = L.map(mapRef.value).setView(DEFAULT_COORDS, DEFAULT_ZOOM)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map)
  
  L.control
  .custom({
    position: 'topright',
    content: `<div class="leaflet-radio-info">🔍 Radio: ${RADIO_KM} km</div>`,
    classes: '',
    style: {
      background: 'white',
      padding: '4px 8px',
      borderRadius: '6px',
      fontWeight: 'bold',
      boxShadow: '0 0 4px rgba(0,0,0,0.2)',
    },
  })
  .addTo(map)

  // Intentar geolocalización del usuario
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        map.setView([lat, lng], DEFAULT_ZOOM)
        
        L.marker([lat, lng]).addTo(map).bindPopup('Estás aquí').openPopup()
        L.circle([lat, lng], {
          radius: RADIO_KM * 1000,
          color: '#3b82f6',
          fillColor: '#93c5fd',
          fillOpacity: 0.2,
        }).addTo(map)
        api.get(`http://localhost:8000/comercio/cercanos/?lat=${lat}&lng=${lng}&radio=${RADIO_KM}`)
  .then((res) => {
    // console.log(res)
    comercioStore.setComercios(res.data)

    res.data.forEach((comercio) => {
      
      const marker = L.marker([comercio.latitud, comercio.longitud]).addTo(map)
      marker.bindPopup(`<b>${comercio.nombre}</b><br>${comercio.direccion}<b>${comercio.telefono}<b>`)
    })
  })
  .catch((err) => {
    console.error('Error al obtener comercios cercanos:', err)
  })

      },
      () => {
        console.warn('No se pudo obtener la ubicación')
      }
    )
  }
})
</script>

<style>
.mapa {
  width: 100%;
  height: 100%;
}
</style>
