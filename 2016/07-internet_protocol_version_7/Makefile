CFLAGS=-std=c++14 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0

ipv7: ipv7.cpp
	clang++ $(CFLAGS) -o ipv7 ipv7.cpp


test: ipv7
	./ipv7 test02.input


clean:
	rm ipv7 d07p02

check:
	clang-tidy ipv7.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file ipv7.cpp
