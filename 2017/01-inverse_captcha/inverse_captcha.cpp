#include <iostream>
#include <string>
#include <vector>

using Digits = std::vector<int>;

int inverse_captcha(Digits const& digits);

int inverse_captcha(Digits const& /*digits*/)
{
    return 0;
}

int main(int /*argc*/, char** /*argv*/)
{
    std::string input;
    std::cin >> input;

    std::cerr << "input length: " << input.size() << '\n';

    Digits digits;
    std::cout << inverse_captcha(digits) << '\n';

    return 0;
}
