CXXFLAGS=-std=c++17 -pedantic -Weverything -Weffc++ -Wno-c++98-compat -Wno-padded -g -O0
CXX=clang++

solve: solve.cpp
	$(CXX) $(CXXFLAGS) -o solve solve.cpp

run: solve
	cat input.txt | ./solve

test: solve
	cat test.txt | ./solve

clean:
	rm solve

check: format
	clang-tidy solve.cpp -config='' -- $(CXXFLAGS)

format:
	clang-format -i -style=file solve.cpp
