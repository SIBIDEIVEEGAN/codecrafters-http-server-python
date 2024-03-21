# Uncomment this to pass the first stage
import socket
import threading
import os
import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    
    
    while True:
        con , adr = server_socket.accept() # wait for client
        thread = threading.Thread(target=handle_client, args=(con, adr))
        thread.start()



def handle_client(con, adr):
    data = con.recv(1024).decode('utf-8').splitlines()

    path = data[0].split(" ")[1]

    if path == "/":
        con.send(b"HTTP/1.1 200 OK \r\n\r\n")
    elif path.startswith("/echo/"):
        msg =  msg = path[len("/echo/"):]
        mlen = len(msg)
        con.send(f"HTTP/1.1 200 OK \r\nContent-Type: text/plain\r\nContent-Length: {mlen}\r\n\r\n{msg}".encode())
    elif path == "/user-agent":
        user_agent = data[2].split(":", 1)[1].strip()
        mlen = len(user_agent)
        con.send(f"HTTP/1.1 200 OK \r\nContent-Type: text/plain\r\nContent-Length: {mlen}\r\n\r\n{user_agent}".encode())
    elif path.startswith("/files/"):
        
        directory = ""
        if sys.argv[1] == "--directory":
            directory = sys.argv[2]
        filename =  path[len("/files/"):]
        file_path = os.path.join(directory, filename)
        response = "HTTP/1.1 404 Not Found \r\n\r\n"
        if os.path.exists(file_path):
            with open(file_path,"r") as file:
                fileContent = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(fileContent)}\r\n\r\n{fileContent}\r\n"

       
        print(response)
        con.send(response.encode())
     
    else:
        con.send(b"HTTP/1.1 404 Not Found \r\n\r\n")

    con.close()

if __name__ == "__main__":
    main()
