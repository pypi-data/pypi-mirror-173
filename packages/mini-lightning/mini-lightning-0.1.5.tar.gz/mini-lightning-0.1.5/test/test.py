from torchmetrics.functional import pairwise_cosine_similarity
import torch
import mini_lightning as ml

from libs import *

model = nn.Linear(10, 10).cuda()
ckpt_fpath = "./asset/1.ckpt"
torch.save(model.state_dict(), ckpt_fpath)
a = torch.load(ckpt_fpath, map_location=Device("cpu"))
b = torch.load(ckpt_fpath)
print(a)
print(b)

x = torch.tensor([[2, 3], [3, 5], [5, 8]], dtype=torch.float32)
y = torch.tensor([[1, 0], [2, 1]], dtype=torch.float32)
print("Result:", pairwise_cosine_similarity(x, y))
print("X:", x)
print("Y:", y)
"""Out[0]
Result: tensor([[0.5547, 0.8682],
        [0.5145, 0.8437],
        [0.5300, 0.8533]])
X: tensor([[0.5547, 0.8321],
        [0.5145, 0.8575],
        [0.5300, 0.8480]])
Y: tensor([[1.0000, 0.0000],
        [0.8944, 0.4472]])
"""
