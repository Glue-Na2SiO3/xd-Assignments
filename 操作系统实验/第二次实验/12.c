#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>
#include <malloc.h>

#define MAX_LINE 80
typedef struct history{
    char args[20][20];//命令
    int argc;//命令个数
}history;
int main(){
    history History[20];
    char tempOrder[MAX_LINE][MAX_LINE];
    int historyNumber = 0;//命令的数量
    memset(tempOrder, 0, sizeof(tempOrder));
    while(1){
        printf("osh>");
        char c;
        int i=0;
        char *order[20];//运行命令
        do{
            order[i]=(char *)malloc(10*sizeof(char));
            scanf("%s",order[i]);//读入命令
            scanf("%c",&c);
            i++;
        }while( c!= '\n');
        order[i]=(char *)malloc(10*sizeof(char));
        order[i]=NULL;
        if(strcmp(order[0],"!!")==0){
            if(historyNumber==0) { printf("History is empty");continue; }
            for (int j = 0; j < History[historyNumber-1].argc; ++j) {
                order[j]=(char *)malloc(10*sizeof(char));
                strcpy(order[j],History[historyNumber-1].args[j]);
            }
        } else if(strcmp(order[0],"!")==0){
            if(i==1) {printf("please input number");continue;}
            int number=order[1][0]-'0'-1;
            if(number>historyNumber||number<0){ printf("number is illegal");continue;}
            for (int j = 0; j < History[historyNumber-1].argc; ++j) {
                order[j]=(char *)malloc(10*sizeof(char));
                strcpy(order[j],History[number].args[j]);
            }
        }else if(strcmp(order[0],"exit")==0){
            printf("bye\n");//退出程序
            break;
        }
        History[historyNumber].argc=i;//记录这个命令有几行
        for (int j = 0; j < i; ++j) {
            strcpy(History[historyNumber].args[j],order[j]);
        }
        historyNumber++;

        if(strcmp(order[0],"cd")==0){
            if(chdir(order[1])==-1){
                printf("Error\n");
                continue;
            }else{
                printf("you are in %s\n",order[1]);
            }
        }

        pid_t pid;
        if((pid = fork()) == -1) { printf("Fork Error.\n"); }
        if(pid == 0) {
            execvp(order[0], order);
            break;
        }
        wait(-1);
    }
    return 0;
}