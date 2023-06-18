import math

import torch
import torch.nn as nn

class LLMConfig():
    def __init__(
            self,
            n_vocab=50257, # total number of tokens in the vocabulary
            n_context=1024, # size of the context window (in number of tokens)
            n_embed=768, # embedding vector size
            n_heads=12): # number of attention heads

        self.cfg = {
            'n_vocab': n_vocab,
            'n_context': n_context,
            'n_embed': n_embed,
            'n_heads': n_heads,
        }

    def __call__(self):
        return self.cfg

    def get(self, attr):
        return self.cfg[attr]


class SimpleMultiHeadAttention(nn.Module):
    # A vanilla multi-head masked self-attention layer.
    def __init__(self, config):
        super().__init__()
        self.cfg = config
        self.n_heads = self.cfg()['n_heads'] # number of attention heads
        self.n_embed = self.cfg()['n_embed'] # embedding vector size
        self.n_context = self.cfg()['n_context'] # number of tokens in context window
        # self.resid_dropout = config['resid_dropout'] # probability of a nn element to be zeroed

        self.Wqkv = nn.Linear(self.n_embed, 3*self.n_embed, bias=False) # W^q, W^k and W^v matrices next to each other

    def forward(self, x):
        n_batch, n_context, n_embed = x.size()  # batch size, token sequence length, embedding dimensionality
        assert self.n_embed % self.n_heads == 0, 'incompatible head/embedding dimensions'
        assert self.n_embed == n_embed, 'incompatible head/embedding dimensions'
        assert self.n_context == n_context, 'incompatible head/embedding dimensions'

        # q = X * W^q , where X is of dim (n_context, n_embed) and W^q is (n_embed, n_embed)
        # (same for k = X * W^k, v = X * W^v)
        q,k,v = self.Wqkv(x).split(self.n_embed, dim=2)

        q = q.view(n_batch, n_context, self.n_heads, n_embed // self.n_heads).transpose(1,2) # (n_batch, n_heads, n_context, n_embed)
        k = k.view(n_batch, n_context, self.n_heads, n_embed // self.n_heads).transpose(1,2) # (n_batch, n_heads, n_context, n_embed)
        v = v.view(n_batch, n_context, self.n_heads, n_embed // self.n_heads).transpose(1,2) # (n_batch, n_heads, n_context, n_embed)

        qkt = q @ k.transpose(2, 3) / math.sqrt(self.n_embed)

        return q,k,v,qkt
