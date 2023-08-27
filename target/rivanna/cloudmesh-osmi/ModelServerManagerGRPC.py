"""TensorFlow Model Server Manager with gRPC.

Usage:
  ModelServerManagerGRPC.py [--server_url=<url>] [--port=<port>] [--gpus=<gpu_fractions>] [--log_file=<log_path>]
  ModelServerManagerGRPC.py (-h | --help)

Options:
  --server_url=<url>      TensorFlow Model Server URL [default: http://localhost:8501].
  --port=<port>           Port number for the gRPC server [default: 50051].
  --gpus=<gpu_fractions>  GPU fractions separated by commas [default: 0.0].
  --log_file=<log_path>   Path to the log file [default: server_log.txt].
  -h --help               Show this help message and exit.
"""

import grpc
import subprocess
import time
import requests
from concurrent import futures
from docopt import docopt
import tf_server_pb2
import tf_server_pb2_grpc

class ModelServiceServicer(tf_server_pb2_grpc.ModelServiceServicer):
    def StartServer(self, request, context):
        manager = TFModelServerManager(request.server_url, request.port, request.gpus, request.log_file)
        manager.start_tf_model_server()
        manager.wait_for_server()

        return tf_server_pb2.ServerResponse(success=True, message="Server started successfully")

class TFModelServerManager:
    def __init__(self, server_url, port, gpus=None, log_file="server_log.txt"):
        self.server_url = server_url
        self.port = port
        self.gpus = gpus
        self.server_check_url = f"{self.server_url}:{port}/v1/models/my_model"
        self.max_attempts = 30
        self.log_file = log_file
        self.server_process = None

    def start_tf_model_server(self):
        cmd = [
            "tensorflow_model_server",
            "--port=" + str(self.port),
            "--model_name=my_model",
            "--model_base_path=" + self.server_url
        ]

        if self.gpus is not None:
            cmd.extend(["--per_process_gpu_memory_fraction=" + str(gpu_fraction) for gpu_fraction in self.gpus])

        log_file = open(self.log_file, "w")
        self.server_process = subprocess.Popen(cmd, stdout=log_file, stderr=log_file)
        print("TensorFlow Model Server started on port", self.port)

    def check_server_availability(self):
        try:
            response = requests.get(self.server_check_url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        return False

    def wait_for_server(self):
        attempt = 0
        while attempt < self.max_attempts:
            if self.check_server_availability():
                print("TensorFlow Model Server is up and available!")
                break
            else:
                print("Waiting for TensorFlow Model Server...")
                attempt += 1
                time.sleep(2)
        else:
            print("Timed out waiting for TensorFlow Model Server to become available.")

def main():
    arguments = docopt(__doc__)

    server_url = arguments['--server_url']
    port = int(arguments['--port'])
    gpus = [float(f) for f in arguments['--gpus'].split(',')]
    log_file = arguments['--log_file']

    manager = TFModelServerManager(server_url, port, gpus, log_file)
    manager.start_tf_model_server()
    manager.wait_for_server()

if __name__ == "__main__":
    main()
