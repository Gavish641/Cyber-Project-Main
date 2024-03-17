import socket
import threading
import sys
import json


class MultiThreadedClient(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.CHAT_SERVER_IP = "10.100.102.12"
        self.CHAT_SERVER_PORT = 5555
        self.chat_messages = []
        self.username = ""
        self.messages = []
        self.current_game = []
        self.found_player = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_flag = threading.Event() # Event to signal thread termination
        self.client_thread = threading.Thread(target=self.connect)
        
        self.chat_thread = threading.Thread(target=self.receive_messages_chat)
        self.stop_chat_flag = threading.Event()
    
    def run(self):
        self.client_thread.start()

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
        self.receive_data()
        
    def disconnect(self):
        print("Client disconnected")
        self.stop_flag.set() # Set the stop flag to signal thread termination
        self.client_socket.close()

    def send_message(self, data):
        json_message = json.dumps(data)
        self.client_socket.send(json_message.encode())

    def receive_data(self):
        while not self.stop_flag.is_set(): # Check the stop flag in the loop
            print("Main Servering")
            try:
                data = self.client_socket.recv(1024)            
                msg = self.decode_json(data)        
                print("Main Server: >>> " + str(msg))
                if not msg:
                    break
                if type(msg) is list:
                    if msg[0] == "login" or msg[0] == "signup":
                        if msg[1] == "success":
                            self.username = msg[2]
                            self.messages = msg # ["login/signup, "success", self.username])

                        else:
                            self.messages = msg # ["login/signup", "error"]
                    if msg[0] == "game" and msg[1] == "chat" and msg[2] == "found":
                        self.found_player = True
                        self.messages = msg
                    else:
                        self.messages = msg
                        self.found_player = False
            except:
                self.client_socket.close()

    def decode_json(self, data):
        try:
            decoded_data = data
            if decoded_data:
                return json.loads(decoded_data)
            else:
                # Handle the case when the decoded data is empty
                return None
        except json.decoder.JSONDecodeError as e:
            # Handle the invalid JSON case
            print(f"Error decoding JSON: {e}")
            return None
    
    def connect_to_chat(self):
        self.stop_flag.set()
        self.stop_chat_flag.clear()
        self.chat_thread.start()
    
    def send_chat_message(self, message):
        if message:
            self.client_socket.send(message.encode('utf-8'))


    def receive_messages_chat(self, ):
        while not self.stop_chat_flag.is_set():
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                msg = self.decode_json(data)
                print("Chat: >>> " + str(msg))
                self.chat_messages.append(msg)
            except Exception as e:
                break

    def leave_chat(self):
        self.stop_flag.clear()
        self.client_thread.join()
        self.stop_chat_flag.set()
    
