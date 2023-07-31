from cloudmesh.common.Shell import Shell
import time
import requests
# from docopt import docopt
import argparse
import os
import socket

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port_ha_proxy_base", type=int, required=True, help="base port for TF servers")
ap.add_argument("-o", "--output_dir", type=str, required=True, help="directory to store output logs")
ap.add_argument("-c", "--config_file", type=str, required=True, help="model config file")
ap.add_argument("-e", "--exec_dir", type=str, required=False, help="directory of the TF serving singularity image")
ap.add_argument("-r", "--repeat_no", type=int, required=False, help="repeat number")
# replace with yaml and get conf from yaml
args = vars(ap.parse_args())

class HAProxyLoadBalancer:

    def __init__(self, port_ha_proxy, output_dir, config_file, exec_dir=None, repeat_no=None):
        self.visible_devices = os.getenv("CUDA_VISIBLE_DEVICES")
        self.port = port_ha_proxy
        self.output_dir = output_dir
        if repeat_no is not None:
            self.port += repeat_no
        self.config_file = config_file
        if exec_dir is None:
            self.exec_dir = os.getcwd()
        else:
            self.exec_dir = exec_dir

    def start(self):
        command = f"time singularity exec --bind `pwd`:/home --pwd /home {self.exec_dir}/haproxy_latest.sif \
                        haproxy -d -f {self.config_file} >& {self.output_dir}haproxy.log &"
        Shell.run(command)

    def shutdown(self):
        raise NotImplementedError

    def status(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex(('127.0.0.1',port)) == 0
    
    def wait_for_server(self):
        start = time.time()
        while not self.status(self.port):
            if time.time() - start > 45:
                raise ValueError("Server not properly started")
            time.sleep(0.5)
            print(".", end="")
        print()
            
def main():
    print(args)
    model_server = HAProxyLoadBalancer(port_ha_proxy=args["port_ha_proxy_base"], output_dir=args["output_dir"], exec_dir=args["exec_dir"], config_file=args["config_file"], repeat_no=args["repeat_no"])
    model_server.start()
    model_server.wait_for_server()

# python LoadBalancer.py -p 8443 -o ../../osmi-output/ -c haproxy-grpc.cfg 

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