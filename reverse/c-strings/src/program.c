#include <stdio.h>
#include <string.h>

int main()
{
    char buffer[20];
    printf("Password:\n");
    scanf("%s", buffer);
    if( strcmp(buffer, "iPzt3CFVkUDjSJ6ieCeKRV6dG6M6bxiI") == 0 ){
      printf("FLAG{iPzt3CFVkUDjSJ6ieCeKRV6dG6M6bxiI}\n");
    }
    return 0;
}