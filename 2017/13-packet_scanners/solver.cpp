#include <algorithm>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using Depth_Range = std::pair<int, int>;
using Depth_Ranges = std::vector<Depth_Range>;

std::tuple<int, int> solver(Depth_Ranges const& drs [[maybe_unused]]);

std::tuple<int, int> solver(Depth_Ranges const& drs [[maybe_unused]])
{
    return std::make_tuple(-1, -1);
}

int main()
{
    Depth_Ranges drs;

    // load data from stdin
    int depth, range;
    while (std::cin >> depth >> range) {
	    drs.push_back(std::make_pair(depth, range));;
    }

    // solve problems
    auto[part_1, part_2] = solver(drs); // NOLINT

    // display result
    std::cout
        << "Part 1: " << part_1 << '\n'
        << "Part 2: " << part_2 << '\n';

    return 0;
}
