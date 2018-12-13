#!/usr/bin/env python


from collections import defaultdict
import fileinput


def part_one(steps):
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


def part_two(steps):
    # graph contains nodes and list of edges
    # degree contains the number of parent steps that need to be completed
    graph = defaultdict(list)
    degree = defaultdict(int)
    for (pre, unlock) in steps:
        graph[pre].append(unlock)
        degree[unlock] += 1
    for node in graph:
        graph[node] = sorted(graph[node])

    # start our work queue with the nodes that have no parent steps
    # should be just one if the problem input is correct
    queue = []
    for node in graph:
        if degree[node] == 0:
            queue.append(node)

    # create events to handle the work if we have workers (5)
    events = []
    while len(events) < 5 and queue:
        node = min(queue)
        queue.remove(node)
        events.append((61 + ord(node) - ord("A"), node))

    # process the rest of the steps as long as there is work in the queue
    # or we have events to handle
    while events or queue:
        # take the first event and process it
        time_taken, node = min(events)
        events.remove((time_taken, node))
        for edge in graph[node]:
            degree[edge] -= 1
            if degree[edge] == 0:
                queue.append(edge)

        # add more events to the event queue if there are workers to handle them
        while len(events) < 5 and queue:
            node = min(queue)
            queue.remove(node)
            events.append((time_taken + 61 + ord(node) - ord("A"), node))

    return time_taken


if __name__ == "__main__":
    instructions = []
    for line in fileinput.input():
        fields = line.strip().split()
        instructions.append((fields[1], fields[7]))

    print(part_one(instructions))
    print(part_two(instructions))
