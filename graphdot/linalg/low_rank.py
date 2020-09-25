#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Low-rank approximation of square matrices.'''
import numpy as np


class LowRankBase:
    def __add__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)

    def __matmul__(self, other):
        return matmul(self, other)


class Sum(LowRankBase):
    '''Represents summations of factor approximations. Due to the bilinear
    nature of matrix inner product, it is best to store the summation as-is so
    as to preserve the low-rank structure of the matrices.'''

    def __init__(self, factors):
        self.factors = factors

    def __repr__(self):
        return ' + '.join([f'({repr(f)})' for f in self.factors])

    @property
    def T(self):
        return Sum([f.T for f in self.factors])

    def __neg__(self):
        return Sum([-f for f in self.factors])

    def diagonal(self):
        return np.sum([f.diagonal() for f in self.factors], axis=0)

    def trace(self):
        return np.sum([f.diagonal().sum() for f in self.factors])

    def quadratic(self, a, b):
        '''Computes a @ X @ b.'''
        return np.sum([f.quadratic(a, b) for f in self.factors], axis=0)

    def todense(self):
        return np.sum([f.todense() for f in self.factors], axis=0)


class LATR(LowRankBase):
    '''Represents an N-by-N square matrix A as L @ R, where L and R are N-by-k
    and k-by-N (k << N) rectangular matrices.'''

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def __repr__(self):
        return f'{self.lhs.shape} @ {self.rhs.shape}'

    @property
    def lhs(self):
        return self._lhs

    @property
    def rhs(self):
        return self._rhs

    @property
    def T(self):
        return LATR(self.rhs.T, self.lhs.T)

    def __neg__(self):
        return LATR(-self.lhs, self.rhs)

    def todense(self):
        return self.lhs @ self.rhs

    def diagonal(self):
        return np.sum(self.lhs * self.rhs.T, axis=1)

    def trace(self):
        return self.diagonal().sum()

    def quadratic(self, a, b):
        '''Computes a @ X @ b.'''
        return (a @ self.lhs) @ (self.rhs @ b)

    def quadratic_diag(self, a, b):
        '''Computes diag(a @ X @ b).'''
        return LATR(a @ self.lhs, self.rhs @ b).diagonal()


class LLT(LATR):
    '''A special case of factor approximation where the matrix is symmetric and
    positive-semidefinite. In this case, the matrix can be represented as
    L @ L.T from a spectral decomposition.'''

    def __init__(self, X, rcond=0, mode='truncate'):
        if isinstance(X, np.ndarray):
            U, S, _ = np.linalg.svd(X, full_matrices=False)
            beta = S.max() * rcond
            if mode == 'truncate':
                mask = S >= beta
                self.U = U[:, mask]
                self.S = S[mask]
            elif mode == 'clamp':
                self.U = U
                self.S = np.maximum(S, beta)
            else:
                raise RuntimeError(
                    f"Unknown spectral approximation mode '{mode}'."
                )
        elif isinstance(X, tuple) and len(X) == 2:
            self.U, self.S = X
        self._lhs = self.U * self.S

    @property
    def lhs(self):
        return self._lhs

    @property
    def rhs(self):
        return self._lhs.T

    def diagonal(self):
        return np.sum(self.lhs**2, axis=1)

    def pinv(self):
        return LLT((self.U, 1 / self.S))

    def logdet(self):
        return 2 * np.log(self.S).sum()

    def cond(self):
        return (self.S.max() / self.S.min())**2

    def __pow__(self, exp):
        return LLT((self.U, self.S**exp))


def dot(X, Y=None, rcond=0, mode='truncate'):
    '''A utility method that creates factor-approximated matrix objects.'''
    if Y is None:
        return LLT(X, rcond=rcond, mode=mode)
    else:
        return LATR(X, Y)


def add(A, B):
    factors = A.factors if isinstance(A, Sum) else [A]
    factors += B.factors if isinstance(B, Sum) else [B]
    return Sum(factors)


def sub(A, B):
    factors = A.factors if isinstance(A, Sum) else [A]
    factors += [-f for f in B.factors] if isinstance(B, Sum) else [-B]
    return Sum(factors)


def matmul(A, B):
    if isinstance(A, Sum):
        if isinstance(B, Sum):
            return Sum([
                a @ b for a in A.factors for b in B.factors
            ])
        else:
            return Sum([
                a @ B for a in A.factors
            ])
    else:
        if isinstance(B, Sum):
            return Sum([
                A @ b for b in B.factors
            ])
        elif isinstance(B, LATR):
            return LATR(A.lhs, (A.rhs @ B.lhs) @ B.rhs)
        else:
            return A.lhs @ (A.rhs @ B)
