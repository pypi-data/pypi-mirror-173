#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 17:25:41 2022

@author: anthony
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.sparse import csr_matrix
from kiri_pathfinding.map_generator import COST_RATIOS


INDEX_DELTAS = [
    (14, np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]])),
    (10, np.array([[-1, 0], [0, -1], [0, 1], [1, 0]])),
]


def draw_path(path, axes=None, color='r'):
    "visualize the path"
    if axes is None:
        _, axes = plt.subplots()
    return axes.plot(*zip(*map(lambda x: x[::-1], path)), color=color)


def generate_connection(data, cost_ratios=None, index_deltas=None):
    """
    generate a array to describe the moving costs between grids in the map.

    params
    ------
    data : np.ndarray(dtype=int),
        the data to describe a map
    dtype : "dict" or "array",
        the data type of the connection costs
    cost_ratios : None or list,
        the cost of each type of terrains,
        None means use default values
    index_deltas : None or list,
        the deltas of different indices,
        None means use default values

    returns
    -------
    connection : dict or np.ndarray,
        the data of costs in connections

    """
    if cost_ratios is None:
        cost_ratios = COST_RATIOS
    if index_deltas is None:
        index_deltas = INDEX_DELTAS
    return _generate_connection_dict(data, cost_ratios, index_deltas)


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
        e_cost = self._get_estimated_cost(stop, target)
        c_cost = (self.movement_ratio * m_cost +
                  self.estimated_ratio * e_cost)
        return c_cost, m_cost

    @staticmethod
    def _get_estimated_cost(start, target):
        cost = np.abs(np.subtract(start, target)).sum() * 20
        return cost

    def _get_movement_cost(self, start, target):
        cost = self.data_connection.get(target, {}).get(start)
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


def _generate_connection_array(data, cost_ratios):
    n_row, n_col = data.shape
    n_indices = n_row * n_col
    connection = csr_matrix(np.zeros((n_indices, n_indices), dtype=int))

    def _generate_conn(ind):
        row, col = _index_to_rowcol(ind, n_col)
        ratio = cost_ratios[data[row, col]]
        for cost, delta in INDEX_DELTAS:
            indices = list(
                filter(lambda x: 0 <= x < n_indices,
                       map(lambda x: _rowcol_to_index(*x, n_col),
                           delta + _index_to_rowcol(ind, n_col),
                           )
                       )
            )
            connection[ind, indices] = ratio * cost

    list(map(_generate_conn, range(n_indices)))
    return connection


def _index_to_rowcol(index, n_col):
    row = index // n_col
    col = index % n_col
    return row, col


def _rowcol_to_index(row, col, n_col):
    index = row * n_col + col
    return index


def _generate_connection_dict(data, cost_ratios, index_deltas):
    connection = {}
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            indices_to_costs = _generate_indices_to_costs(
                row, col, cost_ratios[data[row, col]], data.shape, index_deltas
            )
            connection[row, col] = indices_to_costs
    return connection


def _generate_indices_to_costs(row, col, ratio, shape, index_deltas):
    indices_to_costs = {}
    if ratio <= 0:
        return indices_to_costs
    for cost, indices in index_deltas:
        for row_ind, col_ind in indices + (row, col):
            if not (0 <= row_ind < shape[0] and 0 <= col_ind < shape[1]):
                continue
            indices_to_costs[(row_ind, col_ind)] = ratio * cost
    return indices_to_costs
