#!/usr/bin/env python


from collections import defaultdict
import fileinput


def part_one(steps: list) -> int:
    # graph contains nodes and list of edges
    # degree contains the number of parent steps that need to be completed
    graph = defaultdict(list)
    degree = defaultdict(int)
    for (pre, unlock) in steps:
        graph[pre].append(unlock)
        degree[unlock] += 1

    # start our work queue with the nodes that have no parent steps
    # should be just one if the problem input is correct
    queue = []
    for node in graph:
        if degree[node] == 0:
            queue.append(node)

    # while there is work in the queue
    path = []
    while queue:
        # use the lowest item in the queue
        node = sorted(queue)[0]
        queue.remove(node)
        # add it to our output path
        path.append(node)
        # reduce the degree for any node that is unlocked by this node
        for edge in graph[node]:
            degree[edge] -= 1
            # if the degree falls to zero the node is unlocked
            # add it to the queue
            if degree[edge] == 0:
                queue.append(edge)

    return "".join(path)


if __name__ == "__main__":
    instructions = []
    for line in fileinput.input():
        fields = line.strip().split()
        instructions.append((fields[1], fields[7]))

    print(part_one(instructions))
