"""
PyTorch integration.

Importing this module registers the PyTorch backend with `mlm.math`.
Without this, PyTorch tensors cannot be handled by `mlm.math` functions.

To make PyTorch the default backend, import `mlm.torch.flow`.
"""
from mlm import math as _math
from ._torch_backend import TorchBackend as _TorchBackend

TORCH = _TorchBackend()
""" Backend for PyTorch operations. """

_math.backend.BACKENDS.append(TORCH)

__all__ = [key for key in globals().keys() if not key.startswith('_')]
