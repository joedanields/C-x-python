#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fin = fopen("src/data/credit.dat", "r");
    FILE *fout = fopen("src/data/account.txt", "w");

    if (!fin || !fout) {
        perror("File open error");
        return 1;
    }

    char line[512];
    while (fgets(line, sizeof(line), fin)) {
        // For example, just copy each line from credit.dat to account.txt
        fputs(line, fout);
    }

    fclose(fin);
    fclose(fout);

    return 0;
}
