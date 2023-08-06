#include <stdio.h>
#include "dclpy.h"

int add(int x, int y) {
    printf("call C function(add)!\n");
    return x + y;
}

int sub(int x, int y) {
    printf("call C function(sub)!\n");
    return x - y;
}
