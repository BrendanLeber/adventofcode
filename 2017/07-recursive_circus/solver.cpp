#include <algorithm>
#include <iostream>
#include <iterator>
#include <limits>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

struct Program
{
    std::string name;
    int weight;
    std::vector<std::string> above;

    int total_weight;
    Program* parent;
    std::vector<Program*> children;

    Program(std::string n, int w, std::vector<std::string> a)
	: name(n), weight(w), above(a), total_weight(0), parent(nullptr)
    {}
};

using Programs = std::vector<Program*>;

void calculate_total_weights(Program* node);
void dump_programs(Programs const& programs);
std::string solver_1(Programs& programs);
int solver_2(Programs& programs);

void calculate_total_weights(Program* node)
{
    for (auto p : node->children) {
	calculate_total_weights(p);
	node->total_weight += p->total_weight;
    }

    node->total_weight += node->weight;
}

void dump_programs(Programs const& programs)
{
    for (auto const& p : programs) {
	std::cerr << p->name << " (" << p->weight << ')';
	if (p->above.size() > 0) {
	    std::cerr << " ->";
	    bool first = true;
	    for (auto const& ab : p->above) {
		if (first) {
		    first = false;
		    std::cerr << ' ' << ab;
		}
		else {
		    std::cerr << ", " << ab;
		}
	    }
	}
	std::cerr << '\n';
    }
}

std::string solver_1(Programs& programs)
{
    for (Program* pgm : programs) {
    	if (pgm->above.size() > 0) {
    	    for (auto p_name : pgm->above) {
    		auto it = std::find_if(std::begin(programs), std::end(programs),
		  [p_name](Program* p) -> bool { return p->name == p_name; });

		// set parent and add children
		(*it)->parent = pgm;
		pgm->children.push_back(*it);
    	    }
    	}
    }

    // any node should work as all parents lead to the root
    auto root = programs[0];
    while (root->parent) {
    	root = root->parent;
    }

    return root->name;
}

// this depends on the parent/child relationship existing from running solver_1
int solver_2(Programs& programs)
{
    // any node should work as all parents lead to the root
    auto root = programs[0];
    while (root->parent) {
    	root = root->parent;
    }

    calculate_total_weights(root);

    for (auto ch : root->children) {
	std::cerr
	    << ch->name << ' '
	    << ch->weight << " + "
	    << (ch->total_weight - ch->weight) << " = "
	    << ch->total_weight << '\n';
    }

    return root->total_weight;
}

int main()
{
    Programs programs;
    std::string line;
    while (std::getline(std::cin, line)) {
	std::istringstream iss(line);

	std::vector<std::string> parts;
	parts.clear();
	std::copy(std::istream_iterator<std::string>(iss),
	  std::istream_iterator<std::string>(),
	  std::back_inserter(parts));

	std::string name = parts[0];

	int weight = std::stoi(parts[1].substr(1, parts[1].size() - 2));

	std::vector<std::string> above;
	above.clear();
	if (parts.size() > 2) {
	    std::copy(std::begin(parts) + 3, std::end(parts),
	      std::back_inserter(above));
	    for (auto& name : above) {
		if (name.back() == ',') {
		    name.pop_back();
		}
	    }
	}

	programs.push_back(new Program {name, weight, above});
    }

    // dump_programs(programs);

    std::cout << "Part 1: " << solver_1(programs) << '\n';
    std::cout << "Part 2: " << solver_2(programs) << '\n';

    return 0;
}
