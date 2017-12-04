#include <algorithm>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>

int solver(std::vector<std::string> const& list);

int solver(std::vector<std::string> const& list)
{
    int num_valid = 0;

    std::set<std::string> words;
    for (auto const& phrase : list) {
        words.clear();
        size_t num_words = 0;
        std::istringstream str(phrase);
        std::string word;
        while (str >> word) {
            std::sort(std::begin(word), std::end(word)); // Part Two
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

    std::cout << solver(list) << '\n';

    return 0;
}
