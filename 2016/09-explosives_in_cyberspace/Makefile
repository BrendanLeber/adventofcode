CFLAGS=-std=c++14 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0

eic: eic.cpp
	clang++ $(CFLAGS) -o eic eic.cpp


test: eic
	echo "ADVENT" | ./eic
	echo "A(1x5)BC" | ./eic
	echo "(3x3)XYZ" | ./eic
	echo "A(2x2)BCD(2x2)EFG" | ./eic
	echo "(6x1)(1x3)A" | ./eic
	echo "X(8x2)(3x3)ABCY" | ./eic

run: eic
	cat input | ./eic

clean:
	rm eic

check:
	clang-tidy eic.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file eic.cpp
