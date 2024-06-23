FROM jenkins/jenkins:lts-jdk17

#cambiar al usuario root
USER root

#instalar docker en el contenedor
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

# permiso de accesso Docker
RUN usermod -aG docker jenkins

# Exponer puerto jenkins y 50000 de acuerdo a la documentacion
EXPOSE 8080
EXPOSE 50000

# cambiar al usuario jenkins
USER jenkins

# Variable de entorno Jenkins home
ENV JENKINS_HOME /var/jenkins_home