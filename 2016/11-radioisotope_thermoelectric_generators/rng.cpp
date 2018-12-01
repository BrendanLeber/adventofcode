#include <array>
#include <iostream>
#include <string>
#include <vector>


constexpr int Num_Floors = 4;


void dump_state();
std::vector<int> parse_input();


void dump_state(const std::vector<int>& state)
{
	int num_chips = state.size() / 2;
	for (int floor = Num_Floors - 1; floor >= 0; --floor) {
		std::cout
			<< 'F' << (floor + 1) << " \n";
	}
}


std::vector<int> parse_input()
{
	int num_chips;
	std::cin >> num_chips;

	std::vector<int> state;
	state.reserve(num_chips * 2);
	for (int chip = 0; chip < num_chips * 2; ++chip) {
		int ch;
		std::cin >> ch;
		state.emplace_back(ch);
	}

	return state;
}


int main()
{
	auto state = parse_input();
	std::cout << "initial state:\n";
	dump_state(state);

	return EXIT_SUCCESS;
}
