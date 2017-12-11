#include <cstdlib>
#include <iostream>
#include <set>
#include <utility>
#include <vector>

using Move = std::pair<char, int>;
using Moves = std::vector<Move>;
using Position = std::pair<int, int>;
using Past_Positions = std::set<Position>;

template <int Lower, int Upper>
int wrap(int x)
{
    auto range = Upper - Lower + 1;
    if (x < Lower) {
        x += range * ((Lower - x) / range + 1);
    }
    return Lower + (x - Lower) % range;
}

int part_1(Moves const& moves);
int part_2(Moves const& moves);
int taxicab_distance(Position p, Position q);

int part_1(Moves const& moves)
{
    // start at the origin and facing north
    auto pos = std::make_pair(0, 0);
    int heading = 0; // 0 = North, 1 = East, 2 = South, 3 = West

    for (auto && [ turn, steps ] : moves) {
        // turn left or right
        if (turn == 'L') {
            heading = wrap<0, 3>(heading - 1);
        }
        else if (turn == 'R') {
            heading = wrap<0, 3>(heading + 1);
        }
        else {
            std::cerr << "invalid turn '" << turn << "'\n";
            return -1;
        }

        switch (heading) {
        case 0:
            pos.second += steps;
            break;

        case 1:
            pos.first += steps;
            break;

        case 2:
            pos.second -= steps;
            break;

        case 3:
            pos.first -= steps;
            break;
        }
    }

    return taxicab_distance(std::make_pair(0, 0), pos);
}

int part_2(Moves const& moves)
{
    Past_Positions past;

    // start at the origin and facing north
    auto pos = std::make_pair(0, 0);
    int heading = 0; // 0 = North, 1 = East, 2 = South, 3 = West

    for (auto && [ turn, steps ] : moves) {
        // turn left or right
        if (turn == 'L') {
            heading = wrap<0, 3>(heading - 1);
        }
        else if (turn == 'R') {
            heading = wrap<0, 3>(heading + 1);
        }
        else {
            std::cerr << "invalid turn '" << turn << "'\n";
            return -1;
        }

        for (int step = 0; step < steps; ++step) {
            switch (heading) {
            case 0:
                pos.second += 1;
                break;

            case 1:
                pos.first += 1;
                break;

            case 2:
                pos.second -= 1;
                break;

            case 3:
                pos.first -= 1;
                break;
            }

            // stop if we've been here before
            auto found = past.insert(pos);
            if (!found.second) {
                return taxicab_distance(std::make_pair(0, 0), pos);
            }
        }
    }

    return -1;
}

int taxicab_distance(Position p, Position q)
{
    return std::abs(p.first - q.first) + std::abs(p.second - q.second);
}

int main(int /*argc*/, char** /*argv*/)
{
    char turn, bogus;
    int steps;
    Moves moves;
    while (std::cin >> turn >> steps) {
        std::cin >> bogus; // eat the extra ',' after each turn
        moves.emplace_back(std::make_pair(turn, steps));
    }

    std::cout << "Part 1: " << part_1(moves) << '\n';
    std::cout << "Part 2: " << part_2(moves) << '\n';

    return 0;
}
