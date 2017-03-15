#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>


using Strings = std::vector<std::string>;

struct IP_Address
{
	std::string addr;
	Strings supernets;
	Strings hypernets;

	void clear() {
		supernets.clear();
		hypernets.clear();
	}

	void reset(std::string a) {
		addr = a;
		clear();
	}
};

using IP_Addresses = std::vector<IP_Address>;


Strings abas_to_babs(const Strings& abas);
Strings get_abas(const IP_Address& segment);
bool has_abba(const std::string& segment);
IP_Addresses parse_strings(const Strings& strings);
Strings read_input(std::string in_file);
bool supports_ssl(const IP_Address& addr);
bool supports_tls(const IP_Address& addr);


Strings abas_to_babs(const Strings& abas)
{
	Strings babs;
	std::string bab { "012" };

	for (const auto& aba : abas) {
		bab[0] = bab[2] = aba[1];
		bab[1] = aba[0];
		babs.push_back(bab);
	}

	return babs;
}

Strings get_abas(const IP_Address& addr)
{
	Strings abas;
	for (const auto& segment : addr.supernets) {
		auto end = segment.length() - 2;
		for (size_t pos = 0; pos < end; ++pos) {
			if (segment[pos] != segment[pos+2])
				continue;

			if (segment[pos] != segment[pos+1])
				abas.push_back(segment.substr(pos, 3));
		}
	}

	std::sort(std::begin(abas), std::end(abas));
	auto it = std::unique(std::begin(abas), std::end(abas));
	abas.erase(it, std::end(abas));

	return abas;
}


bool has_abba(const std::string& segment)
{
	for (size_t pos = 0; pos < segment.length() - 3; ++pos) {
		if (segment[pos] != segment[pos+3])
			continue;
		if (segment[pos+1] == segment[pos+2] && segment[pos] != segment[pos+1])
			return true;
	}

	return false;
}


IP_Addresses parse_strings(const Strings& strings)
{
	IP_Addresses addrs;
	IP_Address addr;

	for (const auto& str : strings) {
		addr.reset(str);

		// yeah, i know... copies of copies
		auto s = str;

		while (!s.empty()) {
			if (s[0] == '[') {
				// start of a hypernet segment - remove the '['
				s.erase(0, 1);

				// find the end of the segment (']')
				auto pos = s.find(']');
				if (pos == std::string::npos)
					throw std::runtime_error("malformed hypernet segment");

				// save this hypernet segment to the current address
				auto segment = s.substr(0, pos);
				addr.hypernets.push_back(segment);

				// remove this hypernet segment from the temp string
				s.erase(0, pos + 1);
			}
			else {
				// find the next hypernet segment (or the end)
				auto pos = s.find('[');
				if (pos == std::string::npos) {
					addr.supernets.push_back(s);
					s.erase(0, pos);
				}
				else {
					auto segment = s.substr(0, pos);
					addr.supernets.push_back(segment);

					s.erase(0, pos);
				}
			}
		}

		addrs.push_back(addr);
	}

	return addrs;
}


Strings read_input(std::string in_file)
{
    Strings input;
    std::ifstream in(in_file);

    std::string line;
    while (in >> line) {
        input.push_back(line);
    }

    return input;
}


bool supports_ssl(const IP_Address& addr)
{
	auto abas = get_abas(addr);
	auto babs = abas_to_babs(abas);

	for (const auto& hypernet : addr.hypernets) {
		// std::cerr << "* " << hypernet << std::endl;
		for (const auto& bab : babs) {
			auto pos = hypernet.find(bab);
			// std::cerr << "** " << bab << ' ' << pos << std::endl;
			if (pos != std::string::npos)
				return true;
		}
	}

	return false;
}


bool supports_tls(const IP_Address& addr)
{
	bool in_super = false;
	for (auto super : addr.supernets) {
		if (has_abba(super)) {
			in_super = true;
			break;
		}
	}

	bool in_hyper = false;
	for (auto hyper : addr.hypernets) {
		if (has_abba(hyper)) {
			in_hyper = true;
			break;
		}
	}

	return in_super && !in_hyper;
}


int main(int argc, char** argv)
{
    Strings args(argv, argv + argc);
    if (argc != 2) {
        std::cout << "Syntax: " << args[0] << " <input>\n";
        return EXIT_FAILURE;
    }

    auto input = read_input(args[1]);
    auto addrs = parse_strings(input);

    size_t how_many_support_tls = 0;
    size_t how_many_support_ssl = 0;
    for (auto& addr : addrs) {
	    if (supports_tls(addr)) {
		    ++how_many_support_tls;
	    }

	    if (supports_ssl(addr)) {
		    ++how_many_support_ssl;
	    }
    }

    std::cout
	    << "TLS: " << how_many_support_tls << '\n'
	    << "SSL: " << how_many_support_ssl << '\n';

    return EXIT_SUCCESS;
}
