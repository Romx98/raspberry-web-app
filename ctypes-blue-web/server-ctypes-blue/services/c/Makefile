clean:
	rm -f *.o *.so

StringFunction.so: StringFunction.o
	gcc -shared -o StringFunction.so StringFunction.o

StringFunction.o: StringFunction.c
	gcc -c -Wall -Werror -fPIC StringFunction.c

test: StringFunction.so
	~/web_apps/raspberry-web-app/ctypes-blue-web/server-ctypes-blue/app.py