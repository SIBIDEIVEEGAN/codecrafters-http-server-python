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

    todata = con.recv(1024).decode('utf-8')
    data = todata.splitlines()

    path = data[0].split(" ")[1]
    method = data[0].split(" ")[0]
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
        print(data[0])
        if method == "GET":
            if os.path.exists(file_path):
                with open(file_path,"r") as file:
                    fileContent = file.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(fileContent)}\r\n\r\n{fileContent}\r\n"
        else:
            file_content = todata.split("\r\n\r\n")[-1]
            with open(file_path, "w") as file:
                file.write(file_content)
            response = "HTTP/1.1 201 Created \r\n\r\n"
        
        con.send(response.encode())
    
      
     
    else:
        con.send(b"HTTP/1.1 404 Not Found \r\n\r\n")

    con.close()

if __name__ == "__main__":
    main()
