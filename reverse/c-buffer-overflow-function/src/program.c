#include <stdio.h>

void flag()
{
    printf("FLAG{A8QFkPSeCkbY6QjfcNy1P41jBwV3Z8c9}\n");
}

void name()
{
    char buffer[10];
    printf("Enter your name (10 characters max):\n");
    scanf("%s", buffer);
    printf("Hello %s\n", buffer);     
}

int main()
{
    name();
    return 0;
}