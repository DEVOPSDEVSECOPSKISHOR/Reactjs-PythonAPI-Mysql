Tools and Configurations
API (Backend): Flask API (Lightweight Python framework)

Database: MySQL

Webserver: Nginx (for both proxying and serving static files)

Containerization: Docker

Connection Details
Database:

Internal Docker Network Port: 3306

Host Port (Optional for direct access): 3306

API (Backend):

Internal Docker Network Port: 5000

Not directly exposed to host; accessed via Nginx proxy.

Frontend (React App):

Internal Docker Network Port: 80 (served by Nginx inside the container)

Not directly exposed to host; accessed via Nginx proxy.

Nginx (Proxy):

Host Port: 80 (for HTTP traffic)

Start and build the Docker configuration:

docker compose up --build -d


React Application (Frontend):
Open your web browser and go to:

http://localhost

API Endpoints:
All API calls are routed through the Nginx proxy. You can test them using curl, Postman, Insomnia, or your browser's developer tools. Nginx routes requests for /api/ to the api container.

Hello World API Call:

http://localhost/api/hello

How to Stop the Application
To stop and remove all Docker containers, networks, and the persistent volume (which will delete your database data):

docker compose down -v