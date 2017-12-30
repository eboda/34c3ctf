#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>
#include <unistd.h>
#include <sys/wait.h>

char *read_line() {
    char *line = NULL;
    size_t bufsize = 0; 
    int chars = 0;
    
    chars = getline(&line, &bufsize, stdin);
    if (chars <= 0) {
        exit(EXIT_SUCCESS);
    }
    if (line[chars - 1] == '\n')
        line[chars - 1] = '\0';

    return line;
}

void help() {
    printf("\t\n\t\e[1m+=============================================================+\e[0m\n");
    printf("\t\e[1m|\e[0m                \e[1;4;91mMINIMAL BASH - MAXIMAL FUN\e[0;39m                   | \n");
    printf("\t\e[1m|\e[0m                                                             | \n");
    printf("\t\e[1m|\e[0m            Who needs regular characters anyway?             |  \n");
    printf("\t\e[1m|\e[0m                                                             | \n");
    printf("\t\e[1m|\e[0m         \e[1mSupported characters: \e[0;91m$ ( ) # ! { } < \\ ' ,\e[39m         |\n");
    printf("\t\e[1m|\e[0m                                                             |\n");
    printf("\t\e[1m|\e[0m         \e[1mSupported binaries: \e[0mi'm sure there is some          |\n");
    printf("\t\e[1m|\e[0m                                                             |\n");
    printf("\t\e[1m|\e[0m               Iz also open-source: '\e[1msource\e[0m'                 |\n");
    printf("\t\e[1m|\e[0m                                                             |\n");
    printf("\t\e[1m+=============================================================+\e[0m\n\n");
}

void source() {
    printf("\t\e[1m                                                                     .---.\e[0m \n");
    printf("\t  \e[1;91mSource iz sumthing like dis:\e[1;39m                                      /  .  \\\e[0m \n");
    printf("\t  \e[1m                                                                 |\\_/|   |\e[0m \n");
    printf("\t\e[1m                                                                   |   |  /|\e[0m \n");
    printf("\t\e[1m  .----------------------------------------------------------------------' | \e[0m\n");
    printf("\t\e[1m /  .-.                                                                    |\e[0m \n");
    printf("\t\e[1m|  /   \\                                                                   |\e[0m \n");
    printf("\t\e[1m| |\\_.  | \e[0m \e[90m   [....] \e[39m                                       \e[1m               |\e[0m \n");
    printf("\t\e[1m|\\|  | /|                                                                  |\e[0m \n");
    printf("\t\e[1m| `---' |  \e[0m   \e[31m/* these 11 chars should be more than enough  */\e[1;39m             |\e[0m \n");
    printf("\t\e[1m|       |  \e[0m   re = \e[1;34mregcomp\e[0;39m(&regex, \e[36m\"[^${}!#()<\'\\\\,]\"\e[39m, \e[34m0\e[1;39m);                  | \e[0m \n");
    printf("\t\e[1m|       |                                                                  | \e[0m \n");
    printf("\t\e[1m|       |  \e[0m   \e[90m[....]\e[39m    \e[1m                                                   |\e[0m  \n");
    printf("\t\e[1m|       |                                                                  | \e[0m \n");
    printf("\t\e[1m|       | \e[0m    \e[91mif\e[0m (\e[34mREG_NOMATCH\e[39m == \e[34;1mregexec\e[0;39m(&regex, input, \e[34m0\e[39m, \e[34mNULL\e[39m, \e[34m0\e[39m))  {    | \e[0m \n");
    printf("\t\e[1m|       |                                                                  | \e[0m \n");
    printf("\t\e[1m|       |     \e[0m   \e[90m [....] \e[39m                                          \e[1m        | \e[0m \n");
    printf("\t\e[1m|       |                                                                  | \e[0m \n");
    printf("\t\e[1m|       |         fclose(stdin);                                           | \e[0m \n");
    printf("\t\e[1m|       |         \e[1;34mexecl\e[0;39m(\e[36m\"/bin/bash\"\e[39m, \e[36m\"/bin/bash\"\e[39m, \e[36m\"-c\"\e[39m, input, \e[34mNULL\e[39m);\e[1m      | \e[0m \n");
    printf("\t\e[1m|       |                                                                  | \e[0m \n");
    printf("\t\e[1m|       |     \e[0m   \e[90m [....] \e[39m                                          \e[1m        | \e[0m \n");
    printf("\t\e[1m|       | \e[0m    }   \e[1m                                                         | \e[0m \n");
    printf("\t\e[1m|       |                                                                  | \e[0m \n");
    printf("\t\e[1m|       |  \e[0m  \e[90m [....] \e[39m                                       \e[1m               | \e[0m \n");
    printf("\t\e[1m|       |                                                                  / \e[0m\n");
    printf("\t\e[1m|       |-----------------------------------------------------------------'\e[0m \n");
    printf("\t\e[1m\\       |\e[0m \n");
    printf("\t\e[1m \\     / \e[0m        \n");
    printf("\t\e[1m  `---' \e[0m\n\n");
}


int main() {
    setbuf(stdout, NULL);
    char *input;
    regex_t regex;
    int re;
    re = regcomp(&regex, "[^${}!#()<\'\\,]", 0);

    if (re) {
        printf("regex compile failed \n");
        exit(EXIT_FAILURE);
    }
    
    while (1) {
        printf("\e[1mmin-bash>\e[0m ");
        input = read_line();
        if (!strcmp(input, "help")) {
            help();
        } else if (!strcmp(input, "source")) {
            source();
        } else if (!strcmp(input, "exit")) {
            exit(0);
        } else {
            re = regexec(&regex, input, 0, NULL, 0);
            if (re == REG_NOMATCH) {
                int pid = fork();
                if (pid == 0) {
                    fclose(stdin);
                    execl("/bin/bash", "/bin/bash", "-c", input, NULL);
                    exit(1337);
                } else if (pid == -1) {
                    fprintf(stderr, "failed to fork...");
                    exit(EXIT_FAILURE);
                } else {
                    wait(NULL);
                }
            } else {
                fprintf(stderr, "Invalid character. Try '\e[1mhelp\e[0m'.\n");
            }
        }
        free(input);
    }
}
