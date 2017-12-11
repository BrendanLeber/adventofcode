#include <iostream>
#include <tuple>

std::tuple<int, int> solver();

std::tuple<int, int> solver()
{
    return std::make_tuple(-1, -1);
}

int main()
{
    // load data from stdin

    // solve problems
    auto[part_1, part_2] = solver(); // NOLINT

    // display result
    std::cout
        << "Part 1: " << part_1 << '\n'
        << "Part 2: " << part_2 << '\n';

    return 0;
}
