# -----------------------
# 1) Этап сборки (Node.js)
# -----------------------
FROM node:lts-alpine

WORKDIR /frontend

# Копируем исходный код фронтенда
COPY ./frontend /frontend/

# Устанавливаем зависимости
RUN npm install

# Запускаем сборку (dist)
RUN npm run build-only


# -------------------------
# 2) Этап финального образа
# -------------------------
FROM nginx:stable-alpine

# Удаляем стандартные настройки Nginx (опционально)
RUN rm /etc/nginx/conf.d/default.conf

# Копируем свои настройки Nginx, если нужно
# COPY ./nginx.conf /etc/nginx/conf.d

# Копируем собранные файлы во внутрь Nginx
COPY --from=build-stage /frontend/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
