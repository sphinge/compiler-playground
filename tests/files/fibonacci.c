
#ifndef CUSTOM_STDIO_H
#define CUSTOM_STDIO_H

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main() {
printf("%s", "Start of the ezC program \n"); 
int limit = 10000; 
int a = 0; 
int b = 0; 
int c = 1; 
While_Start9: 
bool t0 = a < limit; 
if (t0) { goto Cond_True8;} if (!(t0)) { goto next7;} Cond_True8: 
printf("%d", a); 
int a = b; 
int b = c; 
int c = a; 
goto While_Start9; 
next7: 
int r = 0; 
return r; 

}
#endif // CUSTOM_STDIO_H
