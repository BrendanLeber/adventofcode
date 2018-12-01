CXXFLAGS=-std=c++17 -pedantic -Weverything -Weffc++ -Wno-c++98-compat -Wno-padded -g -O0
CXX=clang++

no_math: no_math.cpp
	$(CXX) $(CXXFLAGS) -o no_math no_math.cpp

run: no_math
	cat input | ./no_math

test: no_math
	cat test.in | ./no_math

clean:
	rm no_math

check: format
	clang-tidy no_math.cpp -config='' -- $(CXXFLAGS)

format:
	clang-format -i -style=file no_math.cpp
