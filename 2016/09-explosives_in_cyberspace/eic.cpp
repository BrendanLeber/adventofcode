#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>


std::string decompress(std::string input);


std::string decompress(std::string input)
{
	return input;
}


int main(int, char**)
{
	std::string input;
	std::getline(std::cin, input);

	auto output = decompress(input);

	std::cerr
		<< "input " << input << '\n'
		<< "output " << output << '\n';

	std::cout << "decompressed_length " << output.length() << "\n";

	return EXIT_SUCCESS;
}
