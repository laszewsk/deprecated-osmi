from cloudmesh.common.FlatDict import FlatDict
import numpy as np

def unique_base_port(config):

    # if experiment.directive == "a100-dgx":
    #     d = 1
    # elif experiment.directive == 'v100':
    #     d = 2

    # experiment.batch = int(experiment.batch)
    # # 128
    # experiment.ngpus = int(experiment.ngpus)
    # # 4
    # experiment.concurrency = int(experiment.concurrency)
    # # 10
    # experiment.repeat = int(experiment.repeat)
    # # 10
    # id = experiment.repeat + experiment.concurrency*10 + experiment.ngpus*100 + np.log2(experiment.batch)*1000 # + d
    
    
    # gpu doesn't matter because different gpu => different machine
    ngpus = int(config["experiment.ngpus"])
    batch = int(np.log2(int(config["experiment.batch"])))
    concurrency = int(config["experiment.concurrency"])
    repeat = int(config["experiment.repeat"])
    id = (ngpus+1)*1000 + batch*100 + concurrency*10 + (repeat-1)*(ngpus+1)  
    # 57__
    # 47__
    # each repeat of the same experiment will use as much as 5 ports
    return id

# import threading

# class BaseManager:
#     def __init__(self, filename):
#         self.filename = filename
#         self.lock = threading.Lock()
#         with self.lock:
#             self.base = self.read_base()

#     def read_base(self):
#         with self.lock:
#             with open(self.filename, 'r') as f:
#                 lines = f.readlines()
#         return int(lines[0])

#     def write_base(self):
#         with self.lock:
#             with open(self.filename, 'w') as f:
#                 f.write(str(self.base))

#     def increment_base(self):
#         with self.lock:
#             self.base += 1
#             self.write_base()
#         return self.base