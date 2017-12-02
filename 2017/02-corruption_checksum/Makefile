CFLAGS=-DPART_ONE -std=c++17 -stdlib=libstdc++ -pedantic -Weverything -Weffc++ -Wno-c++98-compat -g -O0
#CFLAGS=-DPART_ONE -std=c++17 -Wall -g -O0
CC=clang++

corruption_checksum: corruption_checksum.cpp
	$(CC) $(CFLAGS) -o corruption_checksum corruption_checksum.cpp

run: corruption_checksum
	cat input | ./corruption_checksum

clean:
	rm corruption_checksum

check:
	clang-tidy corruption_checksum.cpp -config='' -- $(CFLAGS)

format:
	clang-format -i -style=file corruption_checksum.cpp
