#include <cmath>
#include <cstdlib>
#include <iostream>
#include <set>
#include <string>
#include <utility>

char pos_to_key(std::pair<int, int> pos);

char pos_to_key(std::pair<int, int> pos)
{
    auto index = pos.second * 3 + pos.first;
    switch (index) {
    case 0:
        return '1';
    case 1:
        return '2';
    case 2:
        return '3';
    case 3:
        return '4';
    case 4:
        return '5';
    case 5:
        return '6';
    case 6:
        return '7';
    case 7:
        return '8';
    case 8:
        return '9';
    default:
        return 'x';
    }
}

int main(int /*argc*/, char** /*argv*/)
{
    // pos.first = col  pos.second = row
    auto pos = std::make_pair(1, 1); // start at '5'

    std::string moves, code;
    while (std::cin >> moves) {
        for (auto move : moves) {
            switch (move) {
            case 'U':
                if (pos.second > 0) {
                    pos.second--;
                }
                break;

            case 'D':
                if (pos.second < 2) {
                    pos.second++;
                }
                break;

            case 'R':
                if (pos.first < 2) {
                    pos.first++;
                }
                break;

            case 'L':
                if (pos.first > 0) {
                    pos.first--;
                }
                break;

            default:
                std::cerr << "inavlid move '" << move << "'\n";
                return -1;
            }
        }

        code.push_back(pos_to_key(pos));
    }

    std::cout << code << '\n';

    return 0;
}
