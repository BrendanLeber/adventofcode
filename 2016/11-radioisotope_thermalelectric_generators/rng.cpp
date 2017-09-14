#include <iostream>
#include <string>
#include <vector>

using Strings = std::vector<std::string>;

int main()
{
    Strings input;
    while (std::cin) {
        std::string line;
        std::getline(std::cin, line);
        if (!line.empty()) {
            input.push_back(line);
        }
    }

    return EXIT_SUCCESS;
}
