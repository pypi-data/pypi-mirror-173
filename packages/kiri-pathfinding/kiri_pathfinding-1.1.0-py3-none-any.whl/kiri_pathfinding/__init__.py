#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 18:04:05 2022

@author: anthony
"""
from matplotlib import pyplot as plt
from kiri_pathfinding.map_generator import generate_map, draw_map
from kiri_pathfinding.pathfinding import PathFinding, draw_path


if __name__ == "__main__":
    data_map = generate_map(20, 20)
    pathfinding = PathFinding(data_map)
    path = pathfinding.find((0, 0), (19, 19))

    fig, ax = plt.subplots()
    draw_map(data_map, ax)
    draw_path(path, ax)
