#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The :mod:`bci.base_models` contains classes:

- :class:`bci.base_models.BaseModel`
- :class:`bci.base_models.IdentityModel`
"""
from __future__ import print_function

__docformat__ = 'restructuredtext'

import math

class BaseModel:
    r'''Base class for the BCI models.'''
    def __init__(self):
        r'''Constructor method for BaseModel'''
        pass

    def __call__(self, *input, **kwargs):
        return self.forward(*input, **kwargs)

    def forward(self, input):
        r'''Returns model prediction for the given input data.
        
        :param input: The tensor of the analyzed data.
        :type input: FloatTensor.

        :return: Model answers for the given input data
        :rtype: FloatTensor'''
        raise NotImplementedError

    def fit(self, input):
        r'''Fit model for the given input data.

        :param input: The tensor of the analyzed data.
        :type input: FloatTensor.'''
        raise NotImplementedError


class IdentityModel(BaseModel):
    r'''A model which defines identity mapping.
    Mathematically define model :math:`\textbf{f}(\textbf{x}) = \textbf{x}`.

    .. warning::
        It's just an example of BCI model, and cannot be used in real cases.

    Example:

    >>> _ = torch.random.manual_seed(42) # Set random seed for repeatability
    >>>
    >>> model = IdentityModel()
    >>> X = torch.randn(2, 1) # Generate random tensor
    >>> predict = model(X)
    tensor([[0.3367],
        [0.1288]])'''

    def __init__(self):
        r'''Constructor method for IdentityModel.'''
        super(IdentityModel, self).__init__()

    def forward(self, input):
        r'''Returns model prediction for the given input data.
        
        :param input: The tensor of the analyzed data.
        :type input: FloatTensor.

        :return: Return similar tensor to input data.
        :rtype: FloatTensor'''
        return input