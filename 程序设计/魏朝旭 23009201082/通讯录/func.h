#define MAX_NAME 15
#define MAX_SEX 5
#define MAX_TELE 12
#define MAX_ADDR 30
#define DEFAULT_SZ 3
#include<stdio.h>
#include<string.h>
#include<stdlib.h>

typedef struct
{
	char name[MAX_NAME];
	int age;
	char sex[MAX_SEX];
	char tele[MAX_TELE];
	char addr[MAX_ADDR];
}PeoInfo;

//通讯录类型 
typedef struct
{
	PeoInfo *data;//存放一个信息
	int size;//记录当前已经有的元素个数 
	int capacity;//当前通讯录的最大容量
}Contact;

//声明函数
void CheckCapacity(Contact* ps);//检查通讯录容量 
void InitContact(Contact* ps);//初始化通讯录
void AddContact(Contact* ps);//增加一个信息到通讯录
void ShowContact(const Contact* ps);//打印通讯录中的信息
void DelContact( Contact* ps);//删除指定人的信息
void SearchContact(const Contact* ps);//查找指定人的信息
void ModifyContact(Contact* ps);//查找修改人的信息
void DestroyContact(Contact* ps);//销毁通讯录
void SaveContact(Contact* ps);//保存文件
void LoadContact(Contact* ps);//加载文件
void ExportContact(Contact* ps);//导出文件 
enum Option
{
	EXIT,ADD,DEL,SEARCH,MODIFY,SHOW,SAVE,EXPORT 
};
