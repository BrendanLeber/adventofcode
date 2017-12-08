#include <algorithm>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>

int part_1(std::vector<std::string> const& list);
int part_2(std::vector<std::string> const& list);

int part_1(std::vector<std::string> const& list)
{
    int num_valid = 0;

    std::set<std::string> words;
    for (auto const& phrase : list) {
        words.clear();
        size_t num_words = 0;
        std::istringstream str(phrase);
        std::string word;
        while (str >> word) {
            words.insert(word);
            ++num_words;
        }

        if (words.size() == num_words) {
            ++num_valid;
        }
    }

    return num_valid;
}

int part_2(std::vector<std::string> const& list)
{
    int num_valid = 0;

    std::set<std::string> words;
    for (auto const& phrase : list) {
        words.clear();
        size_t num_words = 0;
        std::istringstream str(phrase);
        std::string word;
        while (str >> word) {
            std::sort(std::begin(word), std::end(word));
            words.insert(word);
            ++num_words;
        }

        if (words.size() == num_words) {
            ++num_valid;
        }
    }

    return num_valid;
}

int main()
{
    std::vector<std::string> list;
    std::string line;
    while (std::getline(std::cin, line)) {
        list.emplace_back(line);
    }

    std::cout << "Part 1: " << part_1(list) << '\n';
    std::cout << "Part 2: " << part_2(list) << '\n';

    return 0;
}
