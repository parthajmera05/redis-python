import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    connection, _ = server_socket.accept()

    while True:
        buffer: bytes = connection.recv(1024)
        data: str = buffer.decode()
        print("Received message from client", data)
        connection.send("+PONG\r\n".encode())
        print("Sent to client: pong")


if __name__ == "__main__":
    main()
