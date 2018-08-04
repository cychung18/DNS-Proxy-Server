import socket
import sys
import select


# 1 - 12 bytes is DNS header
class Server:

    def __init__(self, ip):
        
        ip = ip.split('.')
        # convert typr from string to byte
        self.my_ip = chr(int(ip[0])) + chr(int(ip[1])) + chr(int(ip[2])) + chr(int(ip[3]))

    # Get host ip address
    # but we got different result in this function, we decided not to use this function to get ip address
    # Instead, we input ip address as we run this server
    def get_my_ip(self):
        # the type is string type, so we should preprocess it
        my_ip = socket.gethostbyname(socket.gethostname())
        my_ip = my_ip.split('.')
        # convert type from string to byte
        return chr(int(my_ip[0])) + chr(int(my_ip[1])) + chr(int(my_ip[2])) + chr(int(my_ip[3]))

    def fetch_default_packet(self, filename):
        fp = open(filename, 'r')
        my_packet = fp.read()
        fp.close()
        return bytearray(my_packet)

       #  determine "no such name" response by EXIST_WEB'''
       #  If it is a no such name" response, we will respond our server ip address for advertising.'''
    def handle_response(self, data, data_g): 
        EXIST_WEB = bytearray(data_g)[3] & 0b00000001 # extract the bit to determine it
        if EXIST_WEB:
            dns_id = bytearray(data_g)[:2]
            # we already write a complete default packet by request google dns. 
            # It helps us to construct the packet.
            my_default_packet = self.fetch_default_packet('my_default_packet.txt') 
            # when we repond to client, the dns id and user question should be the same
            my_default_packet[0:2] = dns_id
            user_query = data[12:]
            my_res = my_default_packet[0:12] + user_query + my_default_packet[67:]
            my_res[-4:] = self.my_ip
            return my_res
        else:
            return data_g

    def server_run(self):
        ''' Create UDP and TCP socket to receive message from client'''
        sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('', 53)
        sock_udp.bind(server_address)
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.bind(('', 53))
        sock_tcp.listen(5)
        # use select function to help us to listen to multiple socket
        inputs = [sock_udp, sock_tcp]
        n = 1
        client_info = {}
        while True:
            readable, writable, exceptional = select.select(inputs, [], inputs)
            for s in readable:
                # handle tcp socket
                if s is sock_tcp:
                    conn, address = sock_tcp.accept()
                    data = conn.recv(4096)
                    sock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock_g.connect(('8.8.8.8', 53))
                    sock_g.sendall(data)
                    while True:
                        response = sock_g.recv(1024)
                        if not response: break
                        conn.sendall(response)
                    conn.shutdown(socket.SHUT_WR)
                    conn.close()
                    sock_g.close()
                    n += 1
                # handel udp socket
                else:
                    data, address = sock_udp.recvfrom(4096)
                    if address[0] == '8.8.8.8':
                        dns_id = str(bytearray(data)[:2])
                        if dns_id in client_info:
                            response = self.handle_response(client_info[dns_id][1], data)
                            sent = sock_udp.sendto(response, client_info[dns_id][0])
                            client_info.pop(dns_id, None)
                    else:
                        n += 1
                        sent = sock_udp.sendto(data, ("8.8.8.8", 53))
                        dns_id = str(bytearray(data)[:2])
                        client_info[dns_id] = [address, data]

            print "Succeed query {0} request.".format(n)
        sock_tcp.close()
        sock_udp.close()

def main():
    
    if len(sys.argv) < 2:
        print "Error: You should enter your ip address."
        exit()
    ip = sys.argv[1]
    s = Server(ip)
    s.server_run()


if __name__ == '__main__':
    main()
