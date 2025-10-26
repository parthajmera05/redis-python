import socket  # noqa: F401
import threading

BUFFER_SIZE = 4096
def handle_command(client : socket.socket):
    with client:
        while True:
        
            
            data = client.recv(BUFFER_SIZE)

            if not data: 
                break
            print(f"Received data: {data}")
            if data.startswith(b"*1\r\n$4\r\nPING\r\n"):
                client.sendall(b"+PONG\r\n")
            if data.startswith(b"*2\r\n$4\r\nECHO\r\n"):
                msg = data.split(b"\r\n")[-2]
                client.sendall(b"$" + str(len(msg)).encode() + b"\r\n" + msg + b"\r\n")
            

            

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)


    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_command, args=(client_socket,)).start()



if __name__ == "__main__":
    main()
