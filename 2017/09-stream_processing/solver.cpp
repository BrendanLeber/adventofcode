#include <algorithm>
#include <iostream>
#include <string>
#include <tuple>

std::tuple<int, int> solver(std::string& stream);
std::string extract_garbage(std::string& stream);
void remove_cancelled(std::string& stream);

std::string extract_garbage(std::string& stream)
{
    std::string extracted;
    auto gbeg = std::find(std::begin(stream), std::end(stream), '<');
    while (gbeg != std::end(stream)) {
        auto gend = std::find(std::begin(stream), std::end(stream), '>');
        extracted.append(gbeg + 1, gend); // don't include the < or >
        stream.erase(gbeg, gend + 1);
        gbeg = std::find(std::begin(stream), std::end(stream), '<');
    }

    return extracted;
}

void remove_cancelled(std::string& stream)
{
    auto it = std::find(std::begin(stream), std::end(stream), '!');
    while (it != std::end(stream)) {
        stream.erase(it, it + 2); // remove ! and the following character
        it = std::find(std::begin(stream), std::end(stream), '!');
    }
}

std::tuple<int, int> solver(std::string& stream)
{
    remove_cancelled(stream);
    auto extracted = extract_garbage(stream);

    int total_score = 0, score = 0;
    for (auto& ch : stream) {
        if (ch == '{') {
            // start a group
            ++score;
        }
        else if (ch == '}') {
            // close a group
            total_score += score;
            --score;
        }
    }

    return std::make_tuple(total_score, extracted.size());
}

int main()
{
    // load data from stdin
    std::string stream;
    std::getline(std::cin, stream);

    // solve problems
    auto[part_1, part_2] = solver(stream); // NOLINT

    // display result
    std::cout
        << "Part 1: " << part_1 << '\n'
        << "Part 2: " << part_2 << '\n';

    return 0;
}
