#include"func.h"
  
int main() {  
    Stack s;  
    initStack(&s);  
    int op;  
    int value;  
  
    printf("这是一个堆栈结构函数调用的示例 (push：1, pop：2, top：3, exit 0): \n");  
    while (1) {  
        scanf("%d",&op); 
        switch (op) {  
            case 1:  
                printf("输入需要push的数字: ");  
                scanf("%d", &value);  
                push(&s, value);  
                break;  
            case 2:  
                if (pop(&s, &value)) {      
                }  
                break;  
            case 3:  
                if (top(&s, &value)) {    
                }  
                break;  
            case 0:  
                return 0; 
            default:  
                printf("请重新输入操作编号\n");  
        }  
    }  
  
    return 0;  
}
