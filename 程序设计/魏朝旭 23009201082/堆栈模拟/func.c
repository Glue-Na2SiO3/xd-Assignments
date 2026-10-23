#include "func.h"

void initStack(Stack *s) {  
    s->top = -1;  
}  
  
bool isEmpty(Stack *s) {  
    return s->top == -1;  
}  
  
bool isFull(Stack *s) {  
    return s->top == MAX_SIZE - 1;  
}  
  
bool push(Stack *s, int value) {  
	int i=0;
    if (isFull(s)) {  
        printf("堆栈已满，%d不能入栈\n", value);  
        return false;  
    }  
    s->data[++(s->top)] = value;  
    printf("%d已入栈, 堆栈目前存放: ", value);  
    for (i = 0; i <= s->top; i++) {  
        printf("%d ", s->data[i]);  
    }  
    printf("\n");  
    return true;  
}  
   
bool pop(Stack *s, int *value) {
	int i = 0;  
    if (isEmpty(s)) {  
        printf("Stack目前为空，没有元素可以出栈\n");  
        return false;  
    }  
    *value = s->data[(s->top)--];  
    printf("%d已出栈, 堆栈目前存放: ", *value);  
    for (i = 0; i <= s->top; i++) {  
        printf("%d ", s->data[i]);  
    }  
    printf("\n");  
    return true;  
}  
    
bool top(Stack *s, int *value) {  
    if (isEmpty(s)) {  
        printf("Stack目前为空，不能获取栈顶元素\n");  
        return false;  
    }  
    *value = s->data[s->top];  
    printf("栈顶元素是%d\n", *value);  
    return true;  
}  
