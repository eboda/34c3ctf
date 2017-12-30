#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#define PASS "gimme_FLAG_please"


int main(int argc, char **argv) {
    setbuf(stdout, NULL);
    if (argc != 2 || strcmp(argv[1], PASS)) {
        printf("Usage: %s %s\n", argv[0], PASS);
        exit(0);
    }
    char buf[200];
    FILE* fdflag = fopen("/flag", "r");
    fread(buf, 1, sizeof(buf), fdflag);
    printf("%s\n", buf);
    fflush(stdout);
    return 0;
}
