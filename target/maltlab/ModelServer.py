"""
Usage:
  ModelServer.py start_and_wait [--config=CONFIG]
                                [--port=PORT]
                                [--ngpus=<NGPUS]
                                [--output_dir=OUTPUT_DIR]
                                [--tfs_sif=TFS_SIF]
  ModelServer.py start [--config=CONFIG]
                       [--port=PORT]
                       [--ngpus=<NGPUS]
                       [--output_dir=OUTPUT_DIR]
                       [--tfs_sif=TFS_SIF]
  ModelServer.py wait [---config=CONFIG]
                      [--timeout=TIMEOUT]
  ModelServer.py status [--port=PORT]
  ModelServer.py (-h | --help)

Options:
    --config=CONFIG          Config file [default: config.yaml].
    --port=PORT              Base port for TF servers.
    --ngpus=<NGPUS           Number of GPUs.
    --output_dir=OUTPUT_DIR  Directory to store output logs.
    --tfs_sif=TFS_SIF        Tensorflow serving apptainer image.
    --status=STATUS          Server status (for wait command).
    --timeout=TIMEOUT        Timeout (for wait command).
    -h --help                Show this screen.
"""

from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.Shell import Shell
from yaml_to_conf import YamlToJsonConverter
import subprocess
import socket
import time
from docopt import docopt
from pprint import pprint
from port_generator import unique_base_port
import os
# from cloudmesh.common.network import PortGenerator


# APPTAINER = []

class ModelServer:

    def __init__(self, config, config_filename=None):
        """
        Initializes the ModelServer object.

        Parameters:
        - config (dict): Configuration dictionary containing various parameters.
        - config_filename (str): Optional filename of the configuration file.

        """
        # p = PortGenerator(config["constant.tfs_base_port"] - 1)
        # self.tfs_base_port = p.get_port() + 1
        self.tfs_base_port = unique_base_port(config) + 1
        self.ngpus = config["experiment.ngpus"]
        self.output_dir = config["data.output"]
        self.batch = config["experiment.batch"]
        self.tfs_sif = config["data.tfs_sif"]
        self.timeout = config["constant.timeout"]
        self.model_conf_file = self.convert_conf_to_json(config_filename)
        self.MACHINE = "maltlab"



    def convert_conf_to_json(self, config_filename):
        """
        Converts a YAML configuration file to JSON format.

        Parameters:
            config_filename (str): The path to the YAML configuration file.

        Returns:
            str: The name of the converted JSON file.
        """
        converter = YamlToJsonConverter(config_filename, "models")
        converter.convert()
        return converter.get_name()

    def start(self):
            """
            Starts the ModelServer by executing the TensorFlow Serving command for each GPU.
            """
            
            StopWatch.event("ModelServer: start")
            banner("LS")
            result = subprocess.run('ls', shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)

            banner("PWD")           
            mypwd = subprocess.run('pwd', shell=True, check=True, capture_output=True, text=True)
            mypwd = mypwd.stdout.strip()
            print (mypwd)
            
            for i in range(self.ngpus):
                port = self.tfs_base_port + i
                if self.MACHINE == "maltlab":
                    command = [
                            # "CUDA_VISIBLE_DEVICES=" + str(i),
                            "apptainer", "exec", 
                            f"--bind={mypwd}:/home", "--pwd=/home", 
                            "--bind=/mnt/hdd/jpf:/mnt/hdd/jpf",
                            self.tfs_sif,
                            "tensorflow_model_server", 
                            f"--port={port:04d}", "--rest_api_port=0",
                            f"--model_config_file={self.model_conf_file}",
                            
                        ]
                        #   f"tensorflow_model_server --port={port:04d} --rest_api_port=0 --model_config_file={self.model_conf_file} "\
                        #   f">& {self.output_dir}/v100-{port:04d}.log &\""
                elif self.MACHINE == "rivanna":
                    command = f"time CUDA_VISIBLE_DEVICES={i} "\
                          f"{APPTAINER} {self.tfs_sif} "\
                          f"tensorflow_model_server --port={port:04d} --rest_api_port=0 --model_config_file={self.model_conf_file} "\
                          f">& {self.output_dir}/v100-{port:04d}.log &"
                # command = " ".join(command)
                print(" ".join(command))
                r = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                print('subprocess start above')
    
    def shutdown(self):
        """
        Not implemented. Shuts down the model server.
        """
        raise NotImplementedError

    def status(self, port):
        """
        Check the status of the ModelServer.

        Parameters:
            port (int): The port number to check the status on.

        Returns:
            bool: True if the ModelServer is running on the specified port, False otherwise.
        """
        StopWatch.event("ModelServer: status")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex(('127.0.0.1', port)) == 0

    def wait_for_server(self, wait_time=0.5):
        """
        Waits for the model server to start up.

        This method continuously checks the status of the model server until the server is up.
        If the server does not start within the specified timeout, a ValueError is raised.

        Args:
            wait_time (float): The time interval between each status check (default is 0.5 seconds)

        Raises:
            ValueError: If the model server does not start within the specified timeout

        Returns:
            None
        """
        StopWatch.event("ModelServer: wait for server")
        start = time.time()
        while not all([self.status(p + self.tfs_base_port) for p in range(self.ngpus)]):
            if time.time() - start > self.timeout:
                print("Server not properly started")
                raise ValueError("Model server not properly started")
            time.sleep(wait_time)
            print(".", end="")
        StopWatch.event("ModelServer: server up")
        print()


def main():
    """
    Entry point of the ModelServer program.
    
    Parses command line arguments, loads configuration, and starts the 
    ModelServer based on the provided arguments.
    """

    args = docopt(__doc__)
    pprint(args)
    config_filename = args["--config"] or "config.yaml"
    config = FlatDict()
    config.load(content=config_filename, expand=True)
    config["experiment.ngpus"] = int(config["experiment.ngpus"])
    # if debug:
    print("ModelServer:", config)

    arg_to_config_mapping = {
        "--port": "constant.tfs_base_port",
        "--ngpus": "experiment.ngpus",
        "--output_dir": "data.output",
        "--tfs_sif": "data.tfs_sif",
        "--timeout": "constant.timeout",
    }

    for arg_key, config_key in arg_to_config_mapping.items():
        arg_value = args[arg_key]
        banner(f"arg_key: {arg_key}, config_key: {config_key}, arg_value: {arg_value}")
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
