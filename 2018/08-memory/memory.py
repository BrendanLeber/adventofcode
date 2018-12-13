#!/usr/bin/env python


import fileinput


class Node:
    def __init__(self):
        self.meta_sum = 0
        self.children = list()
        self.metadata = list()

    def __repr__(self):
        return f"Node(ms: {self.meta_sum} ch: {self.children} meta: {self.metadata})"

    def add_child(self, child):
        self.children.append(child)

    def add_metadata(self, value):
        self.metadata.append(value)

    def sum_metadata(self):
        self.meta_sum = sum(self.metadata)
        for child in self.children:
            self.meta_sum += child.sum_metadata()
        return self.meta_sum

    def sum_metaindex(self):
        self.meta_sum = 0
        if not self.children:
            self.meta_sum = sum(self.metadata)
            return self.meta_sum

        for idx in self.metadata:
            if 0 < idx <= len(self.children):
                self.meta_sum += self.children[idx - 1].sum_metaindex()
        return self.meta_sum


def build_tree(values):
    num_children = values.pop(0)
    num_metadata = values.pop(0)

    node = Node()
    for _ in range(num_children):
        child = build_tree(values)
        node.add_child(child)
    for _ in range(num_metadata):
        node.add_metadata(values.pop(0))

    return node


def part_one(root):
    return root.sum_metadata()


def part_two(root):
    return root.sum_metaindex()


if __name__ == "__main__":
    data = []
    for line in fileinput.input():
        data.extend(list(map(int, line.strip().split())))

    tree = build_tree(data)

    print(part_one(tree))
    print(part_two(tree))
