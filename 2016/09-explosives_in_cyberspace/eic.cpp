#include <algorithm>
#include <iostream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>


size_t decompress(std::string input);
size_t decompress2(std::string input);
std::tuple<size_t, size_t> parse_marker(std::string marker);


std::tuple<size_t, size_t> parse_marker(std::string marker)
{
	auto c_end = marker.find('x');
	auto chars = marker.substr(1, c_end - 1);
	auto num_chars = static_cast<size_t>(std::stoi(chars));

	auto r_start = c_end + 1;
	auto r_end = marker.find(')');
	auto repeat = marker.substr(r_start, r_end - r_start);
	auto num_repeat = static_cast<size_t>(std::stoi(repeat));

	return std::make_tuple(num_chars, num_repeat);
}


size_t decompress(std::string input)
{
	size_t length = 0;
	std::string::size_type start = 0, end = 0;

	while (start <= input.length()) {
		if (input[start] != '(') {
			end = input.find('(', start);
			if (end == std::string::npos) {
				length += input.length() - start;
				return length;
			}
			else {
				length += end - start;
				start = end;
			}
		}
		else {
			end = input.find(')', start);
			auto marker = input.substr(start, end - start + 1);

			size_t num_chars, num_repeat;
			std::tie(num_chars, num_repeat) = parse_marker(marker);

			length += num_repeat * num_chars;

			start = end + num_chars + 1;
		}
	}

	return length;
}


size_t decompress2(std::string /*input*/)
{
	return 0;
}


int main(int, char**)
{
	std::string input;
	std::getline(std::cin, input);

	auto length = decompress(input);

	std::cout << length << "\n";

	return EXIT_SUCCESS;
}
