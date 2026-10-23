#include <stdio.h>
#include <pthread.h>

int *array;
void* sort(void* ptr){
    int *be=(int *)ptr;
    int *number=array;
    int begin=be[0];
    int end=be[1];
    for (int i = begin; i <end ; ++i) {
        for (int j = begin; j <end ; ++j) {
            if(number[j+1]<number[j]){
                int c=number[j];
                number[j]=number[j+1];
                number[j+1]=c;
            }
        }
    }
}
int main() {
    printf("请输入一系列用于排序的整数，以非整数字符结尾\n");
    int length=0;
    int a[100];
    array=a;
    while (scanf("%d",&a[length++]));
    /* 声明两个线程的描述符 */
    pthread_t tid1;
    pthread_t tid2;
    getchar();
    int be1[2]={0,((length-1)/2-1)};
    int be2[2]={((length-1)/2) ,(length-2)};
    pthread_create(&tid1, NULL, sort, be1);
    pthread_create(&tid2, NULL, sort, be2);
    pthread_join(tid1,NULL);
    pthread_join(tid2,NULL);
    int j=0,k=0,i=(length-1)/2;
    int answer[length-2];
    while(i<=length-2&&j<=(length-1)/2-1){
        if(a[j]>a[i]){
            answer[k++]=a[i++];
        } else{
            answer[k++]=a[j++];
        }
    }
    while (i<=length-2) answer[k++]=a[i++];
    while (j<=(length-1)/2-1) answer[k++]=a[j++];

    k=0;
    while (k<length-1){
        printf("%d ",answer[k++]);
    }
    return 0;
}
