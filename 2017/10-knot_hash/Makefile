CXXFLAGS=-std=c++17 -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0
CXX=clang++
#CXXFLAGS=-std=c++17 -Wall -g -O0
#CXX=g++

solver: solver.cpp
	$(CXX) $(CXXFLAGS) -o solver solver.cpp

run: solver
	cat input | ./solver

test: solver
	cat test.in | ./solver

clean:
	rm solver

check: format
	clang-tidy solver.cpp -config='' -- $(CXXFLAGS)

format:
	clang-format -i -style=file solver.cpp
