import logging
import sys
import socketserver
import socket
import matlab.engine

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


class EchoRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        eng = matlab.engine.start_matlab()
        self.logger.debug('handle')

        # Echo the back to the client
        data = self.request.recv(4096)
        self.logger.debug('recv()->"%s"', data)
        data = data.decode('utf-8')
        data = data.replace('\t',' ')
        data = data.split(' ')
        data = list(filter(lambda a: a != '',data))
        data = [float(e) for e in data]
        while len(data)%4 != 0:
            data.pop()
        with open('data.txt','w+') as f:
            for i in range(int(len(data)/4)):
                j = i*4
                f.write('%f %f %f %f\r\n' % (data[j],data[j+1],data[j+2],data[j+3]))
            f.close()
        results = eng.calc()
        s = ''
        for e in results:
            s += str(e) + " "
        self.request.send(s.encode('utf-8'))
        return

    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)


class EchoServer(socketserver.TCPServer):

    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        socketserver.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug('waiting for request')
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return socketserver.TCPServer.close_request(self, request_address)


if __name__ == '__main__':

    import threading

    address = ('192.168.0.15', 65000)  # let the kernel give us a port
    server = EchoServer(address, EchoRequestHandler)
    ip, port = server.server_address  # find out what port we were given
    print(ip)
    print(port)
    server.serve_forever()

