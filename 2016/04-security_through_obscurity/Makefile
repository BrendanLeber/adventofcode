PUZZLE=d04p02
CFLAGS=-std=c++14 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0

compile: $(PUZZLE).cpp
	clang++ $(CFLAGS) -o $(PUZZLE) $(PUZZLE).cpp

test: compile
	cat input | ./$(PUZZLE)

clean:
	rm $(PUZZLE)

check:
	clang-tidy $(PUZZLE).cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file $(PUZZLE).cpp
