
# Development stage
FROM node:20-alpine as development

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install --legacy-peer-deps

# Copier les sources
COPY . .

# Exposer le port
EXPOSE 3000

# Commande par défaut pour le développement
CMD ["npm", "run", "dev"]

# Build stage
FROM node:20-alpine as build

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install --legacy-peer-deps

# Copier les sources
COPY . .

# Build
RUN npm run build

# Production stage
FROM nginx:alpine

# Copier la configuration nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copier les fichiers buildés depuis l'étape de build
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
