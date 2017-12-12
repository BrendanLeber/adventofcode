#include <algorithm>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>

constexpr bool solve_part_one = true;
constexpr size_t num_elements = 256;
constexpr size_t num_rounds = 64;

using List = std::vector<int>;

void dump_list(List const& list, size_t pos, size_t skip);
void one_round(List const& lengths, List& list, size_t& pos, size_t& skip);
int solve_1(List const& lengths);
std::string solve_2(List const& bytes);

void dump_list(List const& list, size_t pos, size_t skip)
{
    for (size_t i = 0; i < list.size(); ++i) {
        if (i != 0) {
            std::cerr << ' ';
        }

        if (i == pos) {
            std::cerr << '[' << list[i] << ']';
        }
        else {
            std::cerr << ' ' << list[i] << ' ';
        }
    }

    std::cerr << "  skip " << skip << '\n';
}

void one_round(List const& lengths, List& list, size_t& pos, size_t& skip)
{
    using Diff_Type = List::difference_type;

    for (auto length : lengths) {
        if (length > 1) {
            // reverse `length' elements in the list
            if (pos + static_cast<size_t>(length) < list.size()) {
                // easy case, no wrapping required
                std::reverse(std::begin(list) + static_cast<Diff_Type>(pos),
                    std::begin(list) + static_cast<Diff_Type>(pos + static_cast<size_t>(length)));
            }
            else {
                // wrap around case
                List sublist;
                auto p = pos;
                for (size_t l = 0; l < static_cast<size_t>(length); ++l) {
                    sublist.push_back(list[p]);
                    p = (p + 1) % list.size();
                }

                std::reverse(std::begin(sublist),
                    std::end(sublist));

                p = pos;
                for (size_t l = 0; l < static_cast<size_t>(length); ++l) {
                    list[p] = sublist[l];
                    p = (p + 1) % list.size();
                }
            }
        }

        // increment `pos' by `length' and `skip'
        pos = (pos + static_cast<size_t>(length) + skip) % list.size();

        // increase `skip' size by one
        ++skip;
    }
}

int solve_1(List const& lengths)
{
    // setup the initial state
    size_t pos = 0, skip = 0;
    List list(num_elements);
    std::iota(std::begin(list), std::end(list), 0);

    one_round(lengths, list, pos, skip);

    return list[0] * list[1];
}

std::string solve_2(List const& bytes)
{
    // setup the initial state
    size_t pos = 0, skip = 0;
    List sparse_hash(num_elements);
    std::iota(std::begin(sparse_hash), std::end(sparse_hash), 0);

    // perform all of the rounds -> sparse hash
    for (size_t round = 0; round < num_rounds; ++round) {
        one_round(bytes, sparse_hash, pos, skip);
    }

    // pack the sparse hash into a dense hash
    List dense_hash;
    // std::cerr << "sparsh_hash size " << sparse_hash.size() << '\n';
    for (size_t beg = 0, end = 16; end <= sparse_hash.size(); beg += 16, end += 16) {
        // std::cerr << "  beg " << beg << "  end " << end << '\n';
        int byte = 0;
        for (size_t sbeg = beg; sbeg < end; ++sbeg) {
            byte ^= sparse_hash[sbeg];
        }
        dense_hash.push_back(byte);
    }

    std::stringstream result;
    for (auto byte : dense_hash) {
        result << std::hex << std::setw(2) << std::setfill('0')
               << byte;
    }

    return result.str();
}

int main()
{
    // load data from stdin
    std::string line;
    std::getline(std::cin, line);

    if constexpr (solve_part_one) {
        // parse into format for part 1
        List lengths;
        std::istringstream iss(line);
        std::string value;
        while (!iss.eof()) {
            std::getline(iss, value, ',');
            lengths.push_back(std::stoi(value));
        }

        // solve part 1
        auto part_1 = solve_1(lengths);

        std::cout << "Part 1: " << part_1 << '\n';
    }
    else {
        // parse into format for part 2
        List bytes;
        for (auto ch : line) {
            bytes.push_back(ch);
        }
        List salt{ 17, 31, 73, 47, 23 };
        for (auto s : salt) {
            bytes.push_back(s);
        }

        // solve part 2
        auto part_2 = solve_2(bytes);

        // display result
        std::cout << "Part 2: " << part_2 << '\n';
    }

    return 0;
}
