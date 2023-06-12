#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler,HTTPServer
import socket, select
import cgi
import argparse

class ProxyRequestHandler(BaseHTTPRequestHandler):

    sockets = {}
    BUFFER = 1024 * 50 
    SOCKET_TIMEOUT = 50

    def _get_connection_id(self):
        """
        It returns the connection ID from the URL path
        :return: The connection id is being returned.
        """
        return self.path.split('/')[-1]

    def _get_socket(self):
        """
        It returns the socket which connects to the target address for this connection
        :return: The socket which connects to the target address for this connection.
        """
        id = self._get_connection_id()
        return self.sockets.get(id, None)

    def _close_socket(self):
        """
        It closes the socket
        """
        id = self._get_connection_id()
        s = self.sockets[id]
        if s:
            s.close()
            del self.sockets[id]


    def do_GET(self):
        """
        > The function tries to read data from the socket, if it succeeds it returns the data to the client
        through the http response, otherwise it returns an error code

        GET: Read data from TargetAddress and return to client through http response
        """
        s = self._get_socket()
        if s:
            # check if the socket is ready to be read
            to_reads, to_writes, in_errors = select.select([s], [], [], 5)
            if len(to_reads) > 0: 
                to_read_socket = to_reads[0]
                try:
                    print("Getting data from target address")
                    data = to_read_socket.recv(self.BUFFER)
                    print(data)
                    self.send_response(200)
                    self.end_headers()
                    if data:
                        self.wfile.write(data)
                except socket.error as ex:
                    print ('Error getting data from target socket: ' , ex  )
                    self.send_response(503)
                    self.end_headers()
            else: 
                print('No content available from socket')
                self.send_response(204) # no content had be retrieved
                self.end_headers()
        else:
            print ('Connection With ID,' + self._get_connection_id() +' , has not been established' )
            self.send_response(400)
            self.end_headers()


    def do_POST(self):
        """
        The function creates a socket connection to the target host and port, and saves the socket reference
        in a dictionary.

        POST: Create TCP Connection to the TargetAddress

        """
        id = self._get_connection_id() 
        print( 'Initializing connection with ID ' , id)
        length = int(self.headers.getheader('content-length'))
        req_data = self.rfile.read(length)
        params = cgi.parse_qs(req_data, keep_blank_values=1) 
        target_host = params['host'][0]
        target_port = int(params['port'][0])

        print('Connecting to target address: ', target_host, " : ", target_port )
        # open socket connection to remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # use non-blocking socket
        s.setblocking(0)
        s.connect_ex((target_host, target_port))

        #save socket reference
        self.sockets[id] = s
        try: 
            self.send_response(200)
            self.end_headers()
        except Exception as e:
            print(e)

    def do_PUT(self):
        """
        Read data from HTTP Request and send to TargetAddress
        
        The function reads data from the HTTP request and sends it to the target address. 
        
        The function first checks if the connection with the given id exists. If it doesn't, it sends a 400
        response. 
        
        If the connection exists, it reads the data from the HTTP request and sends it to the target
        address. 
        
        The function uses the select module to check if the socket is ready to write. If it is, it sends the
        data to the target address. 
        
        If the socket is not ready to write, it sends a 504 response.
        """
        id = self._get_connection_id()
        s = self.sockets[id]
        if not s:
            print("Connection with id", id ," doesn't exist" )
            self.send_response(400)
            self.end_headers()
            return
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)['data'][0] 

        # check if the socket is ready to write
        to_reads, to_writes, in_errors = select.select([], [s], [], 5)
        if len(to_writes) > 0: 
            print ('Sending data ....', data)
            to_write_socket = to_writes[0]
            try: 
                to_write_socket.sendall(data)
                self.send_response(200)
            except socket.error as ex:
                print ('Error sending data from target socket:', ex  )
                self.send_response(503)
        else:
            print('Socket is not ready to write')
            self.send_response(504)
        self.end_headers()

    def do_DELETE(self): 
        """
        It closes the socket, sends a 200 response, and ends the headers
        """
        self._close_socket()
        self.send_response(200)
        self.end_headers()

def run_server(port, server_class=HTTPServer, handler_class=ProxyRequestHandler): 
    """
    It creates a server object, and then calls the serve_forever() method on that object
    
    :param port: The port number that the proxy server will run on
    :param server_class: The class to use for instantiating a server. By default, this is set to
    HTTPServer, which is the base HTTP server included in Python
    :param handler_class: This is the class that will handle the requests
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Tunnel Server")
    parser.add_argument("-p", default=9999, dest='port', help='Specify port number server will listen to', type=int)
    args = parser.parse_args()
    run_server(args.port)