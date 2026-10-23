#include <stdio.h>

int copyFile(const char *source, const char *destination);

int main()
{
    char sourceFileName[256], destinationFileName[256];

    // 提示用户输入源文件名
    printf("Enter the source file name: ");
    scanf("%255s", sourceFileName);

    // 检查源文件名是否有效
    if (strlen(sourceFileName) == 0) {
        printf("Error: Source file name cannot be empty.\n");
        return 0;
    }

    //输入源文件是否存在
    FILE *sourcefile = fopen(sourceFileName, "r");
    if(sourcefile == NULL){
        printf("Error: Source file does not exist.\n");
        return 0;
    }

    // 提示用户输入目标文件名
    printf("Enter the destination file name: ");
    scanf("%255s", destinationFileName);

    // 检查目标文件名是否有效
    if (strlen(destinationFileName) == 0) {
        printf("Error: Destination file name cannot be empty.\n");
        return 0;
    }

    //输入目标文件是否存在
    FILE *destinationfile = fopen(destinationFileName, "r");
    if(destinationfile == NULL){
        printf("Error: destination file does not exist.\n");
        return 0;
    }

    // 调用复制文件的函数
    if (copyFile(sourceFileName, destinationFileName) != 0) {
        printf("Error: File copy operation failed.\n");
        return 0;
    }

    printf("File copied successfully.\n");
    return 0;
}

int copyFile(const char *source, const char *destination)
{
    FILE *sourceFile, *destinationFile;
    char buffer[1024];
    size_t bytesRead, bytesWritten;

    sourceFile = fopen(source, "rb");
    destinationFile = fopen(destination, "wb");

    // 循环读取和写入文件内容
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), sourceFile)) > 0) {
        bytesWritten = fwrite(buffer, 1, bytesRead, destinationFile);
        if (bytesWritten < bytesRead) {
            perror("Error writing to destination file");
            fclose(sourceFile);
            fclose(destinationFile);
            return -1;
        }
    }

    // 检查是否有读取错误
    if (ferror(sourceFile)) {
        perror("Error reading from source file");
        fclose(sourceFile);
        fclose(destinationFile);
        return -1;
    }

    fclose(sourceFile);
    fclose(destinationFile);

    return 0;
}
