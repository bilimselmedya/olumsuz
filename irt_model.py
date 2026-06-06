"""Simple Rasch/IRT (1PL) implementation with NumPy.

This file provides a minimal, well-documented IRTModel suitable for
experimentation and teaching. It intentionally keeps dependencies small
and code readable.
"""
from __future__ import annotations

import numpy as np
from typing import Optional


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


class IRTModel:
    """Rasch / 1PL IRT model.

    P(response=1 | theta_s, b_i) = sigmoid(theta_s - b_i)

    Usage:
        model = IRTModel(n_students, n_items)
        model.fit(R)
        p = model.predict_prob(0, 1)
    """

    def __init__(self, n_students: int, n_items: int, lr: float = 0.01, reg: float = 1e-3):
        self.n_students = int(n_students)
        self.n_items = int(n_items)
        self.lr = float(lr)
        self.reg = float(reg)

        # parameters
        self.theta = np.zeros(self.n_students, dtype=float)
        self.b = np.zeros(self.n_items, dtype=float)

    def fit(self, R: np.ndarray, epochs: int = 100, verbose: bool = True) -> None:
        """Batch gradient updates on a dense response matrix R.

        R should be shape (n_students, n_items) with values 0/1.
        """
        if R.shape != (self.n_students, self.n_items):
            raise ValueError("R must have shape (n_students, n_items)")

        for epoch in range(1, epochs + 1):
            logits = self.theta[:, None] - self.b[None, :]
            p = _sigmoid(logits)
            err = R - p

            grad_theta = np.sum(err, axis=1) - self.reg * self.theta
            grad_b = -np.sum(err, axis=0) - self.reg * self.b

            self.theta += self.lr * grad_theta
            self.b += self.lr * grad_b

            if verbose and (epoch % 10 == 0 or epoch == epochs):
                # negative log-likelihood
                eps = 1e-9
                loss = -np.sum(R * np.log(np.clip(p, eps, 1 - eps)) + (1 - R) * np.log(np.clip(1 - p, eps, 1 - eps)))
                print(f"Epoch {epoch}/{epochs} loss={loss:.4f}")

    def predict_prob(self, student_idx: int, item_idx: int) -> float:
        """Return probability student `student_idx` answers item `item_idx` correctly."""
        return float(_sigmoid(self.theta[int(student_idx)] - self.b[int(item_idx)]))

    def update_online(self, student_idx: int, item_idx: int, response: int) -> None:
        """One-step online update (stochastic gradient) for a single observation."""
        p = self.predict_prob(student_idx, item_idx)
        grad_theta = (response - p) - self.reg * self.theta[int(student_idx)]
        grad_b = -(response - p) - self.reg * self.b[int(item_idx)]

        self.theta[int(student_idx)] += self.lr * grad_theta
        self.b[int(item_idx)] += self.lr * grad_b

    def get_parameters(self) -> tuple[np.ndarray, np.ndarray]:
        return self.theta.copy(), self.b.copy()

