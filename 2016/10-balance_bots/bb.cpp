#include <algorithm>
#include <exception>
#include <iostream>
#include <map>
#include <memory>
#include <regex>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>


enum class Object_Type { UNKNOWN, BOT, OUTPUT };

using Strings = std::vector<std::string>;


struct Chip_Bot
{
	int chip;
	int bot;

	Chip_Bot() : chip(-1), bot(-1) {}
	Chip_Bot(int c, int b) : chip(c), bot(b) {}
};

using Inputs = std::vector<Chip_Bot>;


struct Destination
{
	Object_Type type;
	int dest;

	Destination() : type(Object_Type::UNKNOWN), dest(-1) {}
	Destination(Object_Type t, int d) : type(t), dest(d) {}
};

struct Rule
{
	Destination low;
	Destination high;

	Rule() : low(), high() {}
	Rule(Destination l, Destination h) : low(l), high(h) {}
};

using Rules = std::map<int, Rule>;


struct Bot
{
	int low;
	int high;

	Bot() : low(-1), high(-1) {}
	Bot(int l, int h) : low(l), high(h) {}
};

using Bots = std::map<int, Bot>;


using Output = std::vector<int>;
using Outputs = std::map<int, Output>;


Bots bots;
Inputs inputs;
Outputs outputs;
Rules rules;


void bot_give(int id, int chip);
void initialize_bots();
void initialize_outputs();
void output_give(int id, int chip);
void parse_inputs(const Strings& lines);
void parse_rules(const Strings& lines);


void bot_give(int id, int chip)
{
	std::cout << "  giving chip " << chip << " to bot " << id << '\n';

	auto& bot = bots[id];

	// give chip to this bot
	if (bot.low == -1) {
		bot.low = chip;
	}
	else {
		bot.high = chip;
		if (bot.high < bot.low) {
			std::swap(bot.high, bot.low);
		}
	}

	// do we need to distribute more chips
	if ((bot.low != -1) && (bot.high != -1)) {
		auto rule = rules[id];

		std::cout
			<< "  bot " << id
			<< " send chip " << bot.low
			<< " to " << (rule.low.type == Object_Type::BOT ? "bot " : "output ") << rule.low.dest
			<< " and chip " << bot.high
			<< " to " << (rule.high.type == Object_Type::BOT ? "bot " : "output ") << rule.high.dest
			<< '\n';
		
		// hand off the lower chip
		if (rule.low.type == Object_Type::BOT) {
			bot_give(rule.low.dest, bot.low);
		}
		else {
			output_give(rule.low.dest, bot.low);
		}

		bot.low = -1;

		// hand off the higher chip
		if (rule.high.type == Object_Type::BOT) {
			bot_give(rule.high.dest, bot.high);
		}
		else {
			output_give(rule.high.dest, bot.high);
		}

		bot.high = -1;
	}

	std::cout << "    bot " << id << " low " << bot.low << " high " << bot.high << '\n';
}


void initialize_bots()
{
	for (const auto& rule : rules) {
		auto it = bots.lower_bound(rule.first);
		if (it == std::end(bots) || rule.first < it->first) {
			bots.insert(it, std::make_pair(rule.first, Bot()));
		}

		auto low = rule.second.low;
		if (low.type == Object_Type::BOT) {
			auto it = bots.lower_bound(low.dest);
			if (it == std::end(bots) || low.dest < it->first) {
				bots.insert(it, std::make_pair(low.dest, Bot()));
			}
		}

		auto high = rule.second.high;
		if (high.type == Object_Type::BOT) {
			auto it = bots.lower_bound(high.dest);
			if (it == std::end(bots) || high.dest < it->first) {
				bots.insert(it, std::make_pair(high.dest, Bot()));
			}
		}
	}

	for (const auto& input : inputs) {
		auto it = bots.lower_bound(input.bot);
		if (it == std::end(bots) || input.bot < it->first) {
			bots.insert(it, std::make_pair(input.bot, Bot()));
		}
	}
}


void initialize_outputs()
{
	for (const auto& rule : rules) {
		auto low = rule.second.low;
		if (low.type == Object_Type::OUTPUT) {
			auto it = outputs.lower_bound(low.dest);
			if (it == std::end(outputs) || low.dest < it->first) {
				outputs.insert(it, std::make_pair(low.dest, Output()));
			}
		}

		auto high = rule.second.high;
		if (high.type == Object_Type::OUTPUT) {
			auto it = outputs.lower_bound(high.dest);
			if (it == std::end(outputs) || high.dest < it->first) {
				outputs.insert(it, std::make_pair(high.dest, Output()));
			}
		}
	}
}


void output_give(int id, int chip)
{
	std::cout << "  giving chip " << chip << " to output " << id << '\n';
	outputs[id].push_back(chip);	
}


void parse_inputs(const Strings& lines)
{
	std::regex input_rx { R"rx(value ([[:digit:]]+) goes to bot ([[:digit:]]+))rx" };
	std::smatch match;
	
	for (const auto& line : lines) {
		if (std::regex_match(line, match, input_rx)) {
			auto chip = std::stoi(match[1].str());
			auto bot = std::stoi(match[2].str());
			inputs.push_back(Chip_Bot(chip, bot));
		}
	}
}


void parse_rules(const Strings& lines)
{
	std::regex input_rx { R"rx(bot ([[:digit:]]+) gives low to (output|bot) ([[:digit:]]+) and high to (output|bot) ([[:digit:]]+))rx" };
	std::smatch match;
	
	for (const auto& line : lines) {
		if (std::regex_match(line, match, input_rx)) {
			auto bot_id = std::stoi(match[1].str());

			auto low_type = (match[2].str() == "output") ? Object_Type::OUTPUT : Object_Type::BOT;
			auto low_id = std::stoi(match[3].str());
			auto low = Destination(low_type, low_id);
			
			auto high_type = (match[4].str() == "output") ? Object_Type::OUTPUT : Object_Type::BOT;
			auto high_id = std::stoi(match[5].str());
			auto high = Destination(high_type, high_id);

			auto iter = rules.lower_bound(bot_id);
			if (iter == std::end(rules) || bot_id < iter->first) {
				auto rule = Rule(low, high);
				rules.insert(iter, std::make_pair(bot_id, rule));
			}
			else {
				std::stringstream ss;
				ss << "error inserting rule for bot " << bot_id << " which exists!";
				throw std::domain_error(ss.str());
			}
		}
	}
}


int main(int, char**)
{
	Strings input;
	while (std::cin) {
		std::string line;
		std::getline(std::cin, line);
		if (!line.empty())
			input.push_back(line);
	}

	parse_inputs(input);
	// std::cout << "\ninputs (" << inputs.size() << "):\n";
	// for (const auto& in : inputs) {
	// 	std::cout << "  chip " << in.chip << " bot " << in.bot << '\n';
	// }

	parse_rules(input);
	// std::cout << "\nrules (" << rules.size() << "):\n";
	// for (const auto& rule : rules) {
	// 	std::cout
	// 		<< "  bot " << rule.first
	// 		<< " low " << (rule.second.low.type == Object_Type::OUTPUT ? "out-" : "bot-")
	// 		<< rule.second.low.dest
	// 		<< " high " << (rule.second.high.type == Object_Type::OUTPUT ? "out-" : "bot-")
	// 		<< rule.second.high.dest << '\n';
	// }

	initialize_bots();
	// std::cout << "\nbots (" << bots.size() << "):\n";
	// for (const auto& bot : bots) {
	// 	std::cout
	// 		<< "  bot " << bot.first
	// 		<< " low " << bot.second.low
	// 		<< " high " << bot.second.high << '\n';
	// }

	initialize_outputs();
	// std::cout << "\noutputs (" << outputs.size() << "):\n";
	// for (const auto& output : outputs) {
	// 	std::cout
	// 		<< "  output " << output.first
	// 		<< " sz " << output.second.size() << " [";
	// 	for (const auto& chip : output.second) {
	// 		std::cout << ' ' << chip;
	// 	}
	// 	std::cout << " ]\n";
	// }

	// std::cout << '\n';
	for (const auto& in : inputs) {
		std::cout << "give " << in.chip << " to bot " << in.bot << '\n';
		bot_give(in.bot, in.chip);

		// std::cout << "  bots (" << bots.size() << "):\n";
		// for (const auto& bot : bots) {
		// 	std::cout
		// 		<< "    bot " << bot.first
		// 		<< " low " << bot.second.low
		// 		<< " high " << bot.second.high << '\n';
		// }
	}

	// std::cout << "\noutputs (" << outputs.size() << "):\n";
	// for (const auto& output : outputs) {
	// 	std::cout
	// 		<< "  output " << output.first
	// 		<< " sz " << output.second.size() << " [";
	// 	for (const auto& chip : output.second) {
	// 		std::cout << ' ' << chip;
	// 	}
	// 	std::cout << " ]\n";
	// }

	return EXIT_SUCCESS;
}
