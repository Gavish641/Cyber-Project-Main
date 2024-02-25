import socket
import select
from server_utils import UsersDB, Message, Sorting_Numbers
import threading
import json

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            client_message = data.decode('utf-8')
            if not data or client_message == "exit":
                break
            print(f"Received data: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_exit(client_socket)


def client_exit(client_socket):
    client_socket.close()
    print("Client has disconnected")


'''class MultiThreadedServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def start_server(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                client_handler = threading.Thread(target=handle_client, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

'''
class Server:
    # handles the multiuser server
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.message = Message()
        self.clients = [self.server_socket]
        self.database = UsersDB()
        self.sorting_numbers = Sorting_Numbers()
        self.messages = []

        # Initialize rlist, wlist, and xlist
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def start(self):
        print(f"Server is listening on {self.server_socket.getsockname()}")

        while True:
            # Copy the clients list to rlist for monitoring read events
            self.rlist = list(self.clients)
            rlist, _, _ = select.select(self.rlist, self.wlist, self.xlist)

            for sock in rlist:
                if sock == self.server_socket:
                    # New connection, accept it
                    client_socket, client_address = self.server_socket.accept()
                    self.clients.append(client_socket)
                    print(f"New connection from {client_address}")
                else:
                    # Handle data from an existing client
                    try:
                        data = sock.recv(1024)
                        self.messages.append(self.message.decode_json(data))
                        print("Client: ", self.message.decode_json(data))
                        result_msg = self.handle_messages()
                        print("Server: ", str(result_msg))
                        result_json_msg = self.message.encode_json(result_msg)
                        sock.send(result_json_msg)
                    except:
                        self.clients.remove(sock)
                        print("Server: Client has been disconnected")
                    

    def handle_messages(self):
        for msg in self.messages:
            if type(msg) is list:
                if msg[0] == "login":
                    if self.database.try_login(msg[1], msg[2]):
                        username = msg[1]
                        self.messages.remove(msg)
                        return ["login", "success", username] # msg[1] -> username
                    else:
                        if self.database.check_user_registered(msg[1]):
                            self.database.check_user_registered(msg[1])
                        self.messages.remove(msg)
                        return ["login", "error", self.database.check_user_registered(msg[1])]
                    
                if msg[0] == "signup":
                    if not self.database.check_user_registered(msg[1]):
                        self.database.insert_user(msg[1], msg[2])
                        print("new user successfully registered")
                        username = msg[1]
                        self.messages.remove(msg)
                        return ["signup", "success", username] # [2] -> username
                    else:
                        # the username is already exists
                        print("This username is already exists")
                        self.messages.remove(msg)
                        return ["signup", "error", msg[1]]
                    
                if msg[0] == "game":

                    if msg[1] == "sorting numbers":
                        if msg[2] == "start":
                            numbers = self.sorting_numbers.generate_numbers()
                            self.messages.remove(msg)
                            return ["game", "sorting numbers", numbers]
                        
                        if msg[2] == "check sorted numbers":
                            if int(msg[3]) == int(''.join(map(str, sorted(self.sorting_numbers.numbers_to_sort)))):
                                self.messages.remove(msg)
                                return ["game", "sorting numbers", "success"]
                            self.messages.remove(msg)
                            return ["game", "sorting numbers", "fail"]
            # self.messages.remove(msg)

    def close(self):
        self.server_socket.close()


if __name__ == "__main__":
    # Create and start the server
    server = Server('127.0.0.1', 12345)
    server.start()