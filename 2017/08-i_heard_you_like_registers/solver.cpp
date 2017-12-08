#include <algorithm>
#include <iostream>
#include <iterator>
#include <limits>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wpadded"

struct Instruction {
    std::string reg;
    bool incr;
    int value;
    std::string creg;
    std::string cond;
    int cvalue;
};

#pragma clang diagnostic pop

using Instructions = std::vector<Instruction>;

std::tuple<int, int> solver(Instructions const& instructions);

std::tuple<int, int> solver(Instructions const& instructions)
{
    int max_value = std::numeric_limits<int>::min();
    std::map<std::string, int> rvalues;

    for (auto const& inst : instructions) {
        if (rvalues.find(inst.reg) == std::end(rvalues)) {
            rvalues[inst.reg] = 0;
        }

        if (rvalues.find(inst.creg) == std::end(rvalues)) {
            rvalues[inst.creg] = 0;
        }

        bool is_true = false;
        if (inst.cond == "<") {
            is_true = rvalues[inst.creg] < inst.cvalue;
        }
        else if (inst.cond == "<=") {
            is_true = rvalues[inst.creg] <= inst.cvalue;
        }
        else if (inst.cond == "==") {
            is_true = rvalues[inst.creg] == inst.cvalue;
        }
        else if (inst.cond == "!=") {
            is_true = rvalues[inst.creg] != inst.cvalue;
        }
        else if (inst.cond == ">=") {
            is_true = rvalues[inst.creg] >= inst.cvalue;
        }
        else if (inst.cond == ">") {
            is_true = rvalues[inst.creg] > inst.cvalue;
        }

        if (is_true) {
            if (inst.incr) {
                rvalues[inst.reg] += inst.value;
            }
            else {
                rvalues[inst.reg] -= inst.value;
            }
        }

        max_value = std::max(max_value, rvalues[inst.reg]);
    }

    using pair_type = decltype(rvalues)::value_type;
    auto maxit = std::max_element(std::begin(rvalues), std::end(rvalues),
        [](pair_type const& a, pair_type const& b) -> bool {
            return a.second < b.second;
        });

    return std::make_tuple(maxit->second, max_value);
}

int main()
{
    // load data from stdin
    Instructions instructions;
    std::string line;
    std::vector<std::string> parts;
    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);
        parts.clear();
        std::copy(std::istream_iterator<std::string>(iss),
            std::istream_iterator<std::string>(),
            std::back_inserter(parts));

        instructions.emplace_back(Instruction{
            parts[0],
            parts[1] == "inc",
            std::stoi(parts[2]),
            parts[4],
            parts[5],
            std::stoi(parts[6]) });
    }

    auto[part_1, part_2] = solver(instructions); // NOLINT

    std::cout
        << "Part 1: " << part_1 << '\n'
        << "Part 2: " << part_2 << '\n';

    return 0;
}
