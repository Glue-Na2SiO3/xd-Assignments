#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include "buffer.h"

buffer_item buffer[BUFFER_SIZE];
// 创建互斥锁和信号量
pthread_mutex_t mutex;
sem_t  full,empty;

void buffer_out(){
    int i;
    for ( i = 0; i <BUFFER_SIZE ; ++i) {
        printf("%d",buffer[i]);
    }
    printf("\n");
}

int insert_item(int a,int b){
    sem_wait(&empty);
    pthread_mutex_lock(&mutex);
    int i;
    for(i = 0;i < BUFFER_SIZE;i++){
        if(buffer[i] == 0){
            buffer[i] = 1;//找到空的位置
            break;
        }
    }

    if(i == BUFFER_SIZE) return -1;
    printf("producer %d produced %d\n",a,b);
    buffer_out();
    pthread_mutex_unlock(&mutex);
    sem_post(&full);
    return 0;
}
int remove_item(int a,int b){
    sem_wait(&full);
    pthread_mutex_lock(&mutex);
    int i;
    for(i = 0;i < BUFFER_SIZE;i++){
        if(buffer[i] != 0){
            buffer[i] = 0;
            break;
        }
    }
    if(i == BUFFER_SIZE) return -1;
    printf("consumer %d consumed %d\n",a,b);//第几个吃了几个食物
    buffer_out();
    pthread_mutex_unlock(&mutex);
    sem_post(&empty);
    return 0;
}

void * producer(void * param){
    int* num = (int*)param;
    int food_id=0;
    while(1){
        sleep(((rand() % 10) + 1));
        if(insert_item(*num,++food_id))
            printf("report error condition\n");
    }
}

void * consumer(void *param){
    int* num = (int*)param;
    int food_id=0;
    while(1){
        sleep(((rand() % 10) + 1));
        if(remove_item(*num,++food_id))
            printf("report error condition\n");
    }
}


int main(int argc,char *argv[])
{
    //输入等待时间、生产者、消费者数量
    if(argc != 4) return -1;
    int sleep_time = atoi(argv[1]);
    int producer_num = atoi(argv[2]);
    int consumer_num = atoi(argv[3]);

    //初始化互斥锁和信号量，以及初始化缓冲区
    pthread_mutex_init(&mutex,NULL);
    sem_init(&empty,0,BUFFER_SIZE);
    sem_init(&full,0,0);
    int i;
    for(i=0;i<BUFFER_SIZE;i++) buffer[i]=0;

    //创建生产者、消费者线程
    pthread_t producer_tid[producer_num];
    int producer_id[producer_num];
    for(i = 0;i < producer_num;i++){
        producer_id[i] = i + 1;
        pthread_create(&producer_tid[i],NULL,producer,&producer_id[i]);
    }
    pthread_t consumer_tid[consumer_num];
    int consumer_id[consumer_num];
    for(i = 0;i < consumer_num;i++){
        consumer_id[i] = i + 1;
        pthread_create(&consumer_tid[i],NULL,consumer,&consumer_id[i]);
    }

    //休眠
    sleep(sleep_time);
    //退出
    return 0;
}
