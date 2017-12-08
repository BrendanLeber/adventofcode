#include <algorithm>
#include <cmath>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

using Row = std::vector<int>;
using Sheet = std::vector<Row>;

int part_1(Sheet const& sheet);
int part_2(Sheet const& sheet);

int part_1(Sheet const& sheet)
{
    int checksum = 0;

    for (auto const& row : sheet) {
        auto lo_hi = std::minmax_element(std::begin(row), std::end(row));
        checksum += *lo_hi.second - *lo_hi.first;
    }

    return checksum;
}

int part_2(Sheet const& sheet)
{
    int checksum = 0;

    for (auto const& row : sheet) {
        int lo = 0, hi = 0;
        for (size_t i = 0; i < row.size(); ++i) {
            for (size_t j = i + 1; j < row.size(); ++j) {
                lo = std::min(row[i], row[j]);
                hi = std::max(row[i], row[j]);
                auto d = std::div(hi, lo);
                if (d.rem == 0) {
                    checksum += hi / lo;
                }
            }
        }
    }

    return checksum;
}

int main()
{
    Sheet sheet;
    std::string line;
    Row row;
    while (std::getline(std::cin, line)) {
        std::istringstream str(line);
        row.clear();

        int value;
        while (str >> value) {
            row.emplace_back(value);
        }

        sheet.emplace_back(row);
    }

    std::cout << "Part 1: " << part_1(sheet) << '\n';
    std::cout << "Part 2: " << part_2(sheet) << '\n';

    return 0;
}
