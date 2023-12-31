import socket


class PortGenerator:

    def __init__(self, base_port):
        self.base_port = base_port
        self.last = self.base_port

    def is_port_available(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close() 
        if result == 0:
            print(f"Port {port} is in use")
            return False
        else:
            print(f"Port {port} is available")
            return True

    def get_port(self, port=None, n=100):
        port = self.last if port is None else port
        for i in range(0, n):
            if self.is_port_available(port):
                return port
            port += 1
        raise Exception(f"Could not find available port in range {self.last} - {port}")
        
