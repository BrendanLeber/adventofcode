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
        if (rows != cols) {
            throw std::range_error("rows != cols");
        }

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
};


struct Site
{
};


using Depth_Range = std::pair<int, int>;
using Depth_Ranges = std::vector<Depth_Range>;

void dump_depth_ranges(Depth_Ranges const& drs);
void dump_state();
std::tuple<int, int> solver(Depth_Ranges const& drs);

void dump_depth_ranges(Depth_Ranges const& drs)
{
    for (auto const& dr : drs) {
	std::cerr << dr.first << ": " << dr.second << '\n';
    }
}

void dump_state()
{
}

std::tuple<int, int> solver(Depth_Ranges const& drs)
{
    // dump_depth_ranges(drs);

    auto max_depth = std::max_element(std::begin(drs), std::end(drs),
      [](Depth_Range const& a, Depth_Range const& b) -> int {
	  return a.first < b.first;
      })->first;

    // std::cerr << "max_depth " << max_depth << '\n';

    auto max_range = std::max_element(std::begin(drs), std::end(drs),
      [](Depth_Range const& a, Depth_Range const& b) -> int {
	  return a.second < b.second;
      })->second;

    // std::cerr << "max_range " << max_range << '\n';

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
