#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import torch

DEPTH = 4
BATCH_SIZE = 8
SEQ_LENGTH = 8
IMG_SIZE = 16
HIDDEN_SIZE = 8
NUM_CLASSES = 8

def check_equal(A, B):
    assert torch.allclose(A, B, rtol=1e-3, atol=1e-1) == True
