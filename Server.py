import socket
import ssl
from datetime import datetime
import subprocess
import platform
from gmail import email_alert
import requests
import time
from pythonping import ping 


class Server():

    def create_history(self, msg, success, now,status_code):
        history_max = 100
        try:
            url_response_time = "https://"+ self.name
            start_time = time.time()
            response = requests.get(url_response_time)
            end_time = time.time()
            response_time = end_time-start_time
        except:
            response_time = 1000
        self.history.append((msg, success,now,status_code,response_time)) 
        while len(self.history) > history_max:
            self.history.pop(0)

    def __init__(self, name, port, connection, priority):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()
        self.history = []
        self.alert = False
    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()

        try:
            url = "https://"+ self.name
            response = requests.get(url)
            headers = response.headers
            global status_code
            status_code = response.status_code
            if(status_code == 503 or status_code == 502 or status_code == 501 or status_code == 500):
                msg = "Website might be down due to " + str(status_code) + " Status Code"
                self.alert = True
                email_alert(self.name, msg, "Enter your email here")

            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False
            elif self.connection == "ssl":
                ssl.wrap_socket(socket.create_connection((self.name, self.port), timeout=10))
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False
            else:
                resp = ping(self.name)
                if(resp.success()):
                    self.alert = False
                    success = True
                    msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                else:
                    raise Exception

        except socket.timeout:
            msg = f"server: {self.name} timeout. On port {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"server: {self.name} {e}"
        except Exception as e:              
            msg = f"No Clue??: {e}"
        if success == False and self.alert == False:
            # Send Alert
            self.alert = True
            email_alert(self.name, f"{msg}\n{now}", "Enter your email here")
        self.create_history(msg, success, now,status_code)

if __name__ == "__main__":
    servers = [
        Server("google.com", 443, "not_specified", "high"),
        # Server("yeetzilla.net",80,"plain","high"),
        Server("msn.com", 80, "plain", "high"),
        Server("smtp.gmail.com", 443, "ssl", "high"),
        Server("yahoo.com", 80, "plain", "high")
    ]
    for server in servers:
        server.check_connection()
        print(len(server.history))
        print(server.history[-1])

    # pickle.dump(servers, open("servers.pickle", "wb"))