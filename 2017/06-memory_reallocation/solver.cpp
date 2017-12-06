#include <algorithm>
#include <iostream>
#include <iterator>
#include <limits>
#include <vector>

bool is_repeat_state(std::vector<int> const& state, std::vector<int> const& banks);
void redistribute_blocks(std::vector<int>& banks); // NOLINT
int solver_1(std::vector<int> banks);
int solver_2(std::vector<int> banks);

bool is_repeat_state(std::vector<int> const& state, std::vector<int> const& banks)
{
    return std::equal(std::begin(state), std::end(state), std::begin(banks));
}

void redistribute_blocks(std::vector<int>& banks)
{
    // find position of bank with the highest block count
    size_t pos = 0;
    int blocks = std::numeric_limits<int>::min();
    for (size_t i = 0; i < banks.size(); ++i) {
        if (banks[i] > blocks) {
            blocks = banks[i];
            pos = i;
        }
    }

    // get the number of blocks in that bank and reset it to zero
    blocks = banks[pos];
    banks[pos] = 0;

    // redistribute the blocks among the other banks
    while (blocks > 0) {
        pos = (pos + 1) % banks.size();
        banks[pos] += 1;
        blocks -= 1;
    }
}

int solver_1(std::vector<int> banks)
{
    int num_steps = 0;
    std::vector<std::vector<int>> states;

    while (true) {
        ++num_steps;
        redistribute_blocks(banks);

        // have we seen this state before?
        for (auto const& state : states) {
            if (is_repeat_state(state, banks)) {
                return num_steps;
            }
        }

        states.push_back(banks);
    }
}

int solver_2(std::vector<int> banks)
{
    std::vector<std::vector<int>> states;

    while (true) {
        redistribute_blocks(banks);

        for (auto const& state : states) {
            if (std::equal(std::begin(state), std::end(state), std::begin(banks))) {
                int num_cycles = 0;
                while (true) {
                    ++num_cycles;
                    redistribute_blocks(banks);
                    if (is_repeat_state(state, banks)) {
                        return num_cycles;
                    }
                }
            }
        }

        states.push_back(banks);
    }
}

int main()
{
    std::vector<int> banks{ std::istream_iterator<int>{ std::cin }, {} };

    std::cout << "Part 1: " << solver_1(banks) << '\n';
    std::cout << "Part 2: " << solver_2(banks) << '\n';

    return 0;
}
