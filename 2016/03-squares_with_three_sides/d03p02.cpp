#include <algorithm>
#include <array>
#include <deque>
#include <iostream>

int main(int /*argc*/, char** /*argv*/)
{
    using Triangle = std::array<int, 3>;
    using Triangle_List = std::deque<int>;

    int a, b, c;
    Triangle_List as, bs, cs;
    while (std::cin >> a >> b >> c) {
        as.push_back(a);
        bs.push_back(b);
        cs.push_back(c);
    }

    Triangle_List tris;
    tris.insert(std::end(tris), std::begin(as), std::end(as));
    tris.insert(std::end(tris), std::begin(bs), std::end(bs));
    tris.insert(std::end(tris), std::begin(cs), std::end(cs));

    int possible = 0;
    while (!tris.empty()) {
        Triangle tri{{0, 0, 0}};
        std::copy_n(std::begin(tris), 3, std::begin(tri));
        tris.erase(std::begin(tris), std::begin(tris) + 3);

        std::sort(std::begin(tri), std::end(tri));
        if (tri[0] + tri[1] > tri[2]) {
            ++possible;
        }
    }

    std::cout << possible << '\n';

    return 0;
}
