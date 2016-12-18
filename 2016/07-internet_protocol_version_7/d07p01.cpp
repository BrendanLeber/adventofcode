#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>

using Strings = std::vector<std::string>;

Strings read_input(std::string in_file);

Strings read_input(std::string in_file)
{
    Strings input;
    std::ifstream in(in_file);

    std::string line;
    while (in >> line) {
        input.push_back(line);
    }

    return input;
}

int main(int argc, char** argv)
{
    Strings args(argv, argv + argc);
    if (argc != 2) {
        std::cout << "Syntax: " << args[0] << " <input>\n";
        return EXIT_FAILURE;
    }

    auto input = read_input(args[1]);
    
    return EXIT_SUCCESS;
}
