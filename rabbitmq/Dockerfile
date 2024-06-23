# imagen RabbitMQ con Erlang para administrar
FROM rabbitmq:3-management

#variables de entorno para redundancia de prueba con pipeline jenkinsfile
ENV RABBITMQ_DEFAULT_USER=cicdG3
ENV RABBITMQ_DEFAULT_PASS=password

# Exponer los puertos
EXPOSE 5672 15672

# Ejecutar al iniciar el contenedor
CMD ["rabbitmq-server"]