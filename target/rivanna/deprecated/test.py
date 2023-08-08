from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.FlatDict import expand_config_parameters

from pprint import pprint

config = FlatDict()

config.load("osmi.in.yaml", expand=True)

pprint (dict(config))
expand_config_parameters(flat=config, expand_yaml=True, expand_os=True, expand_cloudmesh=True)

print ("TTTT")
pprint (dict(config))

