#include <stdio.h>
#include <string.h>

int main(void) {
    char name[100];

    printf("What is your name? ");
    if (fgets(name, sizeof(name), stdin) != NULL) {
        name[strcspn(name, "\n")] = '\0';
        printf("Hello, %s!\n", name);
    }

    return 0;
}
