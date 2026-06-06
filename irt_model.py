"""Basit Rasch/IRT (1PL) modeli - NumPy ile.

Bu dosya eğitim amaçlı, küçük sınıflar ve açık işlevlerle basit bir öğrenci-yetenek modeli sağlar.
"""
import math
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class IRTModel:
    """Basit Rasch modeli (1PL).

    P(response=1 | theta_s, b_i) = sigmoid(theta_s - b_i)
    """
    def __init__(self, n_students, n_items, lr=0.01, reg=1e-3):
        self.n_students = n_students
        self.n_items = n_items
        self.lr = lr
        self.reg = reg
        # Başlangıç tahminleri
        self.theta = np.zeros(n_students)
        self.b = np.zeros(n_items)

    def fit(self, R, epochs=100, verbose=True):
        """Toplu eğitim.

        R: numpy array shape (n_students, n_items) with 0/1 answers
        """
        assert R.shape == (self.n_students, self.n_items)
        for epoch in range(epochs):
            logits = self.theta[:, None] - self.b[None, :]
            p = sigmoid(logits)
            # hata
            err = R - p
            # gradyanlar
            grad_theta = np.sum(err, axis=1) - self.reg * self.theta
            grad_b = -np.sum(err, axis=0) - self.reg * self.b
            # güncelle
            self.theta += self.lr * grad_theta
            self.b += self.lr * grad_b

            if verbose and (epoch % 10 == 0 or epoch == epochs - 1):
                loss = -np.sum(R * np.log(np.clip(p, 1e-9, 1 - 1e-9)) + (1 - R) * np.log(np.clip(1 - p, 1e-9, 1 - 1e-9)))
                print(f"Epoch {epoch+1}/{epochs}  loss={loss:.4f}")

    def predict_prob(self, student_idx, item_idx):
        """Tek tahmin: öğrenci ve madde için doğru gelme olasılığı."""
        return float(sigmoid(self.theta[student_idx] - self.b[item_idx]))

    def update_online(self, student_idx, item_idx, response):
        """Çevrimiçi tek adım güncellemesi."""
        p = self.predict_prob(student_idx, item_idx)
        grad_theta = (response - p) - self.reg * self.theta[student_idx]
        grad_b = -(response - p) - self.reg * self.b[item_idx]
        self.theta[student_idx] += self.lr * grad_theta
        self.b[item_idx] += self.lr * grad_b
