import socket
import sys
import datetime
import select

class Server:
    
    def __init__(self):
        self.buffer_size = 1024
        self.status_code_word = {200: "OK", 403: "Forbidden", 404: "Not Found"}

    def get_header(self, status_code, content_length):
        res = "HTTP/1.1 {0} {1}\n".format(status_code, self.status_code_word[status_code])
        res += "Date: " + str(datetime.datetime.now()) + "\n"
        res += "Server: my simple server\n"
        res += "Content-Type: text/html\n"
        res += "Content-Length: {0}\n".format(content_length)
        res += "\r\n"
        return res

    def handle_body(self, data):

        pos1 = data.find('Host')
        pos2 = data.find('\n', pos1 + 1)
        domain_name = data[pos1 + 6 : pos2 - 1]
        res = "<html><h2>Hello! <br>" \
              "I see you were looking for {0}, <br>".format(domain_name)
        res += "but wouldn't you rather buy that from <a>walmart.com</a>" \
               "</h2></html>\n"
        return res, 200

    def server_run(self, PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = ''
        sock.bind((HOST, PORT))
        sock.listen(5)
        conn, address = sock.accept()

        inputs = [sock]
        while inputs:
            readable, writable, exceptional = select.select(inputs, [], inputs)

            for s in readable:
                if s is sock:
                    conn, address = sock.accept()
                    inputs.append(conn)
                else:
                    data = s.recv(self.buffer_size)
                    body, status_code = self.handle_body(data)
                    response = self.get_header(status_code, len(body)) + body
                    s.sendall(response)
                    s.close()
                    inputs.remove(s)

        sock.close()

def main():

    s = Server()
    s.server_run(80)


if __name__ == '__main__':
    main()
