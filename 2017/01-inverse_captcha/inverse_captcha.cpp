#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using Digits = std::vector<int>;

int inverse_captcha(Digits const& digits);

int inverse_captcha(Digits const& digits)
{
    int sum = 0;
    for (auto it = std::begin(digits); it != std::end(digits); ++it) {
        if (*it == *(it + 1)) {
            sum += *it;
        }
    }

    if (digits.front() == digits.back()) {
        sum += digits.front();
    }

    return sum;
}

int main(int /*argc*/, char** /*argv*/)
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

    std::cerr << "input length: " << digits.size() << '\n';

    std::cout << inverse_captcha(digits) << '\n';

    return 0;
}
