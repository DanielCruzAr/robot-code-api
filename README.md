# ARTICLES API
Prueba técnica de RocketCode 
  
## Descargar y ejecutar el proyecto

1. Clona el repositorio:
	```bash
	git clone https://github.com/DanielCruzAr/rocket-code-api.git
	cd rocket-code-api
	```

2. Crea un archivo `.env` nuevo con las siguientes variables de entorno:
    - DATABASE_URL=postgresql://user:password@db:5432/articles_db
    - REDIS_HOST=redis
    - REDIS_PORT=6379
    - REDIS_DB=0
    - API_KEY=supersecretapikey123
    - API_KEY_NAME=x-api-key

3. Ejecuta el siguiente comando para levantar los servicios con Docker:
	```bash
	docker compose up -d
	```
    **Nota:** No es necesario hacer docker build porque subí la imagen a un repositorio público en dockerhub pero para hacerlo solo hay que descomentar la línea 26 y comentar la 25 en el archivo de `docker-compose.yml`.

Una vez completados los pasos entra a http://localhost:8000/docs# para visualizar los endpoints disponibles.

## Para ejecutar las pruebas unitarias y de integración

1. Crea un nuevo entorno de Python e instala las dependencias:
	```bash
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements-dev.txt
	```

2. Levanta la base de datos de pruebas con Docker:
	```bash
	docker compose -f docker-compose.test.yml up -d
	```

3. Ejecuta las pruebas con pytest desde tu terminal:
	```bash
	pytest
	```
