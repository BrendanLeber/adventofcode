#include <algorithm>
#include <iostream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>
#include <map>

using Strings = std::vector<std::string>;


int main(int, char**)
{
	Strings input;
	while (std::cin) {
		std::string line;
		std::getline(std::cin, line);
		if (!line.empty())
			input.push_back(line);
	}

	std::cout << input.size() << "\n";

	return EXIT_SUCCESS;
}
