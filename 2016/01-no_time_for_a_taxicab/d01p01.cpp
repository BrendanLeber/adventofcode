#include <cassert>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <set>
#include <string>
#include <utility>

using Position = std::pair<int, int>;
using Past_Positions = std::set<Position>;

int taxicab_distance(Position p, Position q)
{
    return std::abs(p.first - q.first) + std::abs(p.second - q.second);
}

template <int Lower, int Upper>
int wrap(int x)
{
    auto range = Upper - Lower + 1;
    if (x < Lower) {
        x += range * ((Lower - x) / range + 1);
    }
    return Lower + (x - Lower) % range;
}

int main(int /*argc*/, char** /*argv*/)
{
    Past_Positions past;

    // start at the origin and facing north
    auto pos = std::make_pair(0, 0);
    int heading = 0; // 0 = North, 1 = East, 2 = South, 3 = West

    char turn, bogus;
    int moves;
    while (std::cin >> turn >> moves) {
        std::cin >> bogus; // eat the extra ',' after each turn

        // turn left or right
        if (turn == 'L') {
            heading = wrap<0, 3>(heading - 1);
        } else if (turn == 'R') {
            heading = wrap<0, 3>(heading + 1);
        } else {
            std::cerr << "invalid turn '" << turn << "'\n";
            return -1;
        }

        switch (heading) {
        case 0:
            pos.second += moves;
            break;

        case 1:
            pos.first += moves;
            break;

        case 2:
            pos.second -= moves;
            break;

        case 3:
            pos.first -= moves;
            break;
        }
    }

    std::cout << taxicab_distance(std::make_pair(0, 0), pos) << '\n';

    return 0;
}
