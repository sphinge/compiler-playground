
#ifndef CUSTOM_STDIO_H
#define CUSTOM_STDIO_H

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main() {
printf("%s", "Start of the ezC program \n"); 
int t0 = 0 + 0; 
int i = t0; 
While_Start6: 
bool t1 = i == 0; 
if (t1) { goto Cond_True5;} if (!(t1)) { goto next4;} Cond_True5: 
printf("%s", "I is zero \n"); 
goto While_Start6; 
next4: 
bool t2 = i != 0; 
if (t2) { goto Cond_True10;} if (!(t2)) { goto Cond_False11;} Cond_True10: 
printf("%s", "I is not zero \n"); 
Cond_False11: 
printf("%s", "I zero"); 
printf("%s", "no loop \n"); 
printf("%s", "calling c function\n"); 
int t3 = 0 + 0; 
int r = t3; 
printf("%s", "Exiting program \n"); 
return r; 

}
#endif // CUSTOM_STDIO_H
