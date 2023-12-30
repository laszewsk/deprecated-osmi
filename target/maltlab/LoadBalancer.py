"""
LoadBalancer

Usage:
  LoadBalancer.py start_and_wait  [--config=CONFIG]
                                  [--haproxy_port=PORT]
                                  [--output_dir=OUTPUT]
                                  [--haproxy_sif=IMAGE]
                                  [--timeout=TIMEOUT]
                                  [--tfs_base_port=BASE_PORT]
                                  [--ngpus=NGPUS]
                                  [--haproxy_cfg_file=HAPROXY_CFG_FILE]
                                  [--server=<server>]
  LoadBalancer.py start  [--config=CONFIG]
                         [--haproxy_port=PORT]
                         [--output_dir=OUTPUT]
                         [--haproxy_sif=IMAGE]
  LoadBalancer.py wait [--config=CONFIG]
  LoadBalancer.py (-h | --help)

Options:
  -h --help             Show this screen.
  --config=CONFIG       Model config file.
  --haproxy_port=PORT   Port for haproxy server.
  --output_dir=OUTPUT   Directory to store output logs.
  --haproxy_sif=IMAGE   HAProxy apptainer image.
"""

import os
import socket
import time

from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.Shell import Shell
from docopt import docopt
# from port_generator import unique_base_port
from cloudmesh.common.network import PortGenerator

from haproxy_cfg_generator import generate_haproxy_cfg

APPTAINER = "apptainer exec --bind `pwd`:/home --pwd /home"

class HAProxyLoadBalancer:

    def __init__(self, config):
        """
        Initializes a LoadBalancer object.

        Parameters:
            config (dict): A dictionary containing configuration information.

        Attributes:
            port (int): The unique base port for the LoadBalancer.
            output_dir (str): The output directory for the LoadBalancer.
            haproxy_config_file (str): The path to the HAProxy configuration file.
            haproxy_sif (str): The path to the HAProxy SIF file.
        """

        p = PortGenerator(config["constant.haproxy_port"])
        self.port = p.get_port()
        self.output_dir = config["data.output"]
        generate_haproxy_cfg(config)
        self.haproxy_config_file = config["data.haproxy_cfg_file"]
        self.haproxy_sif = config["data.haproxy_sif"]

    def start(self):
        """
        Starts the load balancer by executing the haproxy command.

        Returns:
            int: The return code of the executed command.
        """
        command = f"time {APPTAINER} {self.haproxy_sif} " \
                  f"haproxy -d -f {self.haproxy_config_file} > {self.output_dir}/haproxy.log 2>&1 &"
        print(command)
        r = Shell.run(command)
        print(r)
        print('that was the shell.run ^')

    def shutdown(self):
        """
        Not implemented. Shuts down the load balancer.
        """
        raise NotImplementedError

    def status(self, port):
        """
        Check the status of a port on the local machine.

        Parameters:
            port (int): The port number to check.

        Returns:
            bool: True if the port is open, False otherwise.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex(('127.0.0.1', port)) == 0

    def wait_for_server(self):
            """
            Waits for the server to start by continuously checking its status.
            
            Raises:
                ValueError: If the load balancer is not properly started within 45 seconds.
            """
            start = time.time()
            while not self.status(self.port):
                if time.time() - start > 45:
                    raise ValueError("Load balancer not properly started")
                time.sleep(0.5)
                print(".", end="")
            print()


def main():
    """
    Entry point of the LoadBalancer program.
    
    This function parses command line arguments, loads the configuration file,
    maps the command line arguments to the corresponding configuration keys,
    and starts or waits for the load balancer based on the provided arguments.
    """
    
    args = docopt(__doc__)

    config_file = args["--config"] or "config.yaml"
    config = FlatDict()
    config.load(config_file, expand=True)

    arg_to_config_mapping = {
        "--haproxy_port": "constant.haproxy_port",
        "--haproxy_sif": "data.haproxy_sif",
        "--output_dir": "data.output",
        "--tfs_base_port": "constant.tfs_base_port",
        "--ngpus": "experiment.ngpus",
        "--haproxy_cfg_file": "data.haproxy_cfg_file",
        "--server": "constant.server",
    }

    for arg_key, config_key in arg_to_config_mapping.items():
        if args[arg_key]:
            config[config_key] = args[arg_key]

    config["experiment.ngpus"] = int(config["experiment.ngpus"])

    load_balancer = HAProxyLoadBalancer(config)
    if args["start"]:
        load_balancer.start()
    elif args["wait"]:
        load_balancer.wait_for_server()
    elif args["start_and_wait"]:
        load_balancer.start()
        load_balancer.wait_for_server()

if __name__ == '__main__':
    main()
