#include <algorithm>
#include <iostream>
#include <iterator>
#include <memory>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>

struct Program {
    std::string name;
    int weight;
    std::vector<std::string> above; // NOLINT

    int total_weight = 0;
    Program* parent = nullptr; // NOLINT
    std::vector<Program*> children;
};

using Programs = std::vector<Program*>;

void calculate_total_weights(Program* node);
void dump_graph(Programs const& programs);
void dump_graph_internal(Program* node);
void dump_programs(Programs const& programs);
std::tuple<bool, Program*> find_different_child(Program* node);
int find_majority(std::vector<Program*> const& children);
Program* find_root(Programs const& programs);

std::string solver_1(Programs const& programs);
int solver_2(Programs const& programs);

void calculate_total_weights(Program* node)
{
    for (auto p : node->children) {
        calculate_total_weights(p);
        node->total_weight += p->total_weight;
    }

    node->total_weight += node->weight;
}

void dump_graph(Programs const& programs)
{
    std::cerr << "digraph recursive_circus {\n";
    std::cerr << "    rankdir = LR;\n";
    std::cerr << "    node [shape = record];\n";
    auto root = find_root(programs);
    dump_graph_internal(root);
    std::cerr << "}\n";
}

void dump_graph_internal(Program* node)
{
    std::cerr
        << "    " << node->name
        << R"l( [label=")l"
        << node->name << '|'
        << node->weight << '|'
        << node->total_weight << R"l("])l"
        << ";\n";

    for (auto p : node->children) {
        std::cerr << "    " << node->name << " -> " << p->name << ";\n";
        dump_graph_internal(p);
    }
}

void dump_programs(Programs const& programs)
{
    for (auto const& p : programs) {
        std::cerr << p->name << " (" << p->weight << ')';
        if (!p->above.empty()) {
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

std::tuple<bool, Program*> find_different_child(Program* node)
{
    int maj = find_majority(node->children);
    auto it = std::find_if(std::begin(node->children), std::end(node->children),
        [maj](Program* p) -> bool { return maj != p->total_weight; });

    return std::make_tuple(it != std::end(node->children), *it);
}

int find_majority(std::vector<Program*> const& children)
{
    size_t idx = 0, count = 1;
    for (size_t i = 1; i < children.size(); ++i) {
        if (children[idx]->total_weight == children[i]->total_weight) {
            ++count;
        }
        else {
            --count;
        }

        if (count == 0) {
            idx = i;
            count = 1;
        }
    }

    count = 0;
    for (auto& child : children) {
        if (child->total_weight == children[idx]->total_weight) {
            ++count;
        }
    }

    if (count <= children.size() / 2) {
        throw - 1;
    }

    return children[idx]->total_weight;
}

Program* find_root(Programs const& programs)
{
    // any node should work as all parents lead to the root
    auto root = programs.front();
    while (root->parent != nullptr) {
        root = root->parent;
    }

    return root;
}

std::string solver_1(Programs const& programs)
{
    return find_root(programs)->name;
}

int solver_2(Programs const& programs)
{
    auto root = find_root(programs);

    // find the child that has a different total weight
    auto node = root;
    bool found;
    Program* child;
    do {
        std::tie(found, child) = find_different_child(node);
        if (found) {
            node = child;
        }
    } while (found);

    auto parent = node->parent;
    // std::cerr << "parent " << parent->name << ' ' << parent->total_weight << '\n';
    // std::cerr << "node " << node->name << ' ' << node->total_weight << ' ' << node->weight << '\n';

    // get another child to calculate the difference in values
    Program* other = (node == parent->children[0])
        ? parent->children[1]
        : parent->children[0];

    auto diff = node->total_weight - other->total_weight;

    // std::cerr
    // 	<< node->total_weight << " - "
    // 	<< other->total_weight << " = "
    // 	<< diff
    // 	<< '\n';

    auto answer = node->weight - diff;

    // std::cerr << answer - diff << '\n';

    return answer;
}

int main()
{
    // load data from stdin
    Programs programs;
    std::string line;
    std::vector<std::string> parts;
    std::string name;
    int weight;
    std::vector<std::string> above;
    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);

        parts.clear();
        std::copy(std::istream_iterator<std::string>(iss),
            std::istream_iterator<std::string>(),
            std::back_inserter(parts));

        name = parts[0];
        weight = std::stoi(parts[1].substr(1, parts[1].size() - 2));

        above.clear();
        if (parts.size() > 2) {
            std::copy(std::begin(parts) + 3, std::end(parts),
                std::back_inserter(above));
            for (auto& a_name : above) {
                if (a_name.back() == ',') {
                    a_name.pop_back();
                }
            }
        }

        programs.push_back(new Program{ name, weight, above }); // NOLINT
    }

    // dump_programs(programs);

    // build tree relationship
    for (Program* pgm : programs) {
        if (!pgm->above.empty()) {
            for (auto const& p_name : pgm->above) {
                auto it = std::find_if(std::begin(programs), std::end(programs),
                    [p_name](Program* p) -> bool { return p->name == p_name; });

                // set parent and add children
                (*it)->parent = pgm;
                pgm->children.push_back(*it);
            }
        }
    }

    calculate_total_weights(find_root(programs));

    // dump_graph(programs);

    std::cout << "Part 1: " << solver_1(programs) << '\n';
    std::cout << "Part 2: " << solver_2(programs) << '\n';

    return 0;
}
