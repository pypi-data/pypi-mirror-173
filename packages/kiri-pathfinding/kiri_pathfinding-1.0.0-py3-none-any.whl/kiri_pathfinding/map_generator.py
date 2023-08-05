#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:48:15 2022

@author: anthony
"""

import numpy as np
from skimage.measure import label
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


# names of terrains
TERRAINS = ["glass", "mud", "water", "road", ]
# percentages of different terrains
PERCENTAGES = [70, 20, 8, 2]
# entering costs of different terrains
COST_RATIOS = [2, 4, 10, 1]
# colors to visulize the map
COLORS = ["#5FE849", "#AF6714", "#65C8E1", "#B2AEAA"]
# colormap bases on the COLORS
CMAP = LinearSegmentedColormap.from_list(
    "map_color", colors=COLORS, N=len(COLORS))


def generate_map(height, width, seed=None):
    """
    generate a map in size (height * width)

    params
    ------
    height, width : int,
        the height and width of the map

    returns
    -------
    data: np.ndarray(shape=(height, width)),
        data to describe the map

    terrain meaning please refer global variable : TERRAINS


    """
    np.random.seed(seed)
    data_raw = np.random.rand(height, width)
    data_map = np.zeros_like(data_raw, dtype=int)
    terrain_prob = np.cumsum(PERCENTAGES)
    for ind, prob in enumerate(terrain_prob):
        data_map[data_raw > np.percentile(data_raw, prob)] = ind + 1

    # connect river
    connector = TerrainConnector(data_map, 2)
    data_map[connector.connect(3)] = 2

    # connect road
    connector = TerrainConnector(data_map, 3)
    data_map[connector.connect(1)] = 3

    return data_map


def draw_map(data, axes=None):
    """
    visualize the map data

    params
    ------
    data : np.ndarray(dtype=int)
        data to describe a map
    axes : matplotlib.axes.Axes

    returns
    -------
    matplotlib.image.AxesImage

    """
    if axes is None:
        _, axes = plt.subplots()
    return axes.imshow(data, cmap=CMAP)


class TerrainConnector:
    """
    class to connect coordinates in the same terrain

    params
    ------
    data_map : np.ndarray(shape=(n, m))
        data to describe the map
    terrain : int,
        the terrain code to connect

    """

    def __init__(self, data_map, terrain):
        self.mask = data_map == terrain

    def connect(self, max_number=1, min_distance2=2, **kwargs):
        """
        connect by the mask

        params
        ------
        max_number : int or None,
            the max number of coordinate sets,
            None means trying to connect all into one set
        min_distance2 : float,
            min distance of the target point to connect

        kwargs
        ------
        keyword params of kiri_pathfinding.pathfinding.PathFinding

        returns
        -------
        mask : np.ndarray,
            the mask of the connected terrain

        """
        end = False
        while not end:
            end = self._connect(max_number, min_distance2, **kwargs)
        return self.mask

    def _connect(self, max_number=None, min_distance2=2, **kwargs):
        from kiri_pathfinding.pathfinding import PathFinding
        pathfinding = PathFinding(self.mask, cost_ratios=(2, 1), **kwargs)
        img_labeled = label(self.mask, connectivity=2)
        label_ls = np.unique(img_labeled)
        if max_number is not None and label_ls.max() <= max_number:
            return True
        for lab in label_ls:
            if lab == 0:
                continue
            all_connected = self.__connect_lab(
                lab, img_labeled, pathfinding, min_distance2)
            if all_connected:
                return True
        return False

    def __connect_lab(self, lab, img_labeled, pathfinding, min_distance2):
        mask = lab == img_labeled
        nodes = self.__filter_nodes(list(zip(*np.where(mask))))
        indices = list(zip(*np.where((~mask) & self.mask)))
        if len(indices) == 0:
            return True
        for node in nodes:
            target = self.__get_closest_index(node, indices, min_distance2)
            path = pathfinding.find(node, target)
            if path:
                self.mask[tuple(zip(*path))] = True
                break
        return False

    @staticmethod
    def __get_closest_index(point, indices, min_distance2=2):
        delta2 = (np.subtract(indices, point) ** 2).sum(1)
        delta2[delta2 <= min_distance2] = delta2.max() + 1
        return indices[np.argmin(delta2)]

    def __filter_nodes(self, indices):
        return filter(self.__if_node, indices)

    def __if_node(self, coord):
        row, col = coord
        data = self.mask[max(0, row - 1): row + 2, max(0, col - 1): col + 2]
        return data.sum() <= 2
