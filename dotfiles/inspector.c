#include <stdio.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    struct stat st;
    if (argc < 2) return 1;

    // stat() works on all file types in the Linux Virtual File System
    if (stat(argv[1], &st) == 0) {
        if (S_ISDIR(st.st_mode)) {
            printf("✓ System Check: Directory verified.\n");
        } else if (S_ISREG(st.st_mode)) {
            printf("✓ System Check: File verified (%ld bytes).\n");
        } else {
            printf("✓ System Check: Special system file verified.\n");
        }
        return 0; 
    } else {
        printf("✗ System Check: Path not found.\n");
        return 1; 
    }
}
