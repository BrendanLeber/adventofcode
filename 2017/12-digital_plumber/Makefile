CXXFLAGS=-std=c++17 -pedantic -Weverything -Weffc++ -Wno-c++98-compat -Wno-padded -g -O0
CXX=clang++

solver: solver.cpp graph.hpp
	$(CXX) $(CXXFLAGS) -o solver solver.cpp

run: solver
	cat input | ./solver

test: solver
	cat test.in | ./solver

clean:
	rm solver

check: format
	clang-tidy solver.cpp graph.hpp -config='' -- $(CXXFLAGS)

format:
	clang-format -i -style=file solver.cpp graph.hpp
