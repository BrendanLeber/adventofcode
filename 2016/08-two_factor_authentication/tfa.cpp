#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>


const size_t Num_Rows = 6;
const size_t Num_Cols = 50;

using Bitmap = std::array<bool, Num_Rows * Num_Cols>;
using Strings = std::vector<std::string>;


void bmp_initialize(Bitmap& bmp);
size_t bmp_count_lit(const Bitmap& bmp);
void bmp_draw(const Bitmap& bmp);
Strings read_input(std::string in_file);


size_t bmp_count_lit(const Bitmap& bmp)
{
	size_t count = 0;
	for (auto bit : bmp)
		if (bit)
			++count;

	return count;
}


void bmp_draw(const Bitmap& bmp)
{
	for (size_t row = 0; row < Num_Rows; ++row) {
		for (size_t col = 0; col < Num_Cols; ++col) {
			auto pixel = bmp[row * Num_Cols + col];
			std::cout << (pixel ? '#' : '.');
		}
		std::cout << '\n';
	}
}


void bmp_initialize(Bitmap& bmp)
{
	for (auto& bit : bmp)
		bit = false;
}


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

    Bitmap bmp;
    bmp_initialize(bmp);

    std::cout << "* initial state\n";
    bmp_draw(bmp);

    for (auto cmd : input) {
	    // process comand
	    // draw bitmap?
    }

    auto pixels_lit = bmp_count_lit(bmp);
    
    std::cout << "pixels lit " << pixels_lit << '\n';

    return EXIT_SUCCESS;
}
