from pprint import pprint
import json
from cloudmesh.common.util import banner
from cloudmesh.common.FlatDict import FlatDict, expand_config_parameters
import os


class YamlToJsonConverter:

    def __init__(self, config_file, base_name="models"):
        self.config_file = config_file
        pid = os.getpid()
        self.json_file = f"{base_name}_{pid}.conf"
        self.config = None
        self.model_config_list = None

    def _load_config_from_yaml(self):
        """
        Load configuration from a YAML file and expand its parameters.
        """
        config = FlatDict()
        config.load(self.config_file, expand=True)
        expand_config_parameters(flat=config, expand_yaml=True, expand_os=True, expand_cloudmesh=True)
        self.config = config

    def _extract_model_config_list(self):
        """
        Extract the 'model_config_list' section from the configuration.
        """
        model_config_list = {}

        for key in self.config:
            parts = key.split(".")
            if len(parts) != 3:
                continue
            section, model, k = parts
            if section == "model_config_list":
                if model not in model_config_list:
                    model_config_list[model] = {}
                model_config_list[model][k] = self.config[key]

        self.model_config_list = model_config_list

    def _save_to_json(self):
        """
        Save data to a JSON file.
        """
        with open(self.json_file, 'w+') as f:
            json.dump(self.model_config_list, f)

    def convert(self):
        banner(self.config_file)
        self._load_config_from_yaml()
        self._extract_model_config_list()
        pprint(self.model_config_list)
        self._save_to_json()

    def get_name(self):
        return self.json_file


if __name__ == "__main__":
    converter = YamlToJsonConverter("path_to_config.yaml")
    converter.convert()

# from pprint import pprint
# from cloudmesh.common.util import banner
# from cloudmesh.common.FlatDict import FlatDict
# from cloudmesh.common.FlatDict import expand_config_parameters
# import json

# def yaml_to_json(config_file, json_file="models.conf"):
#     banner(config_file)
#     # with open(config_file) as stream:
#     #     config = yaml.safe_load(stream)

#     config = FlatDict()
#     config.load(config_file, expand=True)
#     expand_config_parameters(flat=config, expand_yaml=True, expand_os=True, expand_cloudmesh=True)

#     # for key in ["concurrency", "batch", "nrequests", "ngpus", "ports"]:
#     #     config[f"experiment.{key}"] = int(config[f"experiment.{key}"])

#     model_config_list = {}
#     for key in config:
#         print(key.split("."))
#         temp = key.split(".")
#         if len(temp) != 3:
#             continue
#         section,model,k = temp
#         if section == "model_config_list":
#             if model not in model_config_list:
#                 model_config_list[model] = {}
#             model_config_list[model][k] = config[key]

#     pprint(model_config_list)

#     with open(json_file, 'w+') as f:
#         json.dump(model_config_list, f)
