"""
neuralnet/tfuncts.py: some of the most common transfer functions
                      for neuralnetworks.
"""
from __future__ import division
from math import e, tanh


#HYPERBOLIC TANGENT
def tanh_function(x):
    """
    Hyperbolic tangent - transfer function
    """
    return tanh(x)

def tanh_derived(y):
    """
    Hyperbolic tangent - Transfer function derived
    """
    return 1.0 - y**2


# SIGMOID
def sigmoid_function(x):
    """
    Sigmoid - Transfer function
    """
    return 1.0 / (1.0 + e**(-x))

def sigmoid_derived(y):
    """
    Sigmoid - Transfer function derived
    """
    return y - y**2


# IDENTITY
def identity_function(x):
    """
    Identity - Transfer function
    """
    return x

def identity_derived(y):
    """
    Identity - Transfer function derived
    """
    return 1


functions = {
        'identity': (identity_function, identity_derived),
        'sigmoid' : (sigmoid_function, sigmoid_derived),
        'tanh'    : (tanh_function, tanh_derived)
}


