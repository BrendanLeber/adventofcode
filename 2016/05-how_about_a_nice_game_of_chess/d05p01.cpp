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
    std::string password;
    int index = 0;
    
    do {
        auto hash = md5(input + std::to_string(index));
        if (hash.compare(0, start.length(), start) == 0) {
            auto ch = hash[5];
            password.push_back(ch);
            std::cout << index << ' ' << ch << ' ' << password << std::endl;
        }

        ++index;        
    } while (password.length() < 8);

    std::cout << password << '\n';

    return EXIT_SUCCESS;
}
