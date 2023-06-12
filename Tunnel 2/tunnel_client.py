#!/usr/bin/env python
import socket, time
import http.client, urllib
from uuid import uuid4
import threading
import argparse
import sys

BUFFER = 1024 * 50


class Connection():
    
    def __init__(self, connection_id, remote_addr, proxy_addr):
        """
        It creates a new HTTP connection to the proxy server, and stores the connection in the `http_conn`
        variable
        
        :param connection_id: The ID of the connection. This is used to identify the connection in the HTTP
        headers
        :param remote_addr: The address of the remote server that the client is trying to connect to
        :param proxy_addr: The address of the proxy server
        """
        self.id = connection_id
        conn_dest = proxy_addr if proxy_addr else remote_addr
        print("Establishing connection with remote tunneld at " + conn_dest['host'] + ":" + conn_dest['port'])
        self.http_conn = http.client.HTTPConnection(conn_dest['host'], conn_dest['port'])
        self.remote_addr = remote_addr

    def _url(self, url):
        return "http://{host}:{port}{url}".format(host=self.remote_addr['host'], port=self.remote_addr['port'], url=url)

    def create(self, target_addr):
        params = urllib.parse.urlencode({"host": target_addr['host'], "port": target_addr['port']})
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        self.http_conn.request("POST", self._url("/" + self.id), params, headers)

        response = self.http_conn.getresponse()
        response.read()
        if response.status == 200:
            print('Successfully create connection')
            return True 
        else:
            print('Fail to establish connection: status ' , response.status , ' because ' ,response.reason)
            return False 

    def send(self, data):
        params = urllib.urlencode({"data": data})
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        try: 
            self.http_conn.request("PUT", self._url("/" + self.id), params, headers)
            response = self.http_conn.getresponse()
            response.read()
            print(response.status)
        except Exception as ex:
            print ("Error Sending Data: ",ex)

    def receive(self):
        try: 
            self.http_conn.request("GET", "/" + self.id)
            response = self.http_conn.getresponse()
            data = response.read()
            if response.status == 200:
                return data
            else: 
                return None
        except Exception as ex:
            print ("Error Receiving Data: " ,ex)
            return None 

    def close(self):
        print("Close connection to target at remote tunnel")
        self.http_conn.request("DELETE", "/" + self.id)
        self.http_conn.getresponse()

class SendThread(threading.Thread):

    """
    Thread to send data to remote host
    """
    
    def __init__(self, client, connection):
        threading.Thread.__init__(self, name="Send-Thread")
        self.client = client
        self.socket = client.socket
        self.conn = connection
        self._stop = threading.Event()

    def run(self):
        while not self.stopped():
            print ("Getting data from client to send")
            try:
                data = self.socket.recv(BUFFER)
                if data == '': 
                    print ("Client's socket connection broken")
                    # There should be a nicer way to stop receiver
                    self.client.receiver.stop()
                    self.client.receiver.join()
                    self.conn.close()
                    return

                print ("Sending data ... "  , data)
                self.conn.send(data)
            except socket.timeout:
                print ("time out")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class ReceiveThread(threading.Thread):

    """
    Thread to receive data from remote host
    """

    def __init__(self, client, connection):
        threading.Thread.__init__(self, name="Receive-Thread")
        self.client = client
        self.socket = client.socket
        self.conn = connection
        self._stop = threading.Event()

    def run(self):
        while not self.stopped():
            print ("Retreiving data from remote tunneld")
            data = self.conn.receive()
            if data:
                sent = self.socket.sendall(data)
            else:
                print ("No data received")
                # sleep for sometime before trying to get data again
                time.sleep(1)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class ClientWorker(object):

    def __init__(self, socket, remote_addr, target_addr, proxy_addr):
        #threading.Thread.__init__(self)
        self.socket = socket
        self.remote_addr = remote_addr 
        self.target_addr = target_addr
        self.proxy_addr = proxy_addr

    def start(self):
        #generate unique connection ID
        connection_id = str(uuid4())
        #main connection for create and close
        self.connection = Connection(connection_id, self.remote_addr, self.proxy_addr)

        if self.connection.create(self.target_addr):
            self.sender = SendThread(self, Connection(connection_id, self.remote_addr, self.proxy_addr))
            self.receiver = ReceiveThread(self, Connection(connection_id, self.remote_addr, self.proxy_addr))
            self.sender.start()
            self.receiver.start()

    def stop(self):
        #stop read and send threads
        self.sender.stop()
        self.receiver.stop()
        #send close signal to remote server
        self.connection.close()
        #wait for read and send threads to stop and close local socket
        self.sender.join()
        self.receiver.join()
        self.socket.close()




def start_tunnel(listen_port, remote_addr, target_addr, proxy_addr):
    """Start tunnel"""
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.settimeout(None)
    listen_sock.bind(('', int(listen_port)))
    listen_sock.listen(1)
    print ("waiting for connection")
    workers = []
    try:
        while True:
            c_sock, addr = listen_sock.accept() 
            c_sock.settimeout(20)
            print ("connected by ", addr)
            worker = ClientWorker(c_sock, remote_addr, target_addr, proxy_addr)
            workers.append(worker)
            worker.start()
    except (KeyboardInterrupt, SystemExit):
        listen_sock.close()
        for w in workers:
            w.stop()
        for w in workers:
            w.join()
        sys.exit()

if __name__ == "__main__":
    """Parse argument from command line and start tunnel"""

    parser = argparse.ArgumentParser(description='Start Tunnel')
    parser.add_argument('-p', default=8889, dest='listen_port', help='Port the tunnel listens to, (default to 8889)', type=int)
    parser.add_argument('target', metavar='Target Address', help='Specify the host and port of the target address in format Host:Port')
    parser.add_argument('-r', default='localhost:9999', dest='remote', help='Specify the host and port of the remote server to tunnel to (Default to localhost:9999)')
    parser.add_argument('-o', default='', dest='proxy', help='Specify the host and port of the proxy server(host:port)')

    args = parser.parse_args()

    target_addr = {"host": args.target.split(":")[0], "port": args.target.split(":")[1]}
    remote_addr = {"host": args.remote.split(":")[0], "port": args.remote.split(":")[1]}
    proxy_addr = {"host": args.proxy.split(":")[0], "port": args.proxy.split(":")[1]} if (args.proxy) else {}
    start_tunnel(args.listen_port, remote_addr, target_addr, proxy_addr)