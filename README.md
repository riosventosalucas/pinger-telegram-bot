# Pinger

Este proyecto consta de dos partes: el `pinger-bot` y el `pinger-svc`.

## Pinger-bot

El `pinger-bot` es un bot de Telegram que monitorea la conectividad de las direcciones IP. Periódicamente, el bot enviará un mensaje a un chat de Telegram especificado indicando si una o más direcciones IP no responden.

### Configuración

Antes de poder usar el `pinger-bot`, debe proporcionar los siguientes parámetros de configuración en el archivo `docker-compose.yml`:

- `TOKEN`: el token de autenticación de Telegram Bot.
- `ROOM_ID`: el ID del chat de Telegram donde se enviarán los mensajes.
- `CHECK_IPS_INTERVAL`: el intervalo de tiempo en segundos para verificar la conectividad de las direcciones IP.


## Pinger-svc

El `pinger-svc` es un servicio web REST que verifica la conectividad de las direcciones IP. 

### Rutas

- `GET /api/v1/ip/check`: verifica la conectividad de una dirección IP especificada. Se debe proporcionar la dirección IP en la consulta como un parámetro `ip`.

### Uso

Para correr `pinger-svc` y `pinger-bot` ejecuta:

docker-compose up

Una vez inicializado los servicios y aplicaciones, dirigete hacia tu chatbot de telegram, deberias haber recibido un mensaje!