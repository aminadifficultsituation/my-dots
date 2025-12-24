#include <stdio.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    struct stat st;
    if (stat(argv[1], &st) == 0) {
        printf("OS_METADATA: %s | Perms: %o | Size: %ld\n", argv[1], st.st_mode & 0777, st.st_size);
    }
    return 0;
}
//sir saad is the best
