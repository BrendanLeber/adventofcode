CFLAGS=-DPART_TWO -std=c++17 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0

inverse_captcha: inverse_captcha.cpp
	clang++ $(CFLAGS) -o inverse_captcha inverse_captcha.cpp

run: inverse_captcha
	cat input | ./inverse_captcha

clean:
	rm inverse_captcha

check:
	clang-tidy inverse_captcha.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file inverse_captcha.cpp
