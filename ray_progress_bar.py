import ray
import numpy as np
from tqdm import tqdm


class SomeCalculator():
    
    def __init__(self, ray_cpus):
        self._ndata = 1000
        ray.init(num_cpus=ray_cpus, log_to_driver=False)
        self._calculate()
        ray.shutdown()
        print(f'results: {self._results}')
        
    def _calculate(self):
        obj_ids = [
                calculate_remote.remote(
                    input_a, input_b
                )
                for input_a, input_b in zip(
                    np.random.randn(self._ndata),
                    np.random.randn(self._ndata)*2
                )
            ]
        self._results = [
            x for x in tqdm(to_iterator(obj_ids), total=len(obj_ids))
        ]    
        self._results = np.sum(self._results)

def to_iterator(obj_ids):
    while obj_ids:
        done, obj_ids = ray.wait(obj_ids)
        yield ray.get(done[0])

@ ray.remote
def calculate_remote(input_a, input_b):
    return calculate(input_a, input_b)

def calculate(input_a, input_b) -> float:
    return input_a + input_b
    
if __name__ == '__main__':
    calculation = SomeCalculator(2)
