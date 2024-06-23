
#imagen de nginx para el front end, especificamos la version alpine
FROM nginx:alpine

#copiamos los directorios de frontend en el directorio por defecto de nginx
COPY . /usr/share/nginx/html

# ponemos en escucha el puerto 80 del contenedor
EXPOSE 80

#ejecutamos el servidor web de nginx
    # -g para especificar comando "daemon off", que pone el servidor en primer plano
CMD ["nginx", "-g", "daemon off;"]