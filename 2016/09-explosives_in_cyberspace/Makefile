#CFLAGS=-std=c++14 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0
CFLAGS=-std=c++14 -pedantic -Weffc++ -Wno-c++98-compat -g -O0

eic: eic.cpp
	g++ $(CFLAGS) -o eic eic.cpp


test: eic
	cat test01.input | ./eic > test01.result
	diff -uw test01.output test01.result
	cat test02.input | ./eic > test02.result
	diff -uw test02.output test02.result
	cat test03.input | ./eic > test03.result
	diff -uw test03.output test03.result
	cat test04.input | ./eic > test04.result
	diff -uw test04.output test04.result
	cat test05.input | ./eic > test05.result
	diff -uw test05.output test05.result
	cat test06.input | ./eic > test06.result
	diff -uw test06.output test06.result

run: eic
	cat input | ./eic

clean:
	rm eic
	rm *.result

check:
	clang-tidy eic.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file eic.cpp
