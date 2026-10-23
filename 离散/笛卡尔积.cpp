#include<stdio.h>
typedef struct 
{
    int a;
    int b;
}xuou;

void dikaerji(int* A,int* B,xuou* C,int Al,int Bl){
    int n=0;
    for (int i = 0; i < Al; i++)
    {
        for (int j = 0; j < Bl; j++)
        {
            C[n].a=A[i];
            C[n++].b=B[j];
        }
    }
}

int jiaoji(int* A,int* B,int* C,int Al,int Bl)
{
    int n=0;
    for (int i = 0; i < Al; i++)
    {
        for (int j = 0; j < Bl; j++)
        {
            if(A[i]==B[j]){
                C[n++]=A[i];
                break;
            }
        }
    }
    return n;
}
int main(){
    int A[]={1,2,3,4,5,6,7,8};
    int B[]={-1,2,-3,4,-5,6,-7,-8,-9,-10};
    int D[8];
    xuou C[80];
    int n;
    dikaerji(A,B,C,8,10);
    for (int i = 0; i < 80; i++)
    {
        printf("<%d,%d>\n",C[i].a,C[i].b);
    }
    n=jiaoji(A,B,D,8,10);
    for(int i=0;i<n;i++)
    {
        printf("%d\n",D[i]);
    }
    return 0;
}