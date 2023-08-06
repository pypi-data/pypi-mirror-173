import dask
import distributed
#dask.config.set({"distributed.comm.timeouts.tcp": "50s"})

import dask.array as da
from dask.distributed import Client, LocalCluster

from scipy.linalg import svd
'''
dask-scheduler
dask-worker --memory-limit 2G --nprocs 2 --nthreads 2 127.0.0.1:8786
'''
if __name__=="__main__":
    cluster = LocalCluster(n_workers=2, threads_per_worker=1, memory_limit="4G")
    print(cluster)
    client = Client(cluster) # Client('127.0.0.1:8786')  # set up local cluster on your laptop
    print(client)

    x = da.random.random(size=(20_000, 20_000), chunks=(1_000, 1_000))

    u, s, v = da.linalg.svd_compressed(x, k=5000, compute=True)
    
    # u, s, v = svd(x, full_matrices=True)
    print(s.compute())
    print(v.compute())
