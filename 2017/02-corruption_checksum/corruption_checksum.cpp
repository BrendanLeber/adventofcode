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

    for (auto const& row : sheet) {
        int low = std::numeric_limits<int>::max();
        int high = std::numeric_limits<int>::min();

        for (auto const& value : row) {
            low = std::min(low, value);
            high = std::max(high, value);
        }

        checksum += high - low;
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

    std::cout << corruption_checksum(sheet) << '\n';

    return 0;
}
