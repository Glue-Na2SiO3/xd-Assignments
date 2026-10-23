#include<stdio.h>
#include<string.h>
void judge(char answer[1000],char truth[1000]);

int main()
{
    char first[1000]="B B C D B D D C C D D C C C D B C A A A BCD CD ABC BC ABCD ABCD ABD AC BCD AB ABC ABC BC BCD ABC ABC ABC AB ACD BC\0";
    char second[1000]="B D B B C D C B B C D B C C C B C D A C ABD ABC BCD ACD ACD ABC ABCD ABCD BCD ACD ABD ABD ACD AB ABCD ABC BCD ABCD BD CD\0";
    char third[1000]="B D B B C D B D C B B B B D A B B B C B ACD ABCD ABD ABCD ABC AD ABC ACD ACD ABCD ABCD ABCD ABCD ABCD ABCD BC CD AC BCD CD\0";
    char forth[1000]="A C D C C B A A C A A A B A A B C B D D ABC ABCD ABC ABC ABCD ABCD ABC ACD AB BCD ABCD ABC ACD BCD BC ABC ABC ABD ABCD ABC\0";
    char fifth[1000]="A A C A C D B A A D C D B B C C D D C C D C D A D A A B B A ABCD BCD ABCD ABCD ABCD ABCD BC ABCD ABC BCD ABC ACD ABC ABC ABC ABD ABD ACD ACD ABC BCD BCD BCD ABCD ABCD ABC BCD ABCD ABCD BCD\0";
    char sixth[1000]="C D A C C B B A B A A A A C A D A C B D B D A A D A A B A B B D D B B ABD ACD CD ACD ABC ABCD ABC ABCD ABC BC ABCD ABCD BCD ABCD ABC ABC BCD CD ACD ABCD ACD BCD ABD ABCD BCD BD CD AC ABCD ABCD ACD AC AD ABC ABC\0";

    char answer[1000],a;
    int x;
    printf("请输入章节名\n例如：“第一章”请输入“1”\n");
    scanf("%d",&x);
    printf("请输入答案，只允许以大写字母且以一个空格隔开，无需换行，多选题按顺序无需隔开，例如 “A B ABC”\n");
    a=getchar();
    gets(answer);

    switch(x)
    {
        case 1:judge(answer,first);
        break;

        case 2:judge(answer,second);
        break;

        case 3:judge(answer,third);
        break;

        case 4:judge(answer,forth);
        break;

        case 5:judge(answer,fifth);
        break;

        case 6:judge(answer,sixth);
        break;
    }
    return 0;
}

void judge(char answer[1000],char truth[1000])
{
    int i=-1,j=-1,k=0,l,p,flag=0,order=0;
    char m[6],n[6];

    do
            {
                for(k=0;k<5;k++)
                {
                    m[k]='0';
                    n[k]='0';
                }
                m[k]='\0';
                n[k]='\0';
                k=0;
                i=i+1;
                p=i;
                j=j+1;
                l=j;
                do
                {
                    m[k]=answer[i];
                    i++;
                    k++;
                    if(answer[i]=='\0' || answer[i]==' ')
                    {
                        order++;
                    }
                }while(answer[i]!='\0' && answer[i]!=' ');
                k=0;
                do
                {
                    n[k]=truth[j];
                    j++;
                    k++;
                }while(truth[j]!='\0' && truth[j]!=' ');

                if(strcmp(m,n)!=0)
                {
                   printf("\n题号：%d （错误）你的答案：",order);
                   do
                   {
                       printf("%c",answer[p]);
                       p++;
                   }while(answer[p]!=' ' && answer[p]!='\0' );
                   printf(" 正确答案：");
                   do
                   {
                       printf("%c",truth[l]);
                       l++;
                   }while(truth[l]!=' ' && truth[l]!='\0' );
                   flag=1;
                }
            }while(answer[i]!='\0');
            if(flag==0)
            {
                printf("全对");
            }
}
