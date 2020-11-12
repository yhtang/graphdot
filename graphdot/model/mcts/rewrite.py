#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Rewrite(ABC):
    ''' Abstract base class for graph rewrite rules. '''

    @abstractmethod
    def __call__(self, g, random_state):
        ''' Rewrite the given graph using a rule drawn randomly from a pool.

        Parameters
        ----------
        g: object
            An input graph to be rewritten.
        random_state: int or :py:`np.random.Generator`
            The seed to the random number generator (RNG), or the RNG itself.
            If None, the default RNG in numpy will be used.

        Returns
        -------
        h: object
            A new graph.
        '''


class SMILESRewriter:
    pass