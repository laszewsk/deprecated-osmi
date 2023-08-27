#python -m unittest test_yaml_to_haproxy.py

import unittest
from io import StringIO
from yaml_to_haproxy import YAMLToHAProxyConverter

class TestYAMLToHAProxyConverter(unittest.TestCase):
    def test_convert(self):
        input_yaml = """
        haproxy:
          global:
            log:
              - /dev/log local0
            chroot: /var/lib/haproxy
            stats socket: /run/haproxy/admin.sock mode 660 level admin
            stats timeout: 30s

          defaults:
            log: global
            mode: http
            option:
              - httplog
            timeout:
              connect: 5000
              client: 50000
              server: 50000
        """
        expected_output = [
            "haproxy:",
            "  global:",
            "    log:",
            "      - /dev/log local0",
            "    chroot: /var/lib/haproxy",
            "    stats socket: /run/haproxy/admin.sock mode 660 level admin",
            "    stats timeout: 30s",
            "  defaults:",
            "    log: global",
            "    mode: http",
            "    option:",
            "      - httplog",
            "    timeout:",
            "      connect: 5000",
            "      client: 50000",
            "      server: 50000"
        ]

        input_yaml_file = StringIO(input_yaml)
        output_cfg_file = StringIO()
        
        converter = YAMLToHAProxyConverter(input_yaml_file, output_cfg_file)
        converter.convert()

        output_cfg_lines = output_cfg_file.getvalue().strip().split('\n')
        
        self.assertEqual(output_cfg_lines, expected_output)

if __name__ == '__main__':
    unittest.main()



