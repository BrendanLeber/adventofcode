#CFLAGS=-std=c++17 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0
#CC=clang++
CFLAGS=-std=c++17 -Wall -g -O0
CC=g++

solver: solver.cpp
	$(CC) $(CFLAGS) -o solver solver.cpp

run: solver
	cat input | ./solver

clean:
	rm solver

check:
	clang-tidy solver.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file solver.cpp
