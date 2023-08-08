from cloudmesh.common.Shell import Shell
import time
import requests
# from docopt import docopt
import argparse
import os
import socket
from cloudmesh.common.FlatDict import FlatDict
from yaml_to_conf import YamlToJsonConverter

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", type=str,
                required=False,
                help="config file")
ap.add_argument("-p", "--port", type=int,
                required=True,
                help="base port for TF servers")
ap.add_argument("-g", "--ngpus", type=int,
                required=True,
                help="number of GPUs")
ap.add_argument("-o", "--output_dir", type=str,
                required=True,
                help="directory to store output logs")
ap.add_argument("-s", "--sif_dir", type=str,
                required=False,
                help="directory of the TF serving singularity image")
# exec dir is wrong, because cloudmesh dynamically cds into the directory
# ap.add_argument("-m", "--model_conf_base_name", type=str,
# required=False, help="model config file base name")
args = ap.parse_args()

config_filename = getattr(args, "config") or "config.yaml"
config = FlatDict()
config.load(filename=config_filename)
config["experiment.ngpus"] = int(config["experiment.ngpus"])

arg_to_config_mapping = {
    "tfs_base_port": "constant.tfs_base_port",
    "ngpus": "experiment.ngpus",
    "output_dir": "data.output",
    "sif_dir": "data.sif_dir",
}

for arg_key, config_key in arg_to_config_mapping.items():
    arg_value = getattr(args, arg_key)
    if arg_value is not None:
        config[config_key] = arg_value


class ModelServer:

    def __init__(self, config):
        self.tfs_base_port = config["constant.tfs_base_port"]
        self.ngpus = config["experiment.ngpus"]
        self.output_dir = config["data.output"]
        self.sif_dir = config["data.sif_dir"]
        self.batch = config["experiment.batch"]
        self.model_conf_file = self.convert_conf_to_json()

    def convert_conf_to_json(self):
        converter = YamlToJsonConverter(config_filename, "models")
        converter.convert()
        return converter.get_name()

    def start(self):
        # for device in self.visible_devices.split(','):
        for i in range(self.ngpus):
            port = self.tfs_base_port + i
            # print(f"time CUDA_VISIBLE_DEVICES={i} singularity exec --nv --home `pwd` \
            #     {self.exec_dir}/serving_latest-gpu.sif tensorflow_model_server \
            #     --port={port} --rest_api_port=0 --model_config_file={self.model_conf_file} \
            #     >& {self.output_dir}/v100-{port}.log &")
            command = f"time CUDA_VISIBLE_DEVICES={i} "\
                      f"singularity exec --nv --home `pwd` {self.sif_dir}/serving_latest-gpu.sif "\
                      f"tensorflow_model_server --port={port} --rest_api_port=0 --model_config_file={self.model_conf_file} "\
                      f">& {self.output_dir}/v100-{port}.log &"
            print(command)
            r = os.system(command)
            print(r)
            # Shell.run(f"time {self.visible_devices}={i} singularity exec --nv --home "
            # "`pwd` {self.exec_dir}/serving_latest-gpu.sif tensorflow_model_server --port={port} --rest_api_port=0 "
            # "--model_config_file={self.model_conf_file} >& {self.output_dir}/v100-{port}.log &")

    def shutdown(self):
        raise NotImplementedError

    def status(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex(('127.0.0.1', port)) == 0

    def wait_for_server(self):
        start = time.time()
        while not all([self.status(p + self.tfs_base_port) for p in range(self.ngpus)]):
            if time.time() - start > 45:
                print("Server not properly started")
                raise ValueError("Server not properly started")
            time.sleep(0.5)
            print(".", end="")
        print()


def main():
    # print(args)
    model_server = ModelServer(port=args["port"], ngpus=args["ngpus"], output_dir=args["output_dir"], exec_dir=args["exec_dir"],
                               model_conf_file=args["model_conf_file"])
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

    for j in `seq 0 $(($ngpus_PER_NODE-1))`
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
        for PORT in `seq $PORT_TF_SERVER $(($PORT_TF_SERVER+$ngpus_PER_NODE-1))`; do
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

# def __init__(self, port, ngpus, output_dir, exec_dir=None, model_conf_file=None):
#     self.visible_devices = os.getenv("CUDA_VISIBLE_DEVICES")
#     self.tfs_base_port = port
#     self.output_dir = output_dir
#     self.ngpus = ngpus
#     if exec_dir is None:
#         self.exec_dir = os.getcwd()
#     else:
#         self.exec_dir = exec_dir
#     if model_conf_file is None:
#         self.model_conf_file = "models.conf"
#     else:
#         converter = YamlToJsonConverter("models")
#         converter.convert()
#         self.model_conf_file = converter.get_name()
