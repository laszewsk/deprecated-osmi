
from pprint import pprint
from cloudmesh.common.util import banner
from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.FlatDict import expand_config_parameters
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=True, help="yaml file with model_config_list")
args = vars(parser.parse_args())

config_file = args["config"]

banner(config_file)
# with open(config_file) as stream:
#     config = yaml.safe_load(stream)

config = FlatDict()
config.load(config_file, expand=True)
expand_config_parameters(flat=config, expand_yaml=True, expand_os=True, expand_cloudmesh=True)

# for key in ["concurrency", "batch", "nrequests", "ngpus", "ports"]:
#     config[f"experiment.{key}"] = int(config[f"experiment.{key}"])

model_config_list = {}
for key in config:
    print(key.split("."))
    temp = key.split(".")
    if len(temp) != 3:
        continue
    section,model,k = temp
    if section == "model_config_list":
        if model not in model_config_list:
            model_config_list[model] = {}
        model_config_list[model][k] = config[key]

pprint(model_config_list)

with open('new.conf', 'w+') as f:
    json.dump(model_config_list, f)