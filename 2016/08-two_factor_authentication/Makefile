CFLAGS=-std=c++14 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0

tfa: tfa.cpp
	clang++ $(CFLAGS) -o tfa tfa.cpp


test: tfa
	./tfa test01.input


clean:
	rm tfa

check:
	clang-tidy tfa.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file tfa.cpp
