#include <stdio.h>
#include <string.h>

int main(void)
{
    char buffer[32];
    int password = 0;

    printf("Password : \n");
    gets(buffer);

    if(strcmp(buffer, "yGmOl7Yry9YyVTI8IPRz56Oe21GfSRHu")) {
        printf("Incorrect password \n");
    }
    else {
        printf("Correct password \n");
        password = 1;
    }

    if(password) {
        printf ("FLAG{yGmOl7Yry9YyVTI8IPRz56Oe21GfSRHu} \n");
    }

    return 0;
}