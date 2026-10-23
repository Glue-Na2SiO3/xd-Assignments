#include<stdio.h>
#define Maxsize 100
// R为给定关系，Y为其相应闭包，n为R关系矩阵行数和列数 

// 求自反闭包函数  
void r(int R[][Maxsize],int Y[][Maxsize],int n){
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            if(i==j) Y[i][j]=1;
            else Y[i][j]=R[i][j];
        }
    }
}
// 求对称闭包函数  
void s(int R[][Maxsize],int Y[][Maxsize],int n){
    for(int i=0;i<n;i++){
		for(int j=0;j<n;j++){
			Y[i][j] = R[i][j]||R[j][i];
		}
	}
}

// 求传递闭包Warshall
void t(int R[][Maxsize],int Y[][Maxsize],int n){
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++){
			Y[i][j]=R[i][j];
		}
	} 
    for(int j=0;j<n;j++){
		for(int i=0;i<n;i++){
			if(Y[i][j]==1){
				for(int k=0;k<n;k++){
					Y[i][k]|=Y[j][k];
				}
			}
		}
	}
}

 
int main(){
	int n;
	//记录给定关系矩阵 
    int R[Maxsize][Maxsize];
    //记录输出的相应闭包 
    int Y[Maxsize][Maxsize];
    printf("请输入你要输入的关系矩阵的阶数：") ;
    scanf("%d",&n); 
    printf("请输入你要输入的关系矩阵：\n");
    for(int i=0;i<n;i++){
		for(int j=0;j<n;j++)
		scanf("%d",&R[i][j]);
	}
	
    printf("R的自反闭包是：\n");
    r(R,Y,n);
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++){
			printf("%d ",Y[i][j]);
		}
		printf("\n");
	}
	
	printf("R的对称闭包是：\n");
    s(R,Y,n);
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++){
			printf("%d ",Y[i][j]);
		}
		printf("\n");
	}
	
	printf("R的传递闭包是：\n");
    t(R,Y,n);
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++){
			printf("%d ",Y[i][j]);
		}
		printf("\n");
	}
    return 0;
}
