#include <cassert>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <set>
#include <string>
#include <utility>


// template <typename T, size_t N>
// struct Vector
// {
// 	size_t sz;
// 	T data[N];

// 	Vector() : sz(N) {
// 		for (size_t i = 0; i < N; ++i) {
// 			data[i] = T();
// 		}
// 	}
// };


// using Position = Vector<int, 2>;


using Position = std::pair<int, int>;
using Past_Positions = std::set<Position>;


int taxicab_distance(Position p, Position q)
{
    return std::abs(p.first - q.first) + std::abs(p.second - q.second);
}


template <int L, int U>
int wrap(int x)
{
    auto range = U - L + 1;
    if (x < L) {
        x += range * ((L - x) / range + 1);
    }
    return L + (x - L) % range;
}


int main(int, char**)
{
    Past_Positions past;
    auto pos = std::make_pair(0, 0);
    int heading = 0;  // 0 = North, 1 = East, 2 = South, 3 = West

    char turn, bogus;
    int moves;
    while (std::cin >> turn >> moves) {
        std::cin >> bogus;  // eat the extra ',' after each turn

        assert(turn == 'R' || turn == 'L');

        // std::cout << "pos (" << pos.first << ", " << pos.second << ")  heading " << heading;
        // std::cout << "  turn " << turn << "  moves " << moves;

        // turn left or right
        if (turn == 'L') {
            heading = wrap<0, 3>(heading - 1);
        }
        else {
            heading = wrap<0, 3>(heading + 1);
        }

        for (int move = 0; move < moves; ++move) {
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

            auto found = past.insert(pos);
            if (!found.second) {
                std::cout
                    << "repeated pos (" << pos.first << ", " << pos.second << ")\n"
                    << "distance " << taxicab_distance(std::make_pair(0, 0), pos)
                    << std::endl;
                return 0;
            }
        }

        // std::cout << "  pos (" << pos.first << ", " << pos.second << ")  heading " << heading << std::endl;
    }

    std::cout
        << "final pos (" << pos.first << ", " << pos.second << ")\n"
        << "distance " << taxicab_distance(std::make_pair(0, 0), pos)
        << std::endl;

    return 0;
}
