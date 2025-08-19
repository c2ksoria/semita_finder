FROM node:18-alpine

# Cambiar el directorio de trabajo directamente al subdirectorio donde está package.json
WORKDIR /app

# Copiar package.json y package-lock.json desde el subdirectorio
COPY semita-finder-frontend/package*.json ./

# Instalar dependencias
RUN npm install

# Copiar todo el código del subdirectorio al contenedor
COPY semita-finder-frontend/. .

# Exponer puerto
EXPOSE 3000

# Comando por defecto
CMD ["npm", "run", "serve"]
