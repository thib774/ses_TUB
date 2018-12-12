import numpy as np
from numpy.testing import assert_array_equal

from lpi_python import lpi_distance, lpi_optimal_permutation, adjusted_pnorm_error, lpi_mean

import math
import pytest

def root_mean_squared_error(y_true, y_pred):
	return math.sqrt(np.average((y_true - y_pred) ** 2))

def mean_absolute_error(y_true, y_pred):
    return np.average(np.abs(y_pred - y_true))

def test_minimal_zero_omega1():
	x1 = np.array([0., 1., 0., 0.])
	x2 = np.array([0., 0., 1., 0.])
	assert lpi_distance(x1, x2, omega=1) == 0

def test_minimal_zero_omega2():
	x1 = np.array([0., 1., 0., 0.])
	x2 = np.array([0., 0., 0., 1.])
	assert lpi_distance(x1, x2, omega=2) == 0

def test_minimal_zero_omega1_nonzero_hand():
	x1 = np.array([0., 1., 0., 0.])
	x2 = np.array([0., 0., 0., 1.])
	assert lpi_distance(x1, x2, omega=1) == math.sqrt(2)

def test_minimal_zero_omega1_hand():
	x1 = np.array([2., 3., 2., 2.])
	x2 = np.array([1., 1., 1., 4.])
	assert lpi_distance(x1, x2, omega=1) == math.sqrt(10)

def test_15min_symmetry_omega1():
	x1 = np.array([0.63,0.66,0.70,0.73,0.76,0.73,0.70,0.67,0.64,0.62,0.60,0.58,0.55,0.54,0.52,0.50,0.49,0.65,0.82,0.98,1.15,1.08,1.02,0.96,0.90,0.92,0.94,0.96,0.98,0.99,0.99,1.00,1.01,1.04,1.07,1.10,1.13,1.16,1.19,1.22,1.25,1.32,1.38,1.45,1.51,1.57,1.63,1.69,1.75,1.79,1.84,1.89,1.94,1.94,1.95,1.96,1.97,2.01,2.06,2.10,2.14,2.09,2.04,1.99,1.94,1.92,1.90,1.88,1.85,1.81,1.77,1.73,1.69,1.65,1.60,1.56,1.51,1.51,1.50,1.50,1.49,1.48,1.47,1.46,1.46,1.42,1.39,1.36,1.33,1.30,1.26,1.22,1.19,1.18,1.17,1.16])
	x2 = np.array([1.15,1.46,1.77,2.08,2.38,2.67,2.95,3.24,3.52,2.80,2.08,1.36,0.65,0.60,0.56,0.52,0.48,0.50,0.52,0.55,0.57,0.69,0.81,0.93,1.05,0.97,0.89,0.82,0.74,0.82,0.91,0.99,1.07,1.09,1.11,1.12,1.14,1.18,1.22,1.27,1.31,1.28,1.26,1.23,1.20,1.25,1.29,1.34,1.38,1.39,1.40,1.40,1.41,1.38,1.34,1.31,1.27,1.53,1.79,2.06,2.32,2.31,2.31,2.31,2.30,1.91,1.52,1.12,0.73,0.59,0.45,0.31,0.18,0.53,0.88,1.23,1.58,1.41,1.25,1.08,0.92,0.94,0.97,0.99,1.02,0.98,0.95,0.92,0.89,0.79,0.70,0.60,0.51,0.50,0.48,0.47])
	omega = 1
	assert pytest.approx(lpi_distance(x1, x2, omega=omega), 0.01) == lpi_distance(x2, x1, omega=omega)

def test_15min_symmetry_omega2():
	x1 = np.array([0.63,0.66,0.70,0.73,0.76,0.73,0.70,0.67,0.64,0.62,0.60,0.58,0.55,0.54,0.52,0.50,0.49,0.65,0.82,0.98,1.15,1.08,1.02,0.96,0.90,0.92,0.94,0.96,0.98,0.99,0.99,1.00,1.01,1.04,1.07,1.10,1.13,1.16,1.19,1.22,1.25,1.32,1.38,1.45,1.51,1.57,1.63,1.69,1.75,1.79,1.84,1.89,1.94,1.94,1.95,1.96,1.97,2.01,2.06,2.10,2.14,2.09,2.04,1.99,1.94,1.92,1.90,1.88,1.85,1.81,1.77,1.73,1.69,1.65,1.60,1.56,1.51,1.51,1.50,1.50,1.49,1.48,1.47,1.46,1.46,1.42,1.39,1.36,1.33,1.30,1.26,1.22,1.19,1.18,1.17,1.16])
	x2 = np.array([1.15,1.46,1.77,2.08,2.38,2.67,2.95,3.24,3.52,2.80,2.08,1.36,0.65,0.60,0.56,0.52,0.48,0.50,0.52,0.55,0.57,0.69,0.81,0.93,1.05,0.97,0.89,0.82,0.74,0.82,0.91,0.99,1.07,1.09,1.11,1.12,1.14,1.18,1.22,1.27,1.31,1.28,1.26,1.23,1.20,1.25,1.29,1.34,1.38,1.39,1.40,1.40,1.41,1.38,1.34,1.31,1.27,1.53,1.79,2.06,2.32,2.31,2.31,2.31,2.30,1.91,1.52,1.12,0.73,0.59,0.45,0.31,0.18,0.53,0.88,1.23,1.58,1.41,1.25,1.08,0.92,0.94,0.97,0.99,1.02,0.98,0.95,0.92,0.89,0.79,0.70,0.60,0.51,0.50,0.48,0.47])
	omega = 2
	assert pytest.approx(lpi_distance(x1, x2, omega=omega), 0.01) == lpi_distance(x2, x1, omega=omega)

def test_15min_symmetry_omega4():
	x1 = np.array([0.63,0.66,0.70,0.73,0.76,0.73,0.70,0.67,0.64,0.62,0.60,0.58,0.55,0.54,0.52,0.50,0.49,0.65,0.82,0.98,1.15,1.08,1.02,0.96,0.90,0.92,0.94,0.96,0.98,0.99,0.99,1.00,1.01,1.04,1.07,1.10,1.13,1.16,1.19,1.22,1.25,1.32,1.38,1.45,1.51,1.57,1.63,1.69,1.75,1.79,1.84,1.89,1.94,1.94,1.95,1.96,1.97,2.01,2.06,2.10,2.14,2.09,2.04,1.99,1.94,1.92,1.90,1.88,1.85,1.81,1.77,1.73,1.69,1.65,1.60,1.56,1.51,1.51,1.50,1.50,1.49,1.48,1.47,1.46,1.46,1.42,1.39,1.36,1.33,1.30,1.26,1.22,1.19,1.18,1.17,1.16])
	x2 = np.array([1.15,1.46,1.77,2.08,2.38,2.67,2.95,3.24,3.52,2.80,2.08,1.36,0.65,0.60,0.56,0.52,0.48,0.50,0.52,0.55,0.57,0.69,0.81,0.93,1.05,0.97,0.89,0.82,0.74,0.82,0.91,0.99,1.07,1.09,1.11,1.12,1.14,1.18,1.22,1.27,1.31,1.28,1.26,1.23,1.20,1.25,1.29,1.34,1.38,1.39,1.40,1.40,1.41,1.38,1.34,1.31,1.27,1.53,1.79,2.06,2.32,2.31,2.31,2.31,2.30,1.91,1.52,1.12,0.73,0.59,0.45,0.31,0.18,0.53,0.88,1.23,1.58,1.41,1.25,1.08,0.92,0.94,0.97,0.99,1.02,0.98,0.95,0.92,0.89,0.79,0.70,0.60,0.51,0.50,0.48,0.47])
	omega = 4
	assert pytest.approx(lpi_distance(x1, x2, omega=omega), 0.01) == lpi_distance(x2, x1, omega=omega)


def test_minimal_optimal_permutation_omega_1():
	x1 = np.array([1., 1., 1., 1., 5., 1.])
	x2 = np.array([2., 2., 2., 2., 2., 5.])
	omega = 1
	assert_array_equal(lpi_optimal_permutation(x1, x2, omega=omega), np.array([1., 1., 1., 1., 1., 5.]))

def test_minimal_optimal_permutation_omega_2():
	x1 = np.array([1., 1., 1., 5., 1., 1.])
	x2 = np.array([2., 2., 2., 2., 2., 5.])
	omega = 2
	assert_array_equal(lpi_optimal_permutation(x1, x2, omega=omega), np.array([1., 1., 1., 1., 1., 5.]))

def test_minimal_optimal_permutation_omega_4():
	x1 = np.array([1., 5., 1., 1., 1., 1.])
	x2 = np.array([2., 2., 2., 2., 2., 5.])
	omega = 4
	assert_array_equal(lpi_optimal_permutation(x1, x2, omega=omega), np.array([1., 1., 1., 1., 1., 5.]))


def test_15min_adjusted_pnorm_rmse_equal():
	y_hat = np.array([0.63,0.66,0.70,0.73,0.76,0.73,0.70,0.67,0.64,0.62,0.60,0.58,0.55,0.54,0.52,0.50,0.49,0.65,0.82,0.98,1.15,1.08,1.02,0.96,0.90,0.92,0.94,0.96,0.98,0.99,0.99,1.00,1.01,1.04,1.07,1.10,1.13,1.16,1.19,1.22,1.25,1.32,1.38,1.45,1.51,1.57,1.63,1.69,1.75,1.79,1.84,1.89,1.94,1.94,1.95,1.96,1.97,2.01,2.06,2.10,2.14,2.09,2.04,1.99,1.94,1.92,1.90,1.88,1.85,1.81,1.77,1.73,1.69,1.65,1.60,1.56,1.51,1.51,1.50,1.50,1.49,1.48,1.47,1.46,1.46,1.42,1.39,1.36,1.33,1.30,1.26,1.22,1.19,1.18,1.17,1.16])
	y_true = np.array([1.15,1.46,1.77,2.08,2.38,2.67,2.95,3.24,3.52,2.80,2.08,1.36,0.65,0.60,0.56,0.52,0.48,0.50,0.52,0.55,0.57,0.69,0.81,0.93,1.05,0.97,0.89,0.82,0.74,0.82,0.91,0.99,1.07,1.09,1.11,1.12,1.14,1.18,1.22,1.27,1.31,1.28,1.26,1.23,1.20,1.25,1.29,1.34,1.38,1.39,1.40,1.40,1.41,1.38,1.34,1.31,1.27,1.53,1.79,2.06,2.32,2.31,2.31,2.31,2.30,1.91,1.52,1.12,0.73,0.59,0.45,0.31,0.18,0.53,0.88,1.23,1.58,1.41,1.25,1.08,0.92,0.94,0.97,0.99,1.02,0.98,0.95,0.92,0.89,0.79,0.70,0.60,0.51,0.50,0.48,0.47])
	omega = 0
	assert pytest.approx(adjusted_pnorm_error(y_true=y_true, y_pred=y_hat, omega=omega, p=2), 0.01) ==  root_mean_squared_error(y_true, y_hat)


def test_15min_adjusted_pnorm_rmse_unequal():
	y_hat = np.array([0.63,0.66,0.70,0.73,0.76,0.73,0.70,0.67,0.64,0.62,0.60,0.58,0.55,0.54,0.52,0.50,0.49,0.65,0.82,0.98,1.15,1.08,1.02,0.96,0.90,0.92,0.94,0.96,0.98,0.99,0.99,1.00,1.01,1.04,1.07,1.10,1.13,1.16,1.19,1.22,1.25,1.32,1.38,1.45,1.51,1.57,1.63,1.69,1.75,1.79,1.84,1.89,1.94,1.94,1.95,1.96,1.97,2.01,2.06,2.10,2.14,2.09,2.04,1.99,1.94,1.92,1.90,1.88,1.85,1.81,1.77,1.73,1.69,1.65,1.60,1.56,1.51,1.51,1.50,1.50,1.49,1.48,1.47,1.46,1.46,1.42,1.39,1.36,1.33,1.30,1.26,1.22,1.19,1.18,1.17,1.16])
	y_true = np.array([1.15,1.46,1.77,2.08,2.38,2.67,2.95,3.24,3.52,2.80,2.08,1.36,0.65,0.60,0.56,0.52,0.48,0.50,0.52,0.55,0.57,0.69,0.81,0.93,1.05,0.97,0.89,0.82,0.74,0.82,0.91,0.99,1.07,1.09,1.11,1.12,1.14,1.18,1.22,1.27,1.31,1.28,1.26,1.23,1.20,1.25,1.29,1.34,1.38,1.39,1.40,1.40,1.41,1.38,1.34,1.31,1.27,1.53,1.79,2.06,2.32,2.31,2.31,2.31,2.30,1.91,1.52,1.12,0.73,0.59,0.45,0.31,0.18,0.53,0.88,1.23,1.58,1.41,1.25,1.08,0.92,0.94,0.97,0.99,1.02,0.98,0.95,0.92,0.89,0.79,0.70,0.60,0.51,0.50,0.48,0.47])
	omega = 2
	assert adjusted_pnorm_error(y_true=y_true, y_pred=y_hat, omega=omega, p=2) <=  root_mean_squared_error(y_true, y_hat) + 0.01 # small error


def test_15min_adjusted_pnorm_mae_equal():
	y_hat = np.array([0.63,0.66,0.70,0.73,0.76,0.73,0.70,0.67,0.64,0.62,0.60,0.58,0.55,0.54,0.52,0.50,0.49,0.65,0.82,0.98,1.15,1.08,1.02,0.96,0.90,0.92,0.94,0.96,0.98,0.99,0.99,1.00,1.01,1.04,1.07,1.10,1.13,1.16,1.19,1.22,1.25,1.32,1.38,1.45,1.51,1.57,1.63,1.69,1.75,1.79,1.84,1.89,1.94,1.94,1.95,1.96,1.97,2.01,2.06,2.10,2.14,2.09,2.04,1.99,1.94,1.92,1.90,1.88,1.85,1.81,1.77,1.73,1.69,1.65,1.60,1.56,1.51,1.51,1.50,1.50,1.49,1.48,1.47,1.46,1.46,1.42,1.39,1.36,1.33,1.30,1.26,1.22,1.19,1.18,1.17,1.16])
	y_true = np.array([1.15,1.46,1.77,2.08,2.38,2.67,2.95,3.24,3.52,2.80,2.08,1.36,0.65,0.60,0.56,0.52,0.48,0.50,0.52,0.55,0.57,0.69,0.81,0.93,1.05,0.97,0.89,0.82,0.74,0.82,0.91,0.99,1.07,1.09,1.11,1.12,1.14,1.18,1.22,1.27,1.31,1.28,1.26,1.23,1.20,1.25,1.29,1.34,1.38,1.39,1.40,1.40,1.41,1.38,1.34,1.31,1.27,1.53,1.79,2.06,2.32,2.31,2.31,2.31,2.30,1.91,1.52,1.12,0.73,0.59,0.45,0.31,0.18,0.53,0.88,1.23,1.58,1.41,1.25,1.08,0.92,0.94,0.97,0.99,1.02,0.98,0.95,0.92,0.89,0.79,0.70,0.60,0.51,0.50,0.48,0.47])
	omega = 0
	assert pytest.approx(adjusted_pnorm_error(y_true=y_true, y_pred=y_hat, omega=omega, p=1), 0.01) ==  mean_absolute_error(y_true, y_hat)


def test_15min_adjusted_pnorm_mae_unequal():
	y_hat = np.array([0.63,0.66,0.70,0.73,0.76,0.73,0.70,0.67,0.64,0.62,0.60,0.58,0.55,0.54,0.52,0.50,0.49,0.65,0.82,0.98,1.15,1.08,1.02,0.96,0.90,0.92,0.94,0.96,0.98,0.99,0.99,1.00,1.01,1.04,1.07,1.10,1.13,1.16,1.19,1.22,1.25,1.32,1.38,1.45,1.51,1.57,1.63,1.69,1.75,1.79,1.84,1.89,1.94,1.94,1.95,1.96,1.97,2.01,2.06,2.10,2.14,2.09,2.04,1.99,1.94,1.92,1.90,1.88,1.85,1.81,1.77,1.73,1.69,1.65,1.60,1.56,1.51,1.51,1.50,1.50,1.49,1.48,1.47,1.46,1.46,1.42,1.39,1.36,1.33,1.30,1.26,1.22,1.19,1.18,1.17,1.16])
	y_true = np.array([1.15,1.46,1.77,2.08,2.38,2.67,2.95,3.24,3.52,2.80,2.08,1.36,0.65,0.60,0.56,0.52,0.48,0.50,0.52,0.55,0.57,0.69,0.81,0.93,1.05,0.97,0.89,0.82,0.74,0.82,0.91,0.99,1.07,1.09,1.11,1.12,1.14,1.18,1.22,1.27,1.31,1.28,1.26,1.23,1.20,1.25,1.29,1.34,1.38,1.39,1.40,1.40,1.41,1.38,1.34,1.31,1.27,1.53,1.79,2.06,2.32,2.31,2.31,2.31,2.30,1.91,1.52,1.12,0.73,0.59,0.45,0.31,0.18,0.53,0.88,1.23,1.58,1.41,1.25,1.08,0.92,0.94,0.97,0.99,1.02,0.98,0.95,0.92,0.89,0.79,0.70,0.60,0.51,0.50,0.48,0.47])
	omega = 2
	assert adjusted_pnorm_error(y_true=y_true, y_pred=y_hat, omega=omega, p=1) <=  mean_absolute_error(y_true, y_hat) + 0.01 # small error