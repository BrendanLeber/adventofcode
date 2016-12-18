#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>

using Strings = std::vector<std::string>;
using Frequencies = std::map<char, int>;
using Position_Frequencies = std::vector<Frequencies>;

char most_frequent(const Frequencies& freqs);

char most_frequent(const Frequencies& freqs)
{
    std::vector<std::pair<int, char>> pairs;
    for (auto kv : freqs) {
        pairs.push_back(std::make_pair(kv.second, kv.first));
    }

    std::sort(std::begin(pairs), std::end(pairs),
        [](auto& left, auto& right) {
            return right.first < left.first;
        });

    return pairs[0].second;
}

int main(int argc, char** argv)
{
    Strings args(argv, argv + argc);
    if (argc != 2) {
        std::cout << "Syntax: " << args[0] << " <data-file>\n";
        return EXIT_FAILURE;
    }

    size_t message_len = 0;
    Strings messages;
    std::ifstream in(args[1]);
    std::string message;
    while (in >> message) {
        if (message_len == 0) {
            message_len = message.size();
        } else if (message_len != message.size()) {
            std::cerr << "Error length of '" << message << "' does not match other messages (" << message_len << ")\n";
            return EXIT_FAILURE;
        }

        messages.push_back(message);
    }
    in.close();

    Position_Frequencies pos_freqs(message_len);
    for (auto msg : messages) {
        for (size_t pos = 0; pos < message_len; ++pos) {
            Frequencies& freqs{pos_freqs[pos]};
            auto ch = msg[pos];
            auto found = freqs.find(ch);
            if (found == std::end(freqs)) {
                freqs[ch] = 1;
            } else {
                freqs[ch]++;
            }
        }
    }

    std::string ecc_message;
    for (size_t pos = 0; pos < message_len; ++pos) {
        auto ch = most_frequent(pos_freqs[pos]);
        ecc_message.push_back(ch);
    }

    std::cout << ecc_message << '\n';

    return EXIT_SUCCESS;
}
