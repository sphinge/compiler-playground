
#ifndef CUSTOM_STDIO_H
#define CUSTOM_STDIO_H

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main() {

 
    char d[] = "hello"; 
 next1:
 
    char y[] = "HELLP"; 
 next2:
   bool t0 = 2 == 30; 
    if (t0) { goto  Cond_True4;}
    if (!(t0)) { goto  Cond_False5;} 
 Cond_True4:
      next7: printf("%s", d);
 next6: 
 Cond_False5: 
    

 next3: While_Start10: 
   bool t1 = 5000 == 12; 
    if (t1) { goto  Cond_True9;}
    if (!(t1)) { goto  next8;} 
 Cond_True9: 
      next12: printf("%s", y);
 next11:
    goto  While_Start10;
 next8:
   bool t2 = 9 < 10;  
    bool z = t2; 
 next13:  next15: printf("%s", "EXECUTING");
 next14:
 next0:
}
#endif // CUSTOM_STDIO_H
