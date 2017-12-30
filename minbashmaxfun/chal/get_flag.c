#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>


int main() {
    setbuf(stdout, NULL);
    alarm(3);
    unsigned int nums[5];
    unsigned long long res = 0;
    unsigned long long solution = 0;
    FILE* fd;

    if (!(fd = fopen("/dev/urandom", "r"))) {
        printf("no random...\n");
        exit(-1);
    }

    if (fread(nums, 1, sizeof(nums), fd) != sizeof(nums)) {
        printf("no random...\n");
        exit(-1);
    }

    for (int i = 0; i < 5; i++)
        res += (unsigned long long)nums[i];

    printf("Please solve this little captcha:\n");
    fflush(stdout);
    for (int i = 0; i < 4; i++)
        printf("%u + ", nums[i]);
    printf("%u\n", nums[4]);
    fflush(stdout);

    scanf("%llu", &solution);

    if (solution == res) {
        char buf[100];
        FILE* fdflag = fopen("flag", "r");
        fread(buf, 1, sizeof(buf), fdflag);
        printf("%s\n", buf);
        fflush(stdout);
    } else {
        printf("%llu != %llu :(\n", res, solution);
        fflush(stdout);
    }
    return 0;
}
