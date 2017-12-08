#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using Digits = std::vector<int>;

int part_1(Digits const& digits);
int part_2(Digits const& digits);

int part_1(Digits const& digits)
{
    int sum = 0;
    size_t pos, wrap;
    size_t const size = digits.size();
    for (pos = 0, wrap = 1; pos < size; ++pos, wrap = (wrap + 1) % size) {
        if (digits[pos] == digits[wrap]) {
            sum += digits[pos];
        }
    }

    return sum;
}

int part_2(Digits const& digits)
{
    int sum = 0;
    //size_t pos, wrap;
    size_t const size = digits.size();
    for (size_t pos = 0, wrap = size / 2; pos < size; ++pos, wrap = (wrap + 1) % size) {
        if (digits[pos] == digits[wrap]) {
            sum += digits[pos];
        }
    }

    return sum;
}

int main()
{
    std::string input;
    std::cin >> input;

    Digits digits;
    digits.reserve(input.size());
    for (auto digit : input) {
        if (std::isdigit(static_cast<unsigned char>(digit)) != 0) {
            digits.push_back(static_cast<int>(digit) - '0');
        }
    }

    std::cout << "Part 1: " << part_1(digits) << '\n';
    std::cout << "Part 2: " << part_2(digits) << '\n';

    return 0;
}
