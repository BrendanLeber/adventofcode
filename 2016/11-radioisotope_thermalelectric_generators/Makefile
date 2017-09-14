#CFLAGS=-std=c++14 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0
CFLAGS=-std=c++14 -pedantic -Weffc++ -Wno-c++98-compat -g -O0

rng: rng.cpp
	g++ $(CFLAGS) -o rng rng.cpp


test: rng
	cat test01.input | ./rng

run: rng
	cat input | ./rng

clean:
	rm rng

check:
	clang-tidy rng.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file rng.cpp
