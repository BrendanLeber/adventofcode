CFLAGS=-std=c++17 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0

inverse_captcha: inverse_captcha.cpp
	clang++ $(CFLAGS) -o inverse_captcha inverse_captcha.cpp

run: inverse_captcha
	cat input | ./inverse_captcha

test: inverse_captcha
	cat test_01.in | ./inverse_captcha > test_01.result
	diff -uw test_01.out test_01.result
	cat test_02.in | ./inverse_captcha > test_02.result
	diff -uw test_02.out test_02.result
	cat test_03.in | ./inverse_captcha > test_03.result
	diff -uw test_03.out test_03.result
	cat test_04.in | ./inverse_captcha > test_04.result
	diff -uw test_04.out test_04.result

clean:
	rm inverse_captcha

check:
	clang-tidy inverse_captcha.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file inverse_captcha.cpp
