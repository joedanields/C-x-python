#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc != 6) {
        fprintf(stderr, "Usage: %s firstname lastname phone aadhar password\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen("data/credit.dat", "a");
    if (fp == NULL) {
        perror("Error opening credit.dat");
        return 1;
    }

    fprintf(fp, "%s,%s,%s,%s,%s\n", argv[1], argv[2], argv[3], argv[4], argv[5]);
    fclose(fp);

    printf("Data written successfully.\n");
    return 0;
}
