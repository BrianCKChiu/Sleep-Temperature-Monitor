import socket

from server.database import initialize_db
from server.process import handle_request


def start_server():
    HOST = socket.gethostname()
    PORT = "8088"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set ip address to socket
    server.bind((HOST, PORT))

    server.listen(0)
    print(f"Listening on: {HOST}:{PORT}")

    # accept connections
    client_socket, client_address = server.accept()
    print(f"{client_address[0]}:{client_address[1]} -- Connected!")

    while True:
        request: str = client_socket.recv(1024)
        request: str = request.decode("utf-8")

        if request.lower() == "close":
            client_socket.send("closed".encode("utf-8"))
            break

        # process data sent
        handle_request(client_socket, request)
        response = "received".encode("utf-8")  # convert string to bytes
        # convert and send accept response to the client
        client_socket.send(response)

    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    server.close()


if __name__ == "__main__":
    initialize_db()
    start_server()
