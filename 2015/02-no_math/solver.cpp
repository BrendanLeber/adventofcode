#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

// length, width, height
using Dimensions = std::tuple<int, int, int>;
using Packages = std::vector<Dimensions>;

std::pair<int, int> solve(Packages const& packages);

std::pair<int, int> solve(Packages const& packages)
{
    int total_paper = 0, total_ribbon = 0;
    for (auto const& package : packages) {
        auto[l, w, h] = package;

        std::array<int, 3> faces{ { 0, 0, 0 } };
        faces[0] = w * h;
        faces[1] = l * h;
        faces[2] = w * l;

        auto extra = *std::min_element(std::begin(faces), std::end(faces));

        auto paper = 0;
        for (auto a : faces) {
            paper += 2 * a;
        }

        total_paper += paper + extra;

        std::array<int, 3> perimiters{ { 0, 0, 0 } };
        perimiters[0] = 2 * (w + h);
        perimiters[1] = 2 * (l + h);
        perimiters[2] = 2 * (w + l);

        auto wrap = *std::min_element(std::begin(perimiters), std::end(perimiters));
        auto bow = w * l * h;

        total_ribbon += wrap + bow;
    }

    return std::make_pair(total_paper, total_ribbon);
}

int main()
{
    // load data from stdin
    Packages packages;
    std::string line;
    while (std::cin >> line) {
        size_t cch = 0, pos = 0;
        auto l = std::stoi(line.data() + pos, &cch); // NOLINT
        pos += cch + 1;
        auto w = std::stoi(line.data() + pos, &cch); // NOLINT
        pos += cch + 1;
        auto h = std::stoi(line.data() + pos, &cch); // NOLINT
        packages.emplace_back(std::make_tuple(l, w, h));
    }

    // solve problems
    auto[part_1, part_2] = solve(packages); // NOLINT

    // display result
    std::cout << "Part 1: " << part_1 << '\n'
              << "Part 2: " << part_2 << '\n';

    return 0;
}
