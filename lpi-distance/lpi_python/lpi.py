# Author: 	Marcus Voss <voss.marcus@gmail.com>
# License: BSD 3 clause
from scipy.optimize import linear_sum_assignment
import numpy as np

def lpi_medoid(series, omega=1):
	''' finds initial profile by determining the medoid in terms of the adjusted p-norm '''
	distances = np.zeros((len(series), len(series)))

	for i in range(len(series)):
		for j in range(len(series)):
			distances[i,j] = lpi_distance(series[i], series[j], omega=omega)

	return series[np.argmin(distances.sum(axis=0))]



def lpi_optimal_permutation(x1, x2, omega=1, p=2):
	"""
	This is a Python implementation of the LPI distance solved by the Kuhn-Munkres Algorithm (or Hungarian Method) in O(n^4). Problem is formulated as introduced by Haben et al.

	Parameters
	----------
	x1 : np.ndarray, list, or tuple
		First Sequence
	x2 : np.ndarray, list, or tuple
		Second Sequence
	omega: int
		Local restriction parameter
	p: omega
		Order of the p-norm.

	Returns
	-------
	np.ndarray
		Optimal permutation of x1

	"""
	# some very high constant value
	OMEGA = 9999999.

	# length of vector
	n = len(x1)

	# create a cost matrix pre-filled with high constant
	cost = np.full((n,n), (OMEGA))

	# now fill for each the current cost, as allowed per constraint of |f_i - pij| < omega
	for i in range(0, n):
		for j in range(max(0, i-omega), min(n, i+omega+1)):
			cost[i,j] = abs(x2[i] - x1[j])**p
	
	# solve the assigment problem given the cost matrix
	row_ind, col_ind = linear_sum_assignment(cost)

	# use the optimal assignemnt indices to create a permuation matrix
	pi = np.zeros((n,n))
	pi[row_ind, col_ind] = 1

	return np.dot(pi, x1) 


def lpi_distance(x1, x2, omega=1, p=2):
	"""
	This is a Python implementation of the LPI distance solved by the Kuhn-Munkres Algorithm (or Hungarian Method) in O(n^4). Problem is formulated as introduced by Haben et al.

	Parameters
	----------
	x1 : np.ndarray, list, or tuple
		First Sequence
	x2 : np.ndarray, list, or tuple
		Second Sequence
	omega: int
		Local restriction parameter
	p: omega
		Order of the p-norm.

	Returns
	-------
	float
		LPI distance 

	"""
	return np.linalg.norm(lpi_optimal_permutation(x1, x2, omega=omega, p=p) - x2, ord=p)


def adjusted_pnorm_error(y_true, y_pred, omega=1, p=2):
	"""
	Adjusted Error as defined by Haben et al.

	Parameters
	----------
	y_pred : np.ndarray, list, or tuple (1- or 2-dimensional)
		First Sequence
	y_true : np.ndarray, list, or tuple (1- or 2-dimensional)
		Second Sequence
	omega: int
		Local restriction parameter
	p: omega
		Order of the p-norm.

	Returns
	-------
	float
		Squared Mean Adjusted Error

	"""
	return (1 / len(y_true)**(1/p)) * lpi_distance(x1=y_pred, x2=y_true, omega=omega, p=p)


def lpi_mean(series, omega=1, max_iter=10):
	"""
	Majorize Minimize Algorithm for Sample Mean Approximation in LPI space.

	Parameters
	----------
	series : np.ndarray, shape=[N, n]
		N series of length n to average.
	omega: int, default = 1
		Local restriction parameter. Must be chose for specific use case and data resolution.
	max_iter: int, optional, default 10
		Maximum number of epochs.
	
	Returns
	-------
	np.ndarray, shape=(n,)
		LPI sample mean approximation.
	"""
	center = lpi_medoid(series, omega=omega)

	for epoch in range(max_iter):
		optimal_permutations = []
		for s in series:
			optimal_permutations.append(lpi_optimal_permutation(s, center, omega=omega))
		center = np.mean(np.array(optimal_permutations), axis=0)
	return center