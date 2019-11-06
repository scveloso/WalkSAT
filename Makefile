CC = gcc -O3

all:	makewff

makewff: makewff.c
	$(CC)  makewff.c -lm -o makewff

install: makewff
	cp makewff $(HOME)/bin/
	cp Scripts/* $(HOME)/bin/
	

clean:
	rm -f makewff

