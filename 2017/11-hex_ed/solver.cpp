#include <cmath>
#include <iostream>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

using Move = std::string;
using Moves = std::vector<Move>;
using Position = std::pair<int, int>;

std::tuple<int, int> solver(Moves const& moves);

std::tuple<int, int> solver(Moves const& moves)
{
	// x = first; y = second
	auto pos = std::make_pair(0, 0);

	for (auto const& move : moves) {
		if (move == "n") {
			pos.second += 1;
		}
		else if (move == "ne") {
			pos.first += 1;
			pos.second += 1;
		}
		else if (move == "se") {
			pos.first += 1;
			pos.second -= 1;
		}
		else if (move == "s") {
			pos.second -= 1;
		}
		else if (move == "sw") {
			pos.first -= 1;
			pos.second -= 1;
		}
		else if (move == "nw") {
			pos.first -= 1;
			pos.second += 1;
		}
	}

	auto dist = std::abs(pos.first) + std::abs(pos.second);

	return std::make_tuple(dist, -1);
}

int main()
{
    Moves moves;

    // load data from stdin
    std::string line;
    std::getline(std::cin, line);
    std::istringstream iss(line);
    while (!iss.eof()) {
	    std::string move;
            std::getline(iss, move, ',');
            moves.push_back(move);
    }
    
    // solve problems
    auto[part_1, part_2] = solver(moves); // NOLINT

    // display result
    std::cout
        << "Part 1: " << part_1 << '\n'
        << "Part 2: " << part_2 << '\n';

    return 0;
}
