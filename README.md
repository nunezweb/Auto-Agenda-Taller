# README

## Index
- [English Version](#english-version)
- [Versión en Español](#versión-en-español)

---

## English Version

### Auto Agenda Taller

**Auto Agenda Taller** is a web platform designed to facilitate the management of appointments in automotive workshops, making it easier for both clients and workshop staff to organize services, appointments, and communication. The platform aims to optimize operational efficiency and enhance the customer experience.

### General Overview

The main objective of **Auto Agenda Taller** is to simplify the way workshops handle appointments and services, providing clients with a user-friendly way to book appointments while enabling workshop staff to efficiently manage workflow. The application is structured into three main user roles: **Administrator**, **Mechanic**, and **Client**, each with its own dashboard and specific functionalities.

### Technologies Used

1. **Frontend:**
   - **React.js**: To build a dynamic and responsive user interface.
   - **Bootstrap**: Ensures responsive design and a polished look on any device.

2. **Backend:**
   - **Flask**: Python microframework managing business logic and client-server interactions.
   - **SQLAlchemy**: ORM that simplifies database interactions.
   - **Flask-Bcrypt**: Ensures secure password encryption.

3. **Database:**
   - **PostgreSQL**: Relational database used to store information related to users, appointments, vehicles, and services.

4. **Security and Authentication:**
   - **JWT (JSON Web Tokens)**: Used for secure user authentication, ensuring authorized access only.
   - **Flask-Bcrypt**: Encrypts user passwords to safeguard sensitive data.

5. **Current Integrations:**
   - **Brevo API (formerly Sendinblue)**: Sends appointment confirmations and reminders via **email** and **SMS** for effective communication with clients.

6. **Future Integrations:**
   - **Google Calendar API**: Sync appointments with users' personal calendars, enhancing scheduling.

7. **Deployment and Hosting:**
   - **Render**: Ensures continuous availability and scalability.
   - **Heroku**: Provides additional flexibility for server and resource management.

8. **Version Control:**
   - **Git/GitHub**: Manages version control and collaboration, facilitating coordinated development among team members.

---

### How Each Section Works

#### 1. Client (Client Dashboard)

Clients can:
- **Register and manage their profile**: Create an account, update personal information, and manage their vehicles.
- **Book appointments**: Choose a vehicle, service (oil change, general inspection), and book an available time slot. Appointments are confirmed automatically if available.
- **Appointment history**: Review past appointments, services rendered, and comments.
- **Comments and communication**: Leave questions or comments before or after appointments, which will be answered by the workshop.

#### 2. Mechanic (Mechanic Dashboard)

Mechanics can:
- **View and manage assigned appointments**: Access a list of scheduled appointments with details of the service and vehicle.
- **Update appointment status**: Mark appointments as "in progress" or "completed" and leave relevant comments.
- **Client communication**: Respond to client questions or comments regarding their appointments.
- **Work history**: Review a history of completed tasks and appointments.

#### 3. Administrator (Admin Dashboard)

Administrators have full control over the platform and can:
- **Manage users**: Add, remove, or modify user information (clients or mechanics), and assign roles as needed.
- **Manage appointments and services**: View, modify, or reassign appointments, and manage the services offered by the workshop (adjusting times, adding new services).
- **Set workshop parameters**: Adjust the maximum number of appointments per hour and other operational settings.
- **Reports and statistics**: Access statistics about completed appointments, services, and overall workshop performance.

---

### Summary

**Auto Agenda Taller** is a complete solution for managing appointments in automotive workshops, providing a smooth experience for both clients and workshop staff. With a user-friendly interface and a robust backend, the platform optimizes the use of time and resources, while ensuring that clients can easily book and manage their appointments. The use of modern technologies such as **React.js**, **Flask**, **PostgreSQL**, and integration with **Brevo** for notifications via **email** and **SMS**, ensures that the application is fast, secure, and scalable for future improvements. The platform is deployed using **Render** and **Heroku**, offering flexibility and optimal availability.

---

## Versión en Español

### Auto Agenda Taller

**Auto Agenda Taller** es una plataforma web diseñada para facilitar la gestión de citas en talleres automotrices, permitiendo a los clientes y al personal del taller organizar servicios, citas y comunicación de manera eficiente. La plataforma busca optimizar la eficiencia operativa y mejorar la experiencia del cliente.

### Descripción General

El objetivo principal de **Auto Agenda Taller** es simplificar la forma en que los talleres manejan las citas y los servicios, brindando a los clientes una forma fácil de reservar citas mientras el personal del taller gestiona de manera eficiente el flujo de trabajo. La aplicación está estructurada en tres roles principales: **Administrador**, **Mecánico** y **Cliente**, cada uno con su propio panel de control y funcionalidades específicas.

### Tecnologías Utilizadas

1. **Frontend:**
   - **React.js**: Para construir una interfaz de usuario dinámica y responsiva.
   - **Bootstrap**: Asegura un diseño responsivo y pulido en cualquier dispositivo.

2. **Backend:**
   - **Flask**: Microframework en Python que gestiona la lógica del servidor y las interacciones con el cliente.
   - **SQLAlchemy**: ORM que simplifica las interacciones con la base de datos.
   - **Flask-Bcrypt**: Garantiza la encriptación segura de las contraseñas.

3. **Base de Datos:**
   - **PostgreSQL**: Base de datos relacional utilizada para almacenar información relacionada con usuarios, citas, vehículos y servicios.

4. **Seguridad y Autenticación:**
   - **JWT (JSON Web Tokens)**: Implementado para la autenticación segura de usuarios, permitiendo el acceso autorizado.
   - **Flask-Bcrypt**: Encripta las contraseñas para proteger los datos sensibles.

5. **Integraciones Actuales:**
   - **Brevo API (anteriormente Sendinblue)**: Envío de confirmaciones y recordatorios de citas por **email** y **SMS** para una comunicación eficiente con los clientes.

6. **Integraciones Futuras:**
   - **Google Calendar API**: Para sincronizar automáticamente las citas con los calendarios personales de los usuarios, facilitando la gestión de horarios.

7. **Despliegue y Hosting:**
   - **Render**: Asegura una disponibilidad continua y escalabilidad automática.
   - **Heroku**: Utilizado como una opción adicional para el despliegue, proporcionando flexibilidad en la gestión de servidores y recursos.

8. **Control de Versiones:**
   - **Git/GitHub**: Herramienta utilizada para el control de versiones y la colaboración, permitiendo un trabajo coordinado entre los miembros del equipo.

---

### Cómo Funciona Cada Sección

#### 1. Cliente (Panel del Cliente)

Los **clientes** pueden:
- **Registrarse y gestionar su perfil**: Crear una cuenta, actualizar información personal y gestionar los vehículos asociados.
- **Reservar citas**: Seleccionar un vehículo, un servicio (cambio de aceite, revisión general) y reservar un horario disponible. Las citas se confirman automáticamente si hay disponibilidad.
- **Historial de citas**: Revisar citas pasadas, servicios realizados y comentarios asociados.
- **Comentarios y comunicación**: Dejar preguntas o comentarios antes o después de las citas, que serán respondidos por el taller.

#### 2. Mecánico (Panel del Mecánico)

Los **mecánicos** pueden:
- **Ver y gestionar las citas asignadas**: Acceder a una lista de citas programadas con detalles del servicio y vehículo.
- **Actualizar el estado de las citas**: Marcar citas como "en progreso" o "completadas" y dejar comentarios.
- **Comunicación con los clientes**: Responder a preguntas o comentarios de los clientes sobre sus citas.
- **Historial de trabajo**: Revisar su historial de tareas completadas y citas.

#### 3. Administrador (Panel del Administrador)

El **administrador** tiene control total sobre la plataforma y puede:
- **Gestionar usuarios**: Añadir, eliminar o modificar la información de usuarios (clientes o mecánicos) y asignar roles.
- **Gestionar citas y servicios**: Ver, modificar o reasignar citas, y gestionar los servicios ofrecidos (ajustando tiempos, agregando nuevos servicios).
- **Configurar parámetros del taller**: Ajustar el número máximo de citas por hora y otros parámetros operativos.
- **Reportes y estadísticas**: Acceso a estadísticas sobre citas realizadas, servicios completados y el rendimiento general del taller.

---

### Resumen

**Auto Agenda Taller** es una solución completa para la gestión de citas en talleres automotrices, proporcionando una experiencia fluida tanto para clientes como para el personal del taller. Con una interfaz amigable y un backend robusto, la plataforma optimiza el uso del tiempo y los recursos del taller, permitiendo a los clientes gestionar sus citas de manera fácil. El uso de tecnologías modernas como **React.js**, **Flask**, **PostgreSQL** y la integración con **Brevo** para notificaciones por **email** y **SMS** asegura que la aplicación sea rápida, segura y escalable para mejoras futuras. La plataforma está desplegada utilizando **Render** y **Heroku**, garantizando flexibilidad y disponibilidad óptima.
