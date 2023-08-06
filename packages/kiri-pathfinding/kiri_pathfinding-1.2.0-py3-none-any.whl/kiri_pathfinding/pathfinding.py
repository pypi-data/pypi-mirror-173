#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 17:25:41 2022

@author: anthony
"""
from itertools import product
import numpy as np
from numpy.lib.stride_tricks import as_strided
from matplotlib import pyplot as plt
from scipy.ndimage import binary_dilation
from kiri_pathfinding.map_generator import COST_RATIOS


INDEX_DELTAS = [
    (14, np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]], dtype=int)),
    (10, np.array([[-1, 0], [0, -1], [0, 1], [1, 0]], dtype=int)),
]

ARRAY_CROSS = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
], dtype=int)


def draw_path(path, axes=None, color='r'):
    "visualize the path"
    if axes is None:
        _, axes = plt.subplots()
    return axes.plot(*zip(*map(lambda x: x[::-1], path)), color=color)


def generate_connection(
    data, method='array', cost_ratios=None, index_deltas=None, **kwargs
):
    """
    generate a array to describe the moving costs between grids in the map.

    params
    ------
    data : np.ndarray(dtype=int),
        the data to describe a map
    method : "dict" or "array",
        the calculating method of the connection costs
    cost_ratios : None or list,
        the cost of each type of terrains,
        None means use default values
    index_deltas : None or list,
        the deltas of different indices,
        None means use default values

    kwargs
    ------
    nebr_test : bool, the default is False.
        available when arg : method == 'array'.
        True means to consider the neighbor of slants
        False means to ignore that.
        Will run in a longer time.

    returns
    -------
    connection : dict or np.ndarray,
        the data of costs in connections

    """
    if cost_ratios is None:
        cost_ratios = COST_RATIOS
    if index_deltas is None:
        index_deltas = INDEX_DELTAS
    return {"dict": _generate_connection_dict,
            "array": _generate_connection_array,
            }[method](data, cost_ratios, index_deltas, **kwargs)


class PathFinding:
    """
    a class to read map data and find path from point to point, using A* algorithm

    params
    ------
    data_map : np.ndarray(shape=(n, m)),
        the data to describe a map
    balance : (movement_ratio, estimated_ratio),
        ratios of different costs, the default is (1, 1)

    kwargs
    ------
    keyword params of func : generate_connection

    """

    def __init__(self, data_map, balance=None, **kwargs):
        if balance is None:
            balance = (1, 1)
        self.data_connection = generate_connection(data_map, **kwargs)
        self.movement_ratio, self.estimated_ratio = balance
        self.__init_result()

    def __get_costs(self, start, stop, target):
        """
        return the composite cost and movement cost
        from start point to stop point

        """
        m_cost = self._get_movement_cost(start, stop)
        if not m_cost:
            return None, None
        e_cost = self._get_estimated_cost(stop, target)
        c_cost = (self.movement_ratio * m_cost +
                  self.estimated_ratio * e_cost)
        return c_cost, m_cost

    @staticmethod
    def _get_estimated_cost(start, target):
        cost = np.abs(np.subtract(start, target)).sum() * 20
        return cost

    def _get_movement_cost(self, start, target):
        cost = self.data_connection.get(start, {}).get(target)
        return cost

    def __init_result(self):
        self.__closed = set()
        self.__opened = []
        self.__data_points = {}

    def find(self, start, target):
        """
        return the shortest path from start to target point

        params
        ------
        start, target : (y, x)
            the (y, x) coordinates of start and target point

        returns
        -------
        path : list,
            the shortest path, void list means can not find a path

        """
        # init
        self.__init_result()
        self.__opened.append(start)
        self.__data_points[start] = (0, 0, None)

        end = False
        while not end:
            end = self._find_next(target)

        path = self.__get_path(target)
        return path

    def get_cost(self, target):
        "return the cost from the present start point to target in the present pathfinding"
        return self.__data_points[target[1]][0]

    def _find_next(self, target):
        if len(self.__opened) == 0:
            return True

        # init data
        end = False
        ind, current_point = min(
            list(enumerate(self.__opened))[::-1],
            key=lambda x: self.__data_points[x[1]][:2]
        )
        self.__opened.pop(ind)
        self.__closed.add(current_point)
        current_m_cost = self.__data_points[current_point][1]
        points = self.data_connection.get(current_point, ())

        # target reached
        if target in points:
            points = [target]
            end = True

        # record data
        for point in points:
            if point in self.__closed:
                continue
            c_cost, m_cost = self.__get_costs(current_point, point, target)
            if not m_cost:
                continue
            c_cost += current_m_cost
            m_cost += current_m_cost
            if (point not in self.__opened
                    or m_cost < self.__data_points[point][1]):
                self.__data_points[point] = c_cost, m_cost, current_point
                try:
                    self.__opened.remove(point)
                except ValueError:
                    pass
                self.__opened.append(point)

        return end

    def __get_path(self, target):
        if target not in self.__data_points:
            return []

        path = [target]
        parent = self.__data_points[target][2]
        while parent:
            path.append(parent)
            parent = self.__data_points[parent][2]
        return path[::-1]


def _generate_connection_dict(data_map, cost_ratios, index_deltas):
    "this method can not consider the neighbor of slants"
    connection = {}
    for row in range(data_map.shape[0]):
        for col in range(data_map.shape[1]):
            conn = _get_indices_to_costs(
                row, col,
                cost_ratios[data_map[row, col]], data_map.shape, index_deltas
            )
            for rowcol, cost in conn.items():
                try:
                    data = connection[rowcol]
                except KeyError:
                    data = {}
                    connection[rowcol] = data
                data[row, col] = cost
    return connection


def _get_indices_to_costs(row, col, ratio, shape, index_deltas):
    indices_to_costs = {}
    if ratio <= 0:
        return indices_to_costs
    for cost, indices in index_deltas:
        entering_cost = int(ratio * cost)
        if not entering_cost:
            continue
        for row_ind, col_ind in indices + (row, col):
            if not (0 <= row_ind < shape[0] and 0 <= col_ind < shape[1]):
                continue
            indices_to_costs[(row_ind, col_ind)] = entering_cost
    return indices_to_costs


def _generate_connection_array(
        data_map, cost_ratios, index_deltas, nebr_test=False):
    "this method can consider the neighbor of slants"
    index_masks = _get_index_masks(index_deltas, nebr_test)
    data_costs = _get_data_costs(data_map, cost_ratios)

    n_row, n_col = data_map.shape
    func = _base_get_array_connect
    if nebr_test:
        func = _base_get_array_connect_with_nebr
    connection = dict(
        map(lambda x: (x, _get_array_connect(x, data_costs[x], index_masks, func)),
            product(range(n_row), range(n_col))))
    return connection


def _get_data_costs(data_map, cost_ratios):
    data_base = np.vectorize(lambda x: cost_ratios[x])(data_map)
    data_base = np.pad(data_base, 1, constant_values=0)
    n_row, n_col = data_map.shape
    data_costs = as_strided(
        data_base, shape=(n_row, n_col, 3, 3),
        strides=data_base.strides + data_base.strides)
    return data_costs


def _get_index_masks(index_deltas, nebr_test):
    index_masks = []
    for delta, indices in index_deltas:
        for index in indices:
            index_masks.append((delta, index,
                                _convert_index_to_mask(index, nebr_test)))
    return index_masks


def _convert_index_to_mask(index, nebr_test):
    if not nebr_test:
        return tuple(index + 1)
    mask = np.zeros((3, 3), dtype=bool)
    mask[tuple(index + 1)] = 1
    if np.abs(index).sum() > 1:
        mask = binary_dilation(mask, ARRAY_CROSS)
    return mask


def _get_array_connect(rowcol, array, index_masks, func):
    connection = {}
    for delta, index, mask in index_masks:
        cost = func(array, mask)
        if cost > 0:
            connection[tuple(index + rowcol)] = int(cost * delta)
    return connection


def _base_get_array_connect(array, mask):
    return array[mask]


def _base_get_array_connect_with_nebr(array, mask):
    data = array[mask]
    if 0 in data:
        return 0
    return max(data)
