"""
HAProxy Config Generator

Usage:
  haproxy_cfg_generate.py --config=CONFIG
                         [--port=PORT]
                         [--ngpus=NGPUS]
                         [--server=SERVER]
                         [--haproxy_cfg_file=HAPROXY_CFG_FILE]
  haproxy_cfg_generate.py (-h | --help)

Options:
  -h --help                            Show this screen.
  --config=CONFIG                      Config file.
  --port=<port>                        Base port for TF servers.
  --ngpus=NGPUS                        Number of GPUs.
  --server=SERVER                      Server IP.
  --haproxy_cfg_file=HAPROXY_CFG_FILE  Name of file to store haproxy config file.
"""

from cloudmesh.common.util import banner
from cloudmesh.common.FlatDict import FlatDict
from docopt import docopt
from port_generator import unique_base_port
from textwrap import dedent

def generate_haproxy_cfg(config):
  """
  Generate HAProxy configuration file based on the provided config.

  Args:
    config (dict): Configuration parameters for generating the HAProxy configuration.

  Returns:
    None
  """
  
  port = unique_base_port(config)
  print(f'Port number: {port}')
  base = dedent(f'''
    global
      tune.ssl.default-dh-param 1024
    
    defaults
      timeout connect 10000ms
      timeout client 60000ms
      timeout server 60000ms
    
    frontend fe_https
      mode tcp
      bind *:{port:04d} npn spdy/2 alpn h2,http/1.1
      default_backend be_grpc
  
    backend be_grpc
      mode tcp
      balance roundrobin
  ''').strip()
  with open(config["data.haproxy_cfg_file"], 'w+') as f:
    f.write(base)
    for i in range(config["experiment.ngpus"]):
      f.write(f"  server tfs{i} {config['constant.server']}:{port+1+i:04d}\n")

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
