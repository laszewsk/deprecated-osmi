"""
Usage:
  ModelServer.py start_and_wait [-c <config>] [-p <port>] [-g <ngpus>] [-o <output_dir>] [-t <tfs_sif>]
  ModelServer.py start [-c <config>] [-p <port>] [-g <ngpus>] [-o <output_dir>] [-t <tfs_sif>]
  ModelServer.py wait [--timeout=<timeout>]
  ModelServer.py status [-p <port>]
  ModelServer.py (-h | --help)

Options:
  -c <config> --config=<config>       Config file [default: config.yaml].
  -p <port> --port=<port>             Base port for TF servers.
  -g <ngpus> --ngpus=<ngpus>          Number of GPUs.
  -o <output_dir> --output_dir=<output_dir>   Directory to store output logs.
  -t <tfs_sif> --tfs_sif=<tfs_sif>    Tensorflow serving singularity image.
  --status=<status>                   Server status (for wait command).
  --timeout=<timeout>                 Timeout (for wait command).
  -h --help                           Show this screen.
"""

from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.StopWatch import StopWatch
from yaml_to_conf import YamlToJsonConverter
import os
import socket
import time
from docopt import docopt
from pprint import pprint

SINGULARITY = "singularity exec --bind `pwd`:/home --pwd /home"

class ModelServer:

    def __init__(self, config, config_filename=None):
        self.tfs_base_port = config["constant.tfs_base_port"]
        self.ngpus = config["experiment.ngpus"]
        self.output_dir = config["data.output"]
        self.batch = config["experiment.batch"]
        self.tfs_sif = config["data.tfs_sif"]
        self.timeout = config["constant.timeout"]
        self.model_conf_file = self.convert_conf_to_json(config_filename)

    def convert_conf_to_json(self, config_filename):
        converter = YamlToJsonConverter(config_filename, "models")
        converter.convert()
        return converter.get_name()

    def start(self):
        # for device in self.visible_devices.split(','):
        StopWatch.event("ModelServer: start")
        for i in range(self.ngpus):
            port = self.tfs_base_port + i
            command = f"time CUDA_VISIBLE_DEVICES={i} "\
                      f"{SINGULARITY} {self.tfs_sif} "\
                      f"tensorflow_model_server --port={port} --rest_api_port=0 --model_config_file={self.model_conf_file} "\
                      f">& {self.output_dir}/v100-{port}.log &"
            print(command)
            r = os.system(command)
            print(r)
    
    def shutdown(self):
        raise NotImplementedError

    def status(self, port):
        StopWatch.event("ModelServer: status")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex(('127.0.0.1', port)) == 0

    def wait_for_server(self):
        StopWatch.event("ModelServer: wait for server")
        start = time.time()
        while not all([self.status(p + self.tfs_base_port) for p in range(self.ngpus)]):
            if time.time() - start > self.timeout:
                print("Server not properly started")
                raise ValueError("Server not properly started")
            time.sleep(0.5)
            print(".", end="")
        StopWatch.event("ModelServer: server up")
        print()


def main():
    args = docopt(__doc__)
    pprint(args)
    config_filename = args["--config"] or "config.yaml"
    config = FlatDict()
    config.load(content=config_filename, expand=True)
    config["experiment.ngpus"] = int(config["experiment.ngpus"])
    pprint(config)

    arg_to_config_mapping = {
        "--port": "constant.tfs_base_port",
        "--ngpus": "experiment.ngpus",
        "--output_dir": "data.output",
        "--tfs_sif": "data.tfs_sif",
        "--timeout": "constant.timeout",
    }

    for arg_key, config_key in arg_to_config_mapping.items():
        arg_value = args[arg_key]
        if arg_value:
            config[config_key] = arg_value

    model_server = ModelServer(config, config_filename)
    if args['start']:
        model_server.start()
    elif args['wait']:
        model_server.wait_for_server()
    elif args['status']:
        status = model_server.status(config["constant.tfs_base_port"])
        print(f"Server Status: {status}")
    elif args['start_and_wait']:
        model_server.start()
        model_server.wait_for_server()

if __name__ == '__main__':
    main()
