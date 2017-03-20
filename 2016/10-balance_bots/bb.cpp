#include <algorithm>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>


enum class Object_Type { BOT, OUTPUT };


struct Object
{
	int id;
	Object_Type type;

	Object(Object_Type a_type, int an_id) : type(a_type), id(an_id) {}

	Object_Type get_type() const { return type; }
	int get_id() const { return id; }
};


struct Bot : public Object
{
	int low;
	int high;
	std::shared_ptr<Object> give_low;
	std::shared_ptr<Object> give_high;

	Bot(int an_id) : Object(Object_Type::BOT, id), low(-1), high(-1), give_low(nullptr), give_high(nullptr) {}

	bool have_both() const { return low != -1 && high != -1; }

	bool accept(int chip)
	{
		if (low == -1) {
			low = chip;
		}
		else if (high == -1) {
			high = chip;
			if (high < low) {
				std::swap(low, high);
			}
		}
		else {
			throw std::runtime_error("bot has hands full!");
		}

		return have_both();
	}
};


struct Output : public Object
{
	Output(int an_id) : Object(Object_Type::OUTPUT, id) {}
};


using Strings = std::vector<std::string>;
using Chip_Bot = std::pair<int, int>;
using Inputs = std::vector<Chip_Bot>;
using Object_Ptr = std::shared_ptr<Object>;
using Object_Key = std::pair<Object_Type, int>;
using Objects = std::map<Object_Key, Object_Ptr>;


Inputs parse_inputs(const Strings& lines);
Objects parse_objects(const Strings& lines);
Strings split(const std::string &s, char delim);


Inputs parse_inputs(const Strings& lines)
{
	const std::string value_marker { "value" };
	const std::string bot_marker { "bot" };
	Inputs inputs;

	for (const auto& line : lines) {
		if (line.find(value_marker) == 0) {
			auto chip = std::stoi(line.substr(value_marker.length()));
			auto pos = line.find(bot_marker);
			auto bot_pos = pos + bot_marker.length();
			auto bot = std::stoi(line.substr(bot_pos));
			inputs.push_back(std::move(std::make_pair(chip, bot)));
		}
	}

	return inputs;
}


Objects parse_objects(const Strings& lines)
{
	const std::string bot_marker { "bot" };
	const std::string output_marker { "output" };

	// 0   1    2     3   4  5        6    7   8    9  10       11
	// bot <id> gives low to <object> <id> and high to <object> <id>

	Objects objects;
	for (const auto& line : lines) {
		if (line.find(bot_marker) != 0)
			continue;

		auto parts = split(line, ' ');

		Object_Key low_id
			= std::make_pair(
				(parts[5] == output_marker) ? Object_Type::OUTPUT : Object_Type::BOT,
				std::stoi(parts[6]));
		if (objects.find(low_id) == std::end(objects)) {
			if (low_id.first == Object_Type::OUTPUT) {
				objects[low_id] = std::make_shared<Output>(low_id.second);
			}
			else {
				objects[low_id] = std::make_shared<Bot>(low_id.second);
			}
		}

		Object_Key high_id
			= std::make_pair(
				(parts[10] == output_marker) ? Object_Type::OUTPUT : Object_Type::BOT,
				std::stoi(parts[11]));
		if (objects.find(high_id) == std::end(objects)) {
			if (high_id.first == Object_Type::OUTPUT) {
				objects[high_id] = std::make_shared<Output>(high_id.second);
			}
			else {
				objects[high_id] = std::make_shared<Bot>(high_id.second);
			}
		}

		auto bot_id = std::make_pair(Object_Type::BOT, std::stoi(parts[1]));
		if (objects.find(bot_id) == std::end(objects)) {
			objects[bot_id] = std::make_shared<Bot>(bot_id.second);
		}
		auto bot = std::static_pointer_cast<Bot>(objects[bot_id]);
		bot->give_low = objects[low_id];
		bot->give_high = objects[high_id];
	}

	return objects;
}


Strings split(const std::string &s, char delim)
{
	std::stringstream ss(s);
	std::string item;
	Strings elems;
	while (std::getline(ss, item, delim)) {
		elems.push_back(std::move(item));
	}
	return elems;
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

	auto inputs = parse_inputs(input);
	auto objects = parse_objects(input);

	std::cout << input.size() << "\n";

	std::cout << "\ninputs (" << inputs.size() << "):\n";
	for (const auto& in : inputs) {
		std::cout << in.first << " -> " << in.second << '\n';
	}

	std::cout << "\nobjects (" << objects.size() << "):\n";
	for (const auto& obj : objects) {
		if (obj.second->type == Object_Type::BOT) {
			auto bot = std::static_pointer_cast<Bot>(obj.second);

			std::cout << "bot " << bot->id << " low -> " << bot->give_low->id << " high -> " << bot->give_high->id << '\n';
		}
			else {
				auto output = std::static_pointer_cast<Output>(obj.second);
				std::cout << "output " << output->id << '\n';
			}
	}

	return EXIT_SUCCESS;
}
