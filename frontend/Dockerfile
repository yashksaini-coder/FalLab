FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Build-time API URL (for static builds like Next.js/Vite)
ARG API_URL=http://localhost:8000/api/v1
ENV API_URL=${API_URL}

RUN npm run build

EXPOSE 3000

ENV NODE_ENV=production
ENV PORT=3000

CMD ["npm", "start"]
