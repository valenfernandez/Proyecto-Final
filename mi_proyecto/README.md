# Instrucciones para ejecutar mi_proyecto con venv, Django y Celery

Para poder ejecutar el proyecto con Django y Celery se require tener instalado:

Python 3 (https://www.python.org/downloads/)
RabbitMQ (https://www.rabbitmq.com/install-windows.html)
Redis (https://redis.io/docs/getting-started/installation/install-redis-on-windows/) 

Mas informacion sobre el funcionamiento de este proyecto en (https://realpython.com/asynchronous-tasks-with-django-and-celery/)

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
pip install -r requirements.txt
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
