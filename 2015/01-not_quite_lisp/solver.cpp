#include <iostream>
#include <string>
#include <utility>

std::pair<int, int> solve(std::string instructions);

std::pair<int, int> solve(std::string instructions)
{
    int floor = 0;
    int found_pos = 0, pos = 1;
    for (auto ch : instructions) {
        floor += (ch == '(') ? 1 : -1;
        if (found_pos == 0 && floor == -1) {
            found_pos = pos;
        }
        ++pos;
    }

    return std::make_pair(floor, found_pos);
}

int main()
{
    // load data from stdin
    std::string input;
    std::getline(std::cin, input);

    // solve problems
    auto[part_1, part_2] = solve(input); // NOLINT

    // display result
    std::cout << "Part 1: " << part_1 << '\n'
              << "Part 2: " << part_2 << '\n';

    return 0;
}
