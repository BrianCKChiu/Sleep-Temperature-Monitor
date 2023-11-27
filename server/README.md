# Server Pi

The server creates a web server that recieves sensor data from client pis and stores it in a database.

Runs on PORT 5000

## Endpoints

- `GET /health` - Returns 200 if the server is running
- `POST /api/update` - Recieves sensor data from client pis and stores it in a database

```
Parameters:
    - client_id: The id of the PI
    - temperature: The temperature in celsius
```
