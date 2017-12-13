#pragma once

#include <stdexcept>
#include <vector>

class Adjacency_Matrix {
public:
    std::vector<int> inner;
    size_t rows, cols;

    Adjacency_Matrix(size_t c, size_t r) : rows(r), cols(c)
    {
        if (rows != cols) {
            throw std::range_error("rows != cols");
        }

        inner.resize(rows * cols);
    }

    int& operator()(int col, int row)
    {
        auto c = static_cast<size_t>(col);
        auto r = static_cast<size_t>(row);
        if (r >= rows) {
            throw std::range_error("row outside of matrix size");
        }
        else if (c >= cols) {
            throw std::range_error("col outside of matrix size");
        }

        return inner[cols * r + c];
    }
};

struct Vertex {
    int name;
    bool visited;
    int component;

    explicit Vertex(int n) : name(n), visited(false), component(0)
    {
    }

    Vertex() : Vertex(0)
    {
    }
};

struct Graph {
    int num_nodes;
    Adjacency_Matrix adj;
    std::vector<Vertex> vertices;

    explicit Graph(int nodes) : num_nodes(nodes), adj(static_cast<size_t>(nodes), static_cast<size_t>(nodes))
    {
        vertices.resize(static_cast<size_t>(nodes));
        for (int i = 0; i < num_nodes; ++i) {
            vertices[static_cast<size_t>(i)] = Vertex(i);
        }
    }

    void clear_visitation()
    {
        for (auto& v : vertices) {
            v.visited = false;
            v.component = 0;
        }
    }

    void connect(int x, int y)
    {
        adj(x, y) = 1;
        adj(y, x) = 1;
    }

    void explore(int v, int cc)
    {
        vertices[static_cast<size_t>(v)].visited = true;
        vertices[static_cast<size_t>(v)].component = cc;
        for (int col = 0; col < static_cast<int>(adj.cols); ++col) {
            if (adj(v, col) != 0 && !vertices[static_cast<size_t>(col)].visited) {
                explore(col, cc);
            }
        }
    }

    int number_of_components()
    {
        clear_visitation();

        int components = 0;
        for (size_t v = 0; v < vertices.size(); ++v) {
            if (!vertices[v].visited) {
                ++components;
                explore(static_cast<int>(v), components);
            }
        }

        return components;
    }

    bool reach(int x, int y)
    {
        // short circuit, if these two vertices are directly connected
        if (adj(x, y) != 0) {
            return true;
        }

        // clear the visitor tags, just in case
        clear_visitation();

        // explore the graph to find out if they are connected
        explore(x, 0);

        // if the target vertex been visited then they are connected
        return vertices[static_cast<size_t>(y)].visited;
    }
};
