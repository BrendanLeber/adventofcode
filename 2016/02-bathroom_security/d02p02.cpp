#include <array>
#include <cstdlib>
#include <iostream>
#include <string>
#include <utility>

using Position = std::pair<size_t, size_t>;

constexpr size_t grid_size = 7;

const std::array<char, grid_size * grid_size> keypad{{0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, '1', 0, 0, 0,
    0, 0, '2', '3', '4', 0, 0,
    0, '5', '6', '7', '8', '9', 0,
    0, 0, 'A', 'B', 'C', 0, 0,
    0, 0, 0, 'D', 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0}};

size_t pos_to_offset(Position pos);
Position update_pos(char move, Position pos);

size_t pos_to_offset(Position pos)
{
    return pos.second * grid_size + pos.first;
}

Position update_pos(char move, Position pos)
{
    Position new_pos{pos};

    switch (move) {
    case 'U':
        new_pos.second--;
        break;

    case 'D':
        new_pos.second++;
        break;

    case 'L':
        new_pos.first--;
        break;

    case 'R':
        new_pos.first++;
        break;

    default:
        std::cerr << "invalid move '" << move << "'\n";
        std::exit(EXIT_FAILURE);
    }

    return new_pos;
}

int main(int /*argc*/, char** /*argv*/)
{
    // pos.first = col  pos.second = row
    auto pos = std::make_pair(1, 3); // start at '5'

    std::string moves, code;
    while (std::cin >> moves) {
        for (auto move : moves) {
            auto new_pos = update_pos(move, pos);
            auto key = keypad[pos_to_offset(new_pos)];
            if (key != '\0') {
                pos = new_pos;
            }
        }

        code.push_back(keypad[pos_to_offset(pos)]);
    }

    std::cout << code << '\n';

    return EXIT_SUCCESS;
}
