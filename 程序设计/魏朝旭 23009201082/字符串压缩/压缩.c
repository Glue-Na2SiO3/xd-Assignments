#include <stdio.h>  
#include <string.h>  
#include <stdlib.h>  
   
char *compress(char *src);  
  
int main() {  
    char src[100];  
    printf("请输入一个字符串: ");  
    scanf("%99s", src); 
  
    char *ps = compress(src);  
  
    if (ps != NULL) {  
        puts(ps);  
        free(ps); 
    } else {  
        printf("内存分配失败！\n");  
    }  
  
    return 0;  
}  
  
char *compress(char *src) {  
    int len = strlen(src);  
    char *data = (char *)malloc(len+1);   
    if (data == NULL) {  
        return NULL; 
    }  
  
    int i = 0, j = 0, z = 1,m = 0;  
    while (j < len) {  
        if (j < len - 1 && src[j] == src[j + 1]) {  
            z++;  
            j++;  
        } else {  
            if (z < 3) {  
                for ( m = 0; m < z; m++) {  
                    data[i + m] = src[j];  
                }  
                i += z;  
            } else {  
                data[i++] = src[j];  
                if (z < 10) {  
                    data[i++] = '0' + z;  
                } else {  
                    data[i++] = '0' + z / 10;  
                    data[i++] = '0' + z % 10;  
                }  
            }  
            z = 1;  
            j++;  
        }  
    }  
    data[i] = '\0';  
    return data;  
}
