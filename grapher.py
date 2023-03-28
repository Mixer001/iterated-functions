import csv

import networkx as nx
import matplotlib.pyplot as plt
from netgraph import Graph

import numpy as np

from colorama import init as init_colorama
from colorama import Fore
from colorama import Style

init_colorama()

def DrawAGraph(A_graph):
    if(nx.is_planar(A_graph)):
        node_pos = nx.planar_layout(A_graph)
        Graph(A_graph, 
            node_layout = node_pos,
            arrows = True,
            node_labels = True,
            node_label_fontdict=dict(size=10))
        #nx.draw(A_graph, pos = node_pos)
    else:
        node_pos = nx.kamada_kawai_layout(A_graph)
        #node_pos = nx.spring_layout(A_graph, pos = nx.spectral_layout(A_graph), iterations = 5)
        Graph(A_graph,
            node_layout = node_pos,
            arrows = True,
            node_labels = True,
            node_label_fontdict=dict(size=10),
            edge_layout = 'curved')
    plt.show()

def PrintOrbitDetails(file, orbit, orbit_index = 0):
    file.write("\n=====     Orbit %d     =====\n" % orbit_index)
    period = len(orbit)
    mapping = {orbit[i] : orbit[(i+1)%period] for i in range(period)}
    orbit_sort = sorted(orbit)

    file.write("Period: %d\n" % period)

    file.write("Orbit points:\n")
    for i in range(period // 10):
        for j in range(10):
            if(10*i + j < len(orbit)):
                file.write(" -> %f" % orbit[10*i + j])
            else:
                break

        file.write(" ->\n")

    file.write("Max: %f\nMin: %f\n" % (orbit_sort[-1], orbit_sort[0]))

def CreateGraph(file, orbit):
    period = len(orbit)
    mapping = {orbit[i] : orbit[(i+1)%period] for i in range(period)}
    orbit_sort = sorted(orbit)

    file.write("A-Graph edges:\n")

    A_graph = nx.DiGraph()
    for i in range(period - 1):
        segment_a = orbit_sort[i:i+2]
        image = []

        if((segment_a[0] < 0.5) & (segment_a[1] > 0.5)):
            image = [min(mapping[segment_a[0]], mapping[segment_a[1]]), 1.0]
        else:
            image = [min(mapping[segment_a[0]], mapping[segment_a[1]]), max(mapping[segment_a[0]], mapping[segment_a[1]])]
            
        for j in range(period - 1):
            if((image[0] <= orbit_sort[j]) & (orbit_sort[j+1] <= image[1])):
                file.write("%d>%d\n" % (i+1, j+1))
                A_graph.add_edge(i+1, j+1)
    
    return A_graph

orbits = []
graphs = []

with open("input.csv") as file_in:
    reader = csv.reader(file_in, dialect="excel")

    row_number = 0
    for row in reader:
        row_number += 1
        if(len(row) == 0):
            print(f"{Style.DIM}Skipping empty row {row_number}.{Style.RESET_ALL}")
            continue

        inverse = [float(x) for x in reversed(row)]
        points = [inverse[0]]
        orbit_found = False

        for i in range(1, len(inverse)):
            if(points[0] != inverse[i]):
                points.append(inverse[i])
            else:
                orbit_found = True
                break
        
        if(orbit_found):
            print(f"{Fore.GREEN}Orbit of period {len(points)} found in row {row_number}.{Style.RESET_ALL}")
            points.reverse()
            orbits.append(points)
        else:
            print(f"{Fore.RED}Orbit not found in row {row_number}.{Style.RESET_ALL}")

with open("output\\orbits.csv", "w") as file_out:
    writer = csv.writer(file_out, dialect="excel")

    for orbit in orbits:
        writer.writerow(orbit)
    
    file_out.close()

with open("output\\orbits.txt", "w") as file_out:
    for orbit_index in range(len(orbits)):
        PrintOrbitDetails(file=file_out, orbit=orbits[orbit_index], orbit_index=orbit_index)
        A_graph = CreateGraph(file=file_out, orbit=orbits[orbit_index])
        graphs.append(A_graph)
        DrawAGraph(A_graph)

    file_out.close()