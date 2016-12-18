#include <iostream>
#include <string>
#include <vector>
#include "md5.hpp"

int main(int argc, char** argv)
{
    std::vector<std::string> args(argv, argv + argc);
    if (args.size() != 2) {
        std::cerr << "Syntax: " << args[0] << " <door-id>\n";
        return EXIT_FAILURE;
    }

    std::string input { args[1] };

    const std::string start { "00000" };
    std::string password { "--------" };
    int chars_left = 8;
    int index = 0;

    do {
        auto hash = md5(input + std::to_string(index));
        if (hash.compare(0, start.length(), start) == 0) {
            auto pos = hash[5];
            auto ch = hash[6];
            if (pos >= '0' && pos <= '7') {
                auto position = static_cast<size_t>(pos - '0');
                if (password[position] == '-') {
                    password[position] = ch;
                    chars_left--;
                    std::cout << index << ' ' << ch << ' ' << password << std::endl;
                }
            }
        }

        ++index;
    } while (chars_left);

    std::cout << password << '\n';

    return EXIT_SUCCESS;
}
