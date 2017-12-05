#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>

constexpr bool enable_debug = false;

void dump_jumps(int pc, std::vector<int> const& jumps);
int solver_1(std::vector<int> jumps);
int solver_2(std::vector<int> jumps);

void dump_jumps(int pc, std::vector<int> const& jumps)
{
    for (size_t i = 0; i < jumps.size(); ++i) {
        if (i == static_cast<size_t>(pc)) {
            std::cerr << '(';
        }
        std::cerr << jumps[i];
        if (i == static_cast<size_t>(pc)) {
            std::cerr << ')';
        }
        std::cerr << ' ';
    }
    std::cerr << '\n';
}

int solver_1(std::vector<int> jumps)
{
    int num_steps = 0, offset = 0, pc = 0;
    auto const sz = static_cast<int>(jumps.size());
    while (pc >= 0 && pc < sz) {
        if constexpr (enable_debug) {
            dump_jumps(pc, jumps);
        }
        offset = jumps[static_cast<size_t>(pc)]++;
        pc += offset;
        ++num_steps;
    }

    if constexpr (enable_debug) {
        std::copy(std::begin(jumps), std::end(jumps),
            std::ostream_iterator<int>(std::cerr, " "));
        std::cerr << '\n';
    }

    return num_steps;
}

int solver_2(std::vector<int> jumps)
{
    int num_steps = 0, offset = 0, pc = 0;
    auto const sz = static_cast<int>(jumps.size());
    while (pc >= 0 && pc < sz) {
        if constexpr (enable_debug) {
            dump_jumps(pc, jumps);
        }

        offset = jumps[static_cast<size_t>(pc)];
        jumps[static_cast<size_t>(pc)] += (offset >= 3) ? -1 : 1;
        pc += offset;
        ++num_steps;
    }

    if constexpr (enable_debug) {
        std::copy(std::begin(jumps), std::end(jumps),
            std::ostream_iterator<int>(std::cerr, " "));
        std::cerr << '\n';
    }

    return num_steps;
}

int main()
{
    std::vector<int> jumps{ std::istream_iterator<int>{ std::cin }, {} };

    std::cout << "Part 1: " << solver_1(jumps) << '\n';
    std::cout << "Part 2: " << solver_2(jumps) << '\n';

    return 0;
}
