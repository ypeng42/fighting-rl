
import os
import torch
import torch.distributed as dist

dist.init_process_group("gloo")
rank = dist.get_rank()

if rank == 0:
    x = torch.tensor([2.0])
    dist.send(x, dst=1)

    result = torch.empty(1)
    dist.recv(result, src=1)
    print(f"Rank 0: received {result.item()}", flush=True)

else:
    y = torch.tensor([4.0])
    x = torch.empty(1)

    dist.recv(x, src=0)
    result = x + y
    dist.send(result, dst=0)
    print(f"Rank 1: computed {result.item()}", flush=True)

dist.destroy_process_group()
