#include <stdio.h>  
#include <stdlib.h>  
#include <stdbool.h>  

// 定义堆栈的最大容量
#define MAX_SIZE 100 
  
typedef struct { 
// 模拟栈顶指针，初始化为-1表示空栈
    int top; 
    int data[MAX_SIZE];   
} Stack;  
  
void initStack(Stack *s) ;
bool isFull(Stack *s);
bool push(Stack *s, int value);
bool pop(Stack *s, int *value);
bool top(Stack *s, int *value);
