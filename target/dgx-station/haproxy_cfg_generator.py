"""
HAProxy Config Generator

Usage:
  generate_config.py (-c <config> | --config=<config>) [-p <port>] [-g <ngpus>] [-s <server>] [-o <haproxy_cfg_file>]
  generate_config.py (-h | --help)

Options:
  -h --help                              Show this screen.
  -c <config> --config=<config>          Config file.
  -p <port> --port=<port>                Base port for TF servers.
  -g <ngpus> --ngpus=<ngpus>             Number of GPUs.
  -s <server> --server=<server>          Server IP.
  -o <haproxy_cfg_file> --haproxy_cfg_file=<haproxy_cfg_file>  Name of file to store haproxy config file.
"""

from cloudmesh.common.util import banner
from cloudmesh.common.FlatDict import FlatDict
from docopt import docopt

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

def generate_haproxy_cfg(config):
    with open(config["data.haproxy_cfg_file"], 'w+') as f:
        f.write(base)
        for i in range(config["experiment.ngpus"]):
            f.write(f"  server tfs{i} {config['constant.server']}:{config['constant.tfs_base_port']+i}\n")

if __name__ == "__main__":
  args = docopt(__doc__)

  config = FlatDict()
  if args["--config"] is not None:
      config.load(content=open(args["--config"]), expand=True)

  arg_to_config_mapping = {
      "--port": "constant.tfs_base_port",
      "--ngpus": "experiment.ngpus",
      "--haproxy_cfg_file": "data.haproxy_cfg_file",
      "--server": "constant.server",
  }

  for arg_key, config_key in arg_to_config_mapping.items():
      if args[arg_key]:
          config[config_key] = args[arg_key]

  config["experiment.ngpus"] = int(config["experiment.ngpus"])
  generate_haproxy_cfg(config)
