import requests
import socket
import threading


def lookup(url):
    return socket.gethostbyname(url)


class Address:
    __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, url, protocol="https", path="/"):
        self.url = url
        self.prot = protocol

    def get(self, **kwargs):
        return requests.get(f"{self.prot}://{self.url}", **kwargs)

    def put(self, **kwargs):
        return requests.put(f"{self.prot}://{self.url}", **kwargs)

    def post(self, **kwargs):
        return requests.post(f"{self.prot}://{self.url}", **kwargs)

    def delete(self, **kwargs):
        return requests.delete(f"{self.prot}://{self.url}", **kwargs)

    def connect(self, port=443):
        self.__sock.connect((self.url, port))
        return self

    def receive(self, buffer, flags: int = 0):
        return self.__sock.recv(buffer, flags).decode("utf-8")

    def send(self, data, flags: int = 0):
        data = data.encode("utf-8")
        return self.__sock.send(data, flags)

    def get_socket(self):
        return self.__sock


class WebServer:
    def __init__(self, ip, port):
        self.__stopped = False
        self.ip = socket.gethostbyname(ip)
        self.port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.ip, self.port))

    def on_connect(self, connection, addr, callback):
        try:
            types = {
                "image": ["png", "jpg", "ico"]
            }
            page = callback.split()[1].strip("/")
            ext = page.split('.')[1]
            for t in types:
                if ext in types[t]:
                    pref = t
                    break
            else:
                pref = "text"
            headers = f"HTTP/1.1 200 OK\r\nContent-Type: {pref}/{ext}; charset=utf-8\r\n\r\n"

            with open(page, "rb") as file:
                content = file.read()
            connection.send(headers.encode("utf-8") + content)
        except FileNotFoundError:
            h = "HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            connection.send(h.encode(
                "utf-8") + b"""<h1 style='padding:0; margin:0'>404</h1>
                           <h2 style='padding:0; margin:0'>Not found</h2>
                           <p style='padding:0; margin:20px 0;'><b>AEngine</b> webserver</p>""")
        connection.shutdown(socket.SHUT_WR)

    def __listen(self):
        while not self.__stopped:
            try:
                self.__sock.listen()
                a, b = self.__sock.accept()
                print(f"[+]connected to {b[0]}:{b[1]}")
                callback = a.recv(1024).decode("utf-8")
                self.on_connect(a, b, callback)
            except Exception as e:
                print(e)

    def start_listen(self):
        info = self.__sock.getsockname()
        print(f"listening on {info[0]}:{info[1]}")
        threading.Thread(target=self.__listen).start()

    def stop(self):
        self.__stopped = True


class Server:
    def __init__(self, ip, port, buffer=1024):
        self.buffer = buffer
        self.__stopped = False
        self.ip = ip
        self.port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.ip, self.port))

    def on_callback(self, connection, addr, callback):
        pass

    def on_connect(self, connection, addr):
        pass

    def __listen(self):
        while not self.__stopped:
            try:
                self.__sock.listen()
                a, b = self.__sock.accept()
                print(f"[+] connected to {b[0]}:{b[1]}.")
                a.send(b'[+] connected to ' + f"{socket.gethostbyname(socket.gethostname())}:{self.port}.\n".encode(
                    "utf-8"))
                callback = ""
                self.on_connect(a, b)
                while not callback.strip() == "exit":
                    a.send(b" ")
                    callback = a.recv(self.buffer).decode("utf-8").strip()
                    if callback:
                        self.on_callback(a, b, callback)
                print("[+] connection closed.")
                a.send(b"[+] connection closed.")
                a.close()

            except Exception as e:
                a.close()
                print("[+] connection closed.")
                print(e)

    def start_listen(self):
        info = self.__sock.getsockname()
        print(f"listening on {info[0]}:{info[1]}")
        threading.Thread(target=self.__listen).start()

    def stop(self):
        self.__stopped = True


if __name__ == "__main__":
    Server(socket.gethostname(), 80).start_listen()
