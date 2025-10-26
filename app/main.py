import socket  # noqa: F401
import threading

BUFFER_SIZE = 4096
my_dict = {}
def handle_command(client : socket.socket):
    with client:
        while True:
            
            
            chunk = client.recv(BUFFER_SIZE)

            if not chunk: 
                break
           
            
            data = chunk.split(b"\r\n")
            
            command = data[2].decode()
            print(f"Received command: {command}")
            if command == "PING":
                client.sendall(b"+PONG\r\n")
            elif command == "ECHO":
                msg = data[-2]
                client.sendall(b"$" + str(len(msg)).encode() + b"\r\n" + msg + b"\r\n")
            elif command == "SET":
                key = data[4].decode()
                value = data[6].decode()

                if len(data) > 8 and data[8].decode() == "PX":
                    ttl = int(data[10].decode())
                    threading.Timer(ttl / 1000, my_dict.pop, args=[key]).start()
                my_dict[key] = value
                client.sendall(b"+OK\r\n")
            elif command == "GET":
                key = data[4].decode()
                value = my_dict.get(key, None)
                print(f"Inside Get Command:", {value})
                if value is not None:
                    value = value.encode()
                    client.sendall(b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n")
                elif value is None :
                    client.sendall(b"$-1\r\n")
            else :
                client.sendall(b"-ERR unknown command\r\n")
            
                


            
            

            

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
