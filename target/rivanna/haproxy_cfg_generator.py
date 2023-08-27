from pprint import pprint
import json
from cloudmesh.common.util import banner
from cloudmesh.common.FlatDict import FlatDict, expand_config_parameters
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", type=str,
                help="config file")
ap.add_argument("-p", "--port", type=int,
                help="base port for TF servers")
ap.add_argument("-g", "--ngpus", type=int,
                help="number of GPUs")
ap.add_argument("-s", "--server", type=str,
                help="server ip")
ap.add_argument("-o", "--haproxy_cfg_file", type=str,
                help="name of file to store haproxy config file")

args = ap.parse_args()

config_filename = getattr(args, "config")
config = FlatDict()
if config_filename is not None:
  config.load(content=config_filename, expand=True)

arg_to_config_mapping = {
    "port": "constant.tfs_base_port",
    "ngpus": "experiment.ngpus",
    "haproxy_cfg_file": "data.haproxy_cfg_file",
    "server": "constant.server",
}

for arg_key, config_key in arg_to_config_mapping.items():
    arg_value = getattr(args, arg_key)
    if arg_value is not None:
        config[config_key] = arg_value

config["experiment.ngpus"] = int(config["experiment.ngpus"])

base = '''
global
  tune.ssl.default-dh-param 1024
 
defaults
  timeout connect 10000ms
  timeout client 60000ms
  timeout server 60000ms
 
frontend fe_https
  mode tcp
  bind *:8443 npn spdy/2 alpn h2,http/1.1
  default_backend be_grpc

backend be_grpc
  mode tcp
  balance roundrobin
'''

def generate_haproxy_cfg():  
  with open(config["data.haproxy_cfg_file"], 'w+') as f:
      f.write(base)
      for i in range(config["experiment.ngpus"]):
          f.write(f"  server tfs{i} {config['constant.server']}:{config['constant.tfs_base_port']+i}\n")

if __name__ == "__main__":
  generate_haproxy_cfg()