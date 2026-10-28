#include <stdio.h>
#include <string.h>

int main(void) {
    char name[100];

    fprintf(stderr, "[INFO] Program started\n");
    printf("What is your name? ");
    if (fgets(name, sizeof(name), stdin) != NULL) {
        name[strcspn(name, "\n")] = '\0';
        printf("Hello, %s!\n", name);
        fprintf(stderr, "[INFO] Greeting printed\n");
    }

    return 0;
}
