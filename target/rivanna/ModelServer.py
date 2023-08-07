from cloudmesh.common.Shell import Shell
import time
import requests
# from docopt import docopt
import argparse
import os
import socket
from cloudmesh.common.FlatDict import FlatDict
import yaml_to_conf

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", type=str, required=False, help="config file")
ap.add_argument("-p", "--port_tf_server_base", type=int, required=True, help="base port for TF servers")
ap.add_argument("-g", "--num_gpus", type=int, required=True, help="number of GPUs")
ap.add_argument("-o", "--output_dir", type=str, required=True, help="directory to store output logs")
ap.add_argument("-e", "--exec_dir", type=str, required=False, help="directory of the TF serving singularity image")
ap.add_argument("-m", "--model_base_name", type=str, required=False, help="model config file")
# replace with yaml and get conf from yaml
args = ap.parse_args()

config_filename = args.config or "config.yaml"
config = FlatDict()
config.load(filename=config_filename)
# construct the argument parse and parse the arguments

arg_to_config_mapping = {
    "port_tf_server_base": "port_tf_server_base",
    "num_gpus": "num_gpus",
    "output_dir": "output_dir",
    "exec_dir": "exec_dir",
    "model_conf_file": "model_conf_file",
    "repeat_no": "repeat_no"
}

for arg_key, config_key in arg_to_config_mapping.items():
    arg_value = getattr(args, arg_key)
    if arg_value is not None:
        config[config_key] = arg_value

class ModelServer:

    def __init__(self, port_tf_server_base, num_gpus, output_dir, exec_dir=None, model_conf_file=None, repeat_no=None):
        self.visible_devices = os.getenv("CUDA_VISIBLE_DEVICES")
        self.port_tf_server = port_tf_server_base
        self.output_dir = output_dir
        if repeat_no is not None:
            self.port_tf_server += repeat_no
        if model_conf_file is None:
            self.model_conf_file = "models.conf"
        else:
            self.model_conf_file = model_conf_file
        self.num_gpus = num_gpus
        if exec_dir is None:
            self.exec_dir = os.getcwd()
        else:
            self.exec_dir = exec_dir

    def start(self):
        # for device in self.visible_devices.split(','):
        for i in range(self.num_gpus):
            port = self.port_tf_server + i
            # print(f"time CUDA_VISIBLE_DEVICES={i} singularity exec --nv --home `pwd` \
            #     {self.exec_dir}/serving_latest-gpu.sif tensorflow_model_server \
            #     --port={port} --rest_api_port=0 --model_config_file={self.model_conf_file} \
            #     >& {self.output_dir}/v100-{port}.log &")
            command = f"time {self.visible_devices}={i} singularity exec --nv --home `pwd` {self.exec_dir}/serving_latest-gpu.sif tensorflow_model_server --port={port} --rest_api_port=0 --model_config_file={self.model_conf_file} >& {self.output_dir}/v100-{port}.log &"
            print(command)
            r = os.system(command)
            print(r)
            # Shell.run(f"time {self.visible_devices}={i} singularity exec --nv --home `pwd` {self.exec_dir}/serving_latest-gpu.sif tensorflow_model_server --port={port} --rest_api_port=0 --model_config_file={self.model_conf_file} >& {self.output_dir}/v100-{port}.log &")

    def shutdown(self):
        raise NotImplementedError

    def status(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex(('127.0.0.1',port)) == 0
    
    def wait_for_server(self):
        start = time.time()
        while not all([self.status(p+self.port_tf_server) for p in range(self.num_gpus)]):
            if time.time() - start > 45:
                print("Server not properly started")
                raise ValueError("Server not properly started")
            time.sleep(0.5)
            print(".", end="")
        print()
            
def main():
    # print(args)
    model_server = ModelServer(port_tf_server_base=args["port_tf_server_base"], num_gpus=args["num_gpus"], output_dir=args["output_dir"], exec_dir=args["exec_dir"], model_conf_file=args["model_conf_file"])
    model_server.start()
    model_server.wait_for_server()

# python ModelServer.py --port=8500 -g=2 -o=../../osmi-output

if __name__ == '__main__':
    main()
    
"""
    
start_tf_servers() {

    source ???/ENV3
    
    python ModelServer.py start # docopts, click
    python ModelServer.py wait status=up timeout=5min  # humanize
    python ModelServer.py status 

    for j in `seq 0 $(($NUM_GPUS_PER_NODE-1))`
    do
        PORT=$(($PORT_TF_SERVER+$j))
        time CUDA_VISIBLE_DEVICES=$j singularity exec --nv --home `pwd` $EXEC_DIR/serving_latest-gpu.sif tensorflow_model_server --port=$PORT --rest_api_port=0 --model_config_file=models.conf >& $OUTPUT_DIR/v100-$PORT.log &
    done

    # time CUDA_VISIBLE_DEVICES=1 singularity exec --nv --home `pwd` $EXEC_DIR/serving_latest-gpu.sif tensorflow_model_server --port=8501 --rest_api_port=0 --model_config_file=models.conf >& $OUTPUT_DIR/v100-8501.log &
    echo "# cloudmesh status=running progress=45 pid=$$"
    start_wait_for_server=`date +%s`
    echo start_wait_for_server $start_wait_for_server

    # for sec in $(seq -w 10000 -1 1); do
    #     if [[ $(lsof -i :8500) && $(lsof -i :8501) ]]; then break; fi
    #     sleep 0.5
    #     echo "-"
    # done
    for sec in $(seq -w 10000 -1 1); do
        valid=1
        for PORT in `seq $PORT_TF_SERVER $(($PORT_TF_SERVER+$NUM_GPUS_PER_NODE-1))`; do
            if ! [[ $(lsof -i :$PORT) ]]; then
                valid=0;
                break;
            fi
        done
        if [ $valid = 1 ]; then break; fi;
        sleep 0.5
        echo "-"
    done

    end_wait_for_server=`date +%s`
    echo "server up"
    echo end_wait_for_server $end_wait_for_server
    time_server_wait=$((end_wait_for_server-start_wait_for_server))
    echo time_server_wait $time_server_wait
}
    """