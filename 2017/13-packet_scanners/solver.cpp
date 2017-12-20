#include <algorithm>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

template <typename T>
class Matrix {
public:
    std::vector<T> inner;
    size_t rows, cols;

    Matrix(size_t c, size_t r) : rows(r), cols(c)
    {
        // if (rows != cols) {
        //     throw std::range_error("rows != cols");
        // }

        inner.resize(rows * cols);
    }

    T& operator()(size_t col, size_t row)
    {
        if (row >= rows) {
            throw std::range_error("row outside of matrix size");
        }
        else if (col >= cols) {
            throw std::range_error("col outside of matrix size");
        }

        return inner[cols * row + col];
    }

    T const& operator()(size_t col, size_t row) const
    {
        if (row >= rows) {
            throw std::range_error("row outside of matrix size");
        }
        else if (col >= cols) {
            throw std::range_error("col outside of matrix size");
        }

        return inner[cols * row + col];
    }
};

struct Site
{
	bool valid = false;
	bool scanner = false;
	bool packet = false;
};

using Sites = Matrix<Site>;

using Scanners = std::vector<size_t>;

using Depth_Range = std::pair<int, int>;
using Depth_Ranges = std::vector<Depth_Range>;

void dump_depth_ranges(Depth_Ranges const& drs);
void dump_sites(Sites const& sites, Scanners const& scanners, size_t packet);
std::tuple<int, int> solver(Depth_Ranges const& drs);

void dump_depth_ranges(Depth_Ranges const& drs)
{
    for (auto const& dr : drs) {
	std::cerr << dr.first << ": " << dr.second << '\n';
    }
}

void dump_sites(Sites const& sites, Scanners const& scanners, size_t packet)
{
	for (size_t col = 0; col < sites.cols; ++col) {
		std::cout << ' ' << col << "  ";
	}
	std::cout << '\n';

	for (size_t row = 0; row < sites.rows; ++row) {
		for (size_t col = 0; col < sites.cols; ++col) {
			if (!sites(col, row).valid) {
				std::cout << "...";
			}
			else {
				if (row == 0 && col == packet) {
					std::cout << '(';
				}
				else {
					std::cout << '[';
				}
				if (scanners[col] == row) {
					std::cout << 'S';
				}
				else {
					std::cout << ' ';
				}
				if (row == 0 && col == packet) {
					std::cout << ')';
				}
				else {
					std::cout << ']';
				}
			}
			std::cout << ' ';
		}
		std::cout << '\n';
	}
}

std::tuple<int, int> solver(Depth_Ranges const& drs)
{
    // dump_depth_ranges(drs);

    auto max_depth = std::max_element(std::begin(drs), std::end(drs),
      [](Depth_Range const& a, Depth_Range const& b) -> int {
	  return a.first < b.first;
      })->first + 1;

    auto max_range = std::max_element(std::begin(drs), std::end(drs),
      [](Depth_Range const& a, Depth_Range const& b) -> int {
	  return a.second < b.second;
	})->second;

    auto sites = Sites(static_cast<size_t>(max_depth), static_cast<size_t>(max_range));
    for (auto const& dr : drs) {
	    for (size_t row = 0; row < static_cast<size_t>(dr.second); ++row) {
		    sites(static_cast<size_t>(dr.first), row).valid = true;
	    }
    }

    Scanners scanners(static_cast<size_t>(max_depth));
    size_t packet = 0;
    dump_sites(sites, scanners, packet);

    // for (auto scanner : scanners) {
    // 	    if (scanner.second == 0) {
    // 		    continue;  // skip, empty column
    // 	    }

    // 	    if (scanner.first == 0) {
    // 		    scanner.second = 1;
    // 	    }
    // 	    else if (scanner.first ==
    // 	    scanner.first +=


    return std::make_tuple(-1, -1);
}

int main()
{
    Depth_Ranges drs;

    // load data from stdin
    std::string depth, range;
    while (std::cin >> depth >> range) {
	drs.push_back(std::make_pair(std::stoi(depth), std::stoi(range)));
    }

    // solve problems
    auto[part_1, part_2] = solver(drs); // NOLINT

    // display result
    std::cout
        << "Part 1: " << part_1 << '\n'
        << "Part 2: " << part_2 << '\n';

    return 0;
}
