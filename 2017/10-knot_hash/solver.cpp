#include <iostream>
#include <string>
#include <tuple>
#include <vector>

using List = std::vector<int>;

std::tuple<int, int> solver(List const& lengths);

std::tuple<int, int> solver(List const& lengths)
{
    return std::make_tuple(-1, -1);
}

int main()
{
    // load data from stdin
    List lengths;
    std::string value;
    while (std::cin) {
        std::getline(std::cin, value, ',');
        lengths.push_back(std::stoi(value));
    }

    // solve problems
    auto[part_1, part_2] = solver(lengths); // NOLINT

    // display result
    std::cout
        << "Part 1: " << part_1 << '\n'
        << "Part 2: " << part_2 << '\n';

    return 0;
}
