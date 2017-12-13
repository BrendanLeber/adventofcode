#include <algorithm>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

#include "graph.hpp"

using Pipe_List = std::vector<int>;
using Pipe_Map = std::map<int, Pipe_List>;

void dump_pipe_map(Pipe_Map const& pmap);
void graph_pipe_map(Pipe_Map const& pmap);
std::tuple<int, int> solver(Pipe_Map const& pmap);

void dump_pipe_map(Pipe_Map const& pmap)
{
    for (auto && [ pgm_id, pipes ] : pmap) {
        bool first = true;
        std::cerr << pgm_id << " <->";
        for (auto pipe : pipes) {
            if (first) {
                std::cerr << ' ';
                first = false;
            }
            else {
                std::cerr << ", ";
            }
            std::cerr << pipe;
        }
        std::cerr << '\n';
    }
}

void graph_pipe_map(Pipe_Map const& pmap)
{
    std::cerr << "digraph {\n";

    for (auto && [ pgm_id, pipes ] : pmap) {
        for (auto pipe : pipes) {
            std::cerr << "    " << pgm_id << " -> " << pipe << ";\n";
        }
    }

    std::cerr << "}\n";
}

std::tuple<int, int> solver(Pipe_Map const& pmap)
{
    // graph_pipe_map(pmap);

    Graph graph(static_cast<int>(pmap.size()));
    for (auto && [ pgm_id, pipes ] : pmap) {
        graph.connect(pgm_id, pgm_id);
        for (auto pipe : pipes) {
            graph.connect(pgm_id, pipe);
        }
    }

    int connects_to_zero = 0;
    for (int v = 0; v < static_cast<int>(pmap.size()); ++v) {
        if (graph.reach(0, v)) {
            ++connects_to_zero;
        }
    }

    auto num_components = graph.number_of_components();

    return std::make_tuple(connects_to_zero, num_components);
}

int main()
{
    Pipe_Map pmap;

    // load data from stdin
    int pgm_id;
    while (std::cin >> pgm_id) {
        std::string line;
        std::cin >> line; // eat the <-> marker
        std::getline(std::cin, line);

        Pipe_List pipes;
        std::istringstream iss(line);
        while (!iss.eof()) {
            std::string pipe;
            std::getline(iss, pipe, ',');
            pipes.push_back(std::stoi(pipe));
        }

        pmap[pgm_id] = pipes;
    }

    // solve problems
    auto[part_1, part_2] = solver(pmap); // NOLINT

    // display result
    std::cout
        << "Part 1: " << part_1 << '\n'
        << "Part 2: " << part_2 << '\n';

    return 0;
}
