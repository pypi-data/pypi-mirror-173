"""
Jax integration.

Importing this module registers the Jax backend with `mlm.math`.
Without this, Jax tensors cannot be handled by `mlm.math` functions.

To make Jax the default backend, import `mlm.jax.flow`.
"""
from mlm import math as _math

from ._jax_backend import JaxBackend as _JaxBackend

JAX = _JaxBackend()
"""Backend for Jax operations."""

_math.backend.BACKENDS.append(JAX)

__all__ = [key for key in globals().keys() if not key.startswith('_')]
