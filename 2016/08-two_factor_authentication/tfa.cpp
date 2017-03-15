#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>


using Strings = std::vector<std::string>;
Strings read_input(std::string in_file);


template <size_t Rows, size_t Cols>
struct Bitmap
{
	std::array<bool, Rows * Cols> bits;

	Bitmap()
	{
		for (auto& bit : bits)
			bit = false;
	}

	size_t count_lit() const
	{
		size_t count = 0;
		for (auto bit : bits)
			if (bit)
				++count;

		return count;
	}

	void draw() const
	{
		for (size_t row = 0; row < Rows; ++row) {
			for (size_t col = 0; col < Cols; ++col) {
				auto pixel = bits[row * Cols + col];
				std::cout << (pixel ? '#' : '.');
			}
			std::cout << '\n';
		}
	}


	void rotate_row(size_t row, size_t count)
	{
		// std::cout << "\n+ rotate_row row " << row << " count " << count << '\n';

		const size_t row_off = row * Cols;
		
		for (size_t iteration = 0; iteration < count; ++iteration) {
			// save the bit from the last column
			auto saved_bit = bits[row_off + Cols - 1];

			// move bits over one column
			for (size_t col = Cols - 1; col > 0; --col) {
				bits[row_off + col] = bits[row_off + col - 1];
			}

			// place the bit from the last column in the first column
			bits[row_off + 0] = saved_bit;
		}
	}

	void rotate_column(size_t column, size_t count)
	{
		// std::cout << "\n+ rotate_column column " << column << " count " << count << '\n';

		for (size_t iteration = 0; iteration < count; ++iteration) {
			// save the bit from the last row
			auto saved_bit = bits[(Rows - 1) * Cols + column];

			// move bits down one row
			for (size_t row = Rows - 1; row > 0; --row) {
				bits[row * Cols + column] = bits[(row - 1) * Cols + column];
			}

			// place the bit from the last row on the top row
			bits[column] = saved_bit;
		}
	}

	void rect(size_t height, size_t width)
	{
		// std::cout << "\n+ rect height=" << height << " width=" << width << '\n';

		for (size_t row = 0; row < height; ++row) {
			for (size_t col = 0; col < width; ++col) {
				bits[row * Cols + col] = true;
			}
		}
	}
};


template <size_t R, size_t C>
void process_command(std::string cmd, Bitmap<R, C>& bmp)
{
	if (cmd.find("rect ") == 0) {
		size_t width = static_cast<size_t>(std::stoi(cmd.substr(5)));
		auto pos_x = cmd.find('x');
		size_t height = static_cast<size_t>(std::stoi(cmd.substr(pos_x + 1)));
		bmp.rect(height, width);
	}
	else if (cmd.find("rotate row") == 0) {
		size_t row = static_cast<size_t>(std::stoi(cmd.substr(13)));
		auto pos_by = cmd.find(" by ");
		size_t count = static_cast<size_t>(std::stoi(cmd.substr(pos_by + 4)));
		bmp.rotate_row(row, count);
	}
	else if (cmd.find("rotate column") == 0) {
		size_t column = static_cast<size_t>(std::stoi(cmd.substr(16)));
		auto pos_by = cmd.find(" by ");
		size_t count = static_cast<size_t>(std::stoi(cmd.substr(pos_by + 4)));
		bmp.rotate_column(column, count);
	}
	else {
		throw std::runtime_error("invalid command");
	}
}


Strings read_input(std::string in_file)
{
    Strings input;
    std::ifstream in(in_file);

    std::string line;
    while (in) {
	    std::getline(in, line);
	    if (!line.empty())
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

    Bitmap<6, 50> bmp;

    // std::cout << "* initial state\n";
    // bmp.draw();

    for (auto cmd : input) {
	    process_command(cmd, bmp);
	    // bmp.draw();
    }

    auto pixels_lit = bmp.count_lit();

    std::cout << "pixels_lit " << pixels_lit << '\n';

    return EXIT_SUCCESS;
}
