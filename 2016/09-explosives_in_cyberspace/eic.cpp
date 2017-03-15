#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>


std::string decompress(std::string input);


std::string decompress(std::string input)
{
	std::string output;

	while (!input.empty()) {
		// std::cerr << "string " << input << '\n';

		if (input[0] != '(') {
			auto end = input.find('(');

			auto segment = input.substr(0, end);
			// std::cerr << "segment " << segment << '\n';

			output.append(segment);
			input.erase(0, end);
		}
		else {
			auto end = input.find(')');
			auto marker = input.substr(1, end - 1);
			input.erase(0, end + 1);

			// std::cerr << "marker " << marker << '\n';

			auto num_chars = std::stoi(marker);
			end = marker.find('x');
			auto num_times = std::stoi(marker.substr(end + 1));

			auto repeat = input.substr(0, num_chars);
			input.erase(0, num_chars);

			// std::cerr << "chars " << num_chars << " times " << num_times << " repeat " << repeat << '\n';

			for (int i = 0; i < num_times; ++i)
				output.append(repeat);
		}
	}

	return output;
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
