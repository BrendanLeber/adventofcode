#CFLAGS=-std=c++14 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0
CFLAGS=-std=c++14 -pedantic -Weffc++ -Wno-c++98-compat -g -O0

bb: bb.cpp
	g++ $(CFLAGS) -o bb bb.cpp


test: bb
	cat test01.input | ./bb

run: bb
	cat input | ./bb

clean:
	rm bb

check:
	clang-tidy bb.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file bb.cpp
