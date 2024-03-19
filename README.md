# Introduction

This tool is a tool to test the forwarding effect of different algorithms when a point is dynamically selected as a broadcast point in a complete graph.

We hope that the algorithm ensures redundancy in network forwarding while reducing the amount of redundant forwarding, and does not overload a single node when multiple broadcast points are simultaneously present.

After comparing matpilot and graphviz, the dot file displays better, so the final presentation is in the form of dots

## Usage

`python3 main.py --config input2.json`

and then copy graph/xxx.dot to https://edotor.net/