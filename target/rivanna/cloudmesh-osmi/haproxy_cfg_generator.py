import yaml
from docopt import docopt

class YAMLToHAProxyConverter:
    def __init__(self, yaml_file_path, output_file_path):
        self.yaml_file_path = yaml_file_path
        self.output_file_path = output_file_path

    def generate_cfg_lines(self, data, indent_level=0):
        cfg_lines = []

        for key, value in data.items():
            if isinstance(value, dict):
                cfg_lines.append('  ' * indent_level + f"{key}:")
                cfg_lines.extend(self.generate_cfg_lines(value, indent_level + 1))
            elif isinstance(value, list):
                cfg_lines.append('  ' * indent_level + f"{key}:")
                for item in value:
                    cfg_lines.append('  ' * (indent_level + 1) + f"- {item}")
            else:
                cfg_lines.append('  ' * indent_level + f"{key}: {value}")

        return cfg_lines

    def convert(self):
        with open(self.yaml_file_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        cfg_lines = self.generate_cfg_lines(yaml_data['haproxy'])

        with open(self.output_file_path, 'w') as output_file:
            output_file.write('\n'.join(cfg_lines))

if __name__ == "__main__":
    usage = """
    YAML to HAProxy Converter
    
    Usage:
      yaml_to_haproxy.py INPUT_YAML OUTPUT_CFG
      yaml_to_haproxy.py -h | --help
      
    Options:
      -h --help     Show this help message and exit.
    """
    
    arguments = docopt(usage)
    
    input_yaml = arguments['INPUT_YAML']
    output_cfg = arguments['OUTPUT_CFG']
    
    converter = YAMLToHAProxyConverter(input_yaml, output_cfg)
    converter.convert()

    



    input_yaml = """
    haproxy:
      global:
        log:
          - /dev/log local0
          - /dev/log local1 notice
        chroot: /var/lib/haproxy
        stats socket: /run/haproxy/admin.sock mode 660 level admin
        stats timeout: 30s

      defaults:
        log: global
        mode: http
        option:
          - httplog
          - dontlognull
        timeout:
          connect: 5000
          client: 50000
          server: 50000

      frontend http_front:
        bind: *
    """
