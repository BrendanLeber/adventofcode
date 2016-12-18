PUZZLE=d05p01
CFLAGS=-std=c++14 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O2

compile: $(PUZZLE).cpp md5.o
	clang++ $(CFLAGS) -o $(PUZZLE) $(PUZZLE).cpp md5.o

md5.o: md5.hpp md5.cpp
	clang++ $(CFLAGS) -c md5.cpp

test: $(PUZZLE)
	./$(PUZZLE) abc

clean:
	rm $(PUZZLE) md5.o

check:
	clang-tidy $(PUZZLE).cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file $(PUZZLE).cpp
