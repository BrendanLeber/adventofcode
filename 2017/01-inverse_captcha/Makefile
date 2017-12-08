CFLAGS=-std=c++17 -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0

solver: solver.cpp
	clang++ $(CFLAGS) -o solver solver.cpp

run: solver
	cat input | ./solver

clean:
	rm solver

check:
	clang-tidy solver.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file solver.cpp
