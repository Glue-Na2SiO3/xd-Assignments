#include <stdio.h>  
#define BUFFER_SIZE 1024  
  
int main(int argc, char *argv[]) {  
    if (argc != 3) {  
        printf("请保证你依次输入了：程序名 、源文件路径 、 目标文件路径\n");  
        return -1;  
    }  
    
    FILE *source_file = fopen(argv[1], "rb"); 

    if (!source_file) {  
        perror("打开源文件产生错误");  
        return -1;  
    }  
  
    FILE *destination_file = fopen(argv[2], "wb"); 

    if (!destination_file) {  
        perror("打开目标文件产生错误");  
        fclose(source_file); 

        return -1;  
    }  

    char buffer[BUFFER_SIZE];  
    size_t bytes_read;  
  	
    while ((bytes_read = fread(buffer, sizeof(char), BUFFER_SIZE, source_file)) > 0) {  

        fwrite(buffer, sizeof(char), bytes_read, destination_file);  
    }  
  

    fclose(source_file);  
    fclose(destination_file);  
  
    printf("File copied successfully.\n");  
  
    return 0;  
}
