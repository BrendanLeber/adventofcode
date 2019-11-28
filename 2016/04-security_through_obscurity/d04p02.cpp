#include <algorithm>
#include <iostream>
#include <regex>
#include <string>
#include <vector>

using Data = std::tuple<std::string, int, std::string>;
using Frequency = std::pair<char, int>;
using Frequencies = std::vector<Frequency>;

std::string decrypt_name(std::string encrypted_name, int sector_id);
Frequencies get_frequencies(std::string encrypted_name);
bool is_real_room(Data data);

std::string decrypt_name(std::string encrypted_name, int sector_id)
{
    std::string decrypted_name;
    for (auto ch : encrypted_name) {
        if (ch == '-') {
            decrypted_name.push_back(' ');
        }
        else {
            int value = static_cast<char>(ch - 'a');
            value = (value + sector_id) % 26;
            decrypted_name.push_back(static_cast<char>(value + 'a'));
        }
    }

    return decrypted_name;
}

Frequencies get_frequencies(std::string encrypted_name)
{
    std::array<int, 26> counts{};

    for (auto ch : encrypted_name) {
        counts[static_cast<size_t>(ch) - static_cast<size_t>('a')] += 1;
    }

    Frequencies freqs;
    for (size_t c = 0; c < 26; ++c) {
        if (counts[c] > 0) {
            freqs.push_back(std::make_pair(static_cast<char>('a' + c), counts[c]));
        }
    }

    std::sort(std::begin(freqs), std::end(freqs), [](auto& left, auto& right) {
          bool result;
          if (left.second > right.second) {
              result = true;
          } else if (left.second < right.second) {
              result = false;
          } else if (left.first < right.first) {
              result = true;
          } else {
              result = false;
          }
          return result;
      });

    return freqs;
}

bool is_real_room(Data data)
{
    std::string encrypted_name, checksum;

    std::tie(encrypted_name, std::ignore, checksum) = data;

    encrypted_name.erase(
        std::remove_if(std::begin(encrypted_name), std::end(encrypted_name), [](char x) { return x == '-'; }),
        std::end(encrypted_name));

    // get frequency of letters in the encrypted_name
    auto freqs = get_frequencies(encrypted_name);

    // validate the checksum against the encrypted_name
    for (size_t i = 0; i < checksum.size(); ++i) {
        if (freqs[i].first != checksum[i]) {
            return false;
        }
    }

    // return true if we made it here as it's a match
    return true;
}

int main(int /*argc*/, char** /*argv*/)
{
    std::string line;
    std::vector<std::string> input;
    while (std::cin >> line) {
        input.push_back(line);
    }

    std::vector<Data> data;

    try {
        std::regex re(R"(^([^[:digit:]]+)([[:digit:]]+)\[([a-z]+)\]$)");
        std::smatch match;

        for (const auto& el : input) {
            if (std::regex_match(el, match, re)) {
                auto encrypted_name = match[1].str();
                auto sector_id = std::stoi(match[2].str());
                auto checksum = match[3].str();
                data.push_back(std::make_tuple(encrypted_name, sector_id, checksum));
            } else {
                std::cerr << "no match " << el << '\n';
                std::exit(EXIT_FAILURE);
            }
        }
    }
    catch (std::regex_error& ex) {
        std::cerr << "regex_error: " << ex.what() << '\n';
        std::exit(EXIT_FAILURE);
    }

    for (auto d : data) {
        if (is_real_room(d)) {
            std::string encrypted_name;
            int sector_id;
            std::tie(encrypted_name, sector_id, std::ignore) = d;
            auto decrypted_name = decrypt_name(encrypted_name, sector_id);
            std::cout << decrypted_name << " sector id " << std::get<1>(d) << '\n';
        }
    }

    return EXIT_SUCCESS;
}
