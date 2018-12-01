CXXFLAGS=-std=c++17 -pedantic -Weverything -Weffc++ -Wno-c++98-compat -Wno-padded -g -O0
CXX=clang++

not_quite_lisp: not_quite_lisp.cpp
	$(CXX) $(CXXFLAGS) -o not_quite_lisp not_quite_lisp.cpp

run: not_quite_lisp
	cat input | ./not_quite_lisp

test: not_quite_lisp
	cat test.in | ./not_quite_lisp

clean:
	rm not_quite_lisp

check: format
	clang-tidy not_quite_lisp.cpp -config='' -- $(CXXFLAGS)

format:
	clang-format -i -style=file not_quite_lisp.cpp
