#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using Digits = std::vector<int>;

int inverse_captcha(Digits const& digits);

int inverse_captcha(Digits const& digits)
{
#if defined(PART_TWO)
    size_t const half = digits.size() / 2;
#else
    size_t const half = 1;
#endif

    int sum = 0;
    size_t pos, wrap;
    size_t const size = digits.size();
    for (pos = 0, wrap = half; pos < size; ++pos, wrap = (wrap + 1) % size) {
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

    std::cout << inverse_captcha(digits) << '\n';

    return 0;
}
