import torch
from gpt import SimpleMultiHeadAttention as SMHA
from gpt import LLMConfig as Cfg

# batch size, token sequence length, embedding dimensionality
vocab_size=10
n_batch = 3
n_context = 5
n_embed = 6
n_heads=3

cfg = Cfg(
    n_vocab=vocab_size,
    n_context=n_context,
    n_embed=n_embed,
    n_heads=n_heads
    )

ssa = SMHA(cfg)

x = torch.randn((n_batch, n_context, n_embed))

q,k,v = ssa(x)

print(q.shape, k.shape, v.shape)




