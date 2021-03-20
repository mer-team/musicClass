## musicClass
Python microservice responsible for the music emotion classification

### Docker Params
| Arg | Default | Description |
| --- | --- | --- |
| API_URL | localhost:8000 | API backend URL (without http://)
| HOST | localhost | RabbitMQ host |
| USER | guest | HTTP basic auth username  |
| PASS | guest | HTTP basic auth password |
| PORT | 5672 | RabbitMQ Port |
| MNG_PORT | 15672 | RabbitMQ Management Port |
| TIME | 10 | Timeout to check if the service is up |

### RabbitMQ Queues
* Read from `classifyMusic`
    * Payload: json(features result)

### Run Local Microservice
Run Rabbit
```
docker run -d -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest -p 15672:15672 -p 5672:5672 rabbitmq:3-management-alpine
```

Build local `musicClass` image from source
```
docker build -t musicclasslocal:latest .
```

Run local `musicClass` image
```
docker run -it --rm -e TIME=10 -e PORT=5672 -e PASS=guest -e USER=guest -e HOST=localhost -e MNG_PORT=15672 --net=host musicclasslocal:latest
```

Run official `musicClass` image
```
docker run -e TIME=10 -e USER=merUser -e PASS=passwordMER -e HOST=localhost -e MNG_PORT=15672 --net=host merteam/musicclass:latest
```

### Tests
```
pytest
```
The tests are provided in the file `test_rabbit.py`. Currently checking the rabbitMQ connection and sending jobs to the queue.