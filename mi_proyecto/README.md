# Instrucciones para ejecutar mi_proyecto con venv, Django y Celery

Para poder ejecutar el proyecto con Django y Celery se require tener instalado:

Python 3 (https://www.python.org/downloads/)
RabbitMQ (https://www.rabbitmq.com/install-windows.html)
Redis (https://redis.io/docs/getting-started/installation/install-redis-on-windows/) 

Para verificar que estos 3 se instalaron y se están ejecutando correctamente, se tienen que realizar las siguientes pruebas.

Para Python cualquiera de estos 2 comandos tiene que devolver la versión de Python (si la segunda opción es la única que funciona, usar "python3" en lugar de "python" para todos los comandos subsequentes):

```
python --version
python3 --version 
```

El resultado de este comando debe ser algo parecido a:

```
Python 3.10.12
```

Para RabbitMQ en Ubuntu/Mac:

```
rabbitmqctl version
```

El resultado de este comando debe ser algo parecido a:

```
RabbitMQ version: 3.8.4
```

Para RabbitMQ en Windows, debe haber un archivo instalado en "C:\Program Files\RabbitMQ\rabbitmq_server-x.x.x\sbin\" llamado "rabbitmqctl.bat". Abrir CMD o Powershell en esta carpeta y ejecutar:

```
rabbitmq-service.bat status
```

RabbitMQ debe devolver el estado del nodo actual, lo que indica que se instaló correctamente.

Para Redis, se debe ejecutar:

```
redis-cli ping
```

La respuesta debe ser

```
PONG
```

Mas informacion sobre el funcionamiento de este proyecto junto con Celery en (https://realpython.com/asynchronous-tasks-with-django-and-celery/)

- Abrir el CMD/Powershell/Terminal sobre mi_proyecto

- Crear nuevo venv con

```
python -m venv venv
```

- Activar el venv (en Ubuntu) con
```
source venv/bin/activate
```
Y en windows con
```
venv\Scripts\activate
```

- Instalar librerias del archivo requirements.txt
```
pip install -r requirements.txt
```

Realizar migraciones y activar servidor
```
python manage.py migrate
```

- Iniciar servidor con
```
python manage.py runserver
```

- Abrir una nueva terminal.

- Iniciar otro venv. En Ubuntu con:
```
source venv/bin/activate
```
Y en windows con
```
venv\Scripts\activate
```

- Iniciar celery (IMPORTANTE: Si es en Windows, agregar --pool=solo al final del comando)
```
celery -A mi_proyecto worker -l info  
```

Los logs de celery deben mostrar estos resultados:

- ** ---------- .> transport:   amqp://guest:**@localhost:5672// <--- esto significa que rabbit se esta usando para la comunicacion de los mensajes
- ** ---------- .> results:     redis://localhost:6379/ <-- esto muestra que redis se esta usando para guardar los mensajes
