#include <cmath>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

using Row = std::vector<int>;
using Sheet = std::vector<Row>;

int corruption_checksum(Sheet const& sheet);

int corruption_checksum(Sheet const& sheet)
{
    int checksum = 0;

#if defined(PART_TWO)
    for (auto const& row : sheet) {
        bool found = false;
        int lo = 0, hi = 0;
        for (size_t i = 0; !found && i < row.size(); ++i) {
            for (size_t j = i + 1; !found && j < row.size(); ++j) {
                lo = std::min(row[i], row[j]);
                hi = std::max(row[i], row[j]);
                auto d = std::div(hi, lo);
                if (d.rem == 0) {
                    found = true;
                }
            }
        }

        if (found) {
            checksum += hi / lo;
        } else {
            std::cerr << "match not found!\n";
        }
    }
#else
    for (auto const& row : sheet) {
        int low = std::numeric_limits<int>::max();
        int high = std::numeric_limits<int>::min();

        for (auto const& value : row) {
            low = std::min(low, value);
            high = std::max(high, value);
        }

        checksum += high - low;
    }
#endif

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

    std::cout << corruption_checksum(sheet) << '\n';

    return 0;
}
