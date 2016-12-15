#include <algorithm>
#include <array>
#include <iostream>

int main(int /*argc*/, char** /*argv*/)
{
    using Triangle = std::array<int, 3>;

    int possible = 0;
    Triangle tri{{0, 0, 0}};
    while (std::cin >> tri[0] >> tri[1] >> tri[2]) {
        std::sort(std::begin(tri), std::end(tri));
        if (tri[0] + tri[1] > tri[2]) {
            ++possible;
        }
    }

    std::cout << possible << '\n';

    return 0;
}
