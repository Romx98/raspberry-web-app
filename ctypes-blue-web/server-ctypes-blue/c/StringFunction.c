#include<stdio.h>
#include<stdlib.h>
#include<string.h>


void add_one_to_string(char *input) {
    for (int x = 0; x < strlen(input); x++) {
        input[x] += 3;
    }
}
