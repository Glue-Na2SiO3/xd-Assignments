#include"func.h"

void CheckCapacity(Contact* ps) {
	if (ps->size == ps->capacity) {
		PeoInfo* ptr= realloc(ps->data, (ps->capacity + 2) * sizeof(PeoInfo));
		if (ptr != NULL) {
			ps->data = ptr;
			ps->capacity += 2;
		//	printf("增容成功\n");
		} else {
			perror("增容失败");
		}
	}
}
void LoadContact(Contact* ps) {
	PeoInfo tmp = { 0 };
	FILE* pfRead = fopen("contat.txt", "rb");
	if (pfRead == NULL) {
		perror("LoadContact");
		return;
	}
	while (fread(&tmp, sizeof(PeoInfo), 1, pfRead)) {
		CheckCapacity(ps);
		ps->data[ps->size] = tmp;
		ps->size++;
	}
	//读取文件，放在通讯录中
	fclose(pfRead);
	pfRead = NULL;
}
void InitContact(Contact* ps) {
	ps->data =(PeoInfo*) malloc(3 * sizeof(PeoInfo));
	if (ps->data == NULL) {
		perror("通讯录初始化失败");
		return;
	}
	ps->size = 0;
	ps->capacity = DEFAULT_SZ;//设置通讯录最初只有0个元素
	LoadContact(ps);
	//把文件中已经存放的信息加载到通讯录中
}
void AddContact(Contact* ps) {
	CheckCapacity(ps);//检测通讯录容量，满了增容，不满不干事。
	printf("请输入名字：");
	scanf("%s", ps->data[ps->size].name);
	printf("请输入年龄：");
	scanf("%d", &(ps->data[ps->size].age));
	printf("请输入性别：");
	scanf("%s", ps->data[ps->size].sex);
	printf("请输入电话：");
	scanf("%s", ps->data[ps->size].tele);
	printf("请输入地址：");
	scanf("%s", ps->data[ps->size].addr);
	ps->size++;
	printf("添加成功\n");
}
void ShowContact(const Contact* ps) {
	if (ps->size == 0) {
		printf("通讯录为空\n");
	} else {
		int i = 0;
		printf("%-20s\t %-4s\t %-5s\t %-12s\t %-20s\n", "名字", "年龄", "性别", "电话", "地址");
		for (i = 0; i < ps->size; i++) {
			printf("%-20s\t %-4d\t %-5s\t %-12s\t %-20s\n",
			       ps->data[i].name, ps->data[i].age, ps->data[i].sex, ps->data[i].tele, ps->data[i].addr);
		}
	}
}
static int FindByName(const Contact* ps, char name[MAX_NAME]) {
	int i = 0;
	for (i = 0; i < ps->size; i++) {
		if (strcmp(ps->data[i].name, name) == 0) {
			return i;
		}
	}
	return -1;
}//定义函数查找删除人的位置，找到了返回名字所在元素下标，找不到返回-1
void DelContact(Contact* ps) {
	char name[MAX_NAME];
	printf("请输入要删除人的名字：\n");
	scanf("%s",name);
	int pos = FindByName(ps, name); //运用查找删除人的位置函数
	if (pos==-1) {
		printf("要删除的人不存在\n");
	} else {
		int j = 0;
		for (j = pos; j <ps->size-1 ; j++) {
			ps->data[j] = ps->data[j + 1];
		}
		ps->size--;
		printf("删除成功\n");
	}
}
void SearchContact(const  Contact* ps) {
	char name[MAX_NAME];
	printf("请输入要查找人的姓名：");
	scanf("%s", name);
	int pos = FindByName(ps, name);
	if (pos == -1) {
		printf("要查找的人不存在\n");
	} else {
		printf("%-20s\t %-4s\t %-5s\t %-12s\t %-20s\n", "名字", "年龄", "性别", "电话", "地址");
		printf("%-20s\t %-4d\t %-5s\t %-12s\t %-20s\n",
		       ps->data[pos].name, ps->data[pos].age, ps->data[pos].sex, ps->data[pos].tele, ps->data[pos].addr);

	}
}
void ModifyContact(Contact* ps) {
	char name[MAX_NAME];
	printf("请输入要修改人的名字：");
	scanf("%s", name);
	int pos = FindByName(ps, name);
	if (pos == -1) {
		printf("要修改人的信息不存在\n");
	} else {
		printf("请输入名字：");
		scanf("%s", ps->data[pos].name);
		printf("请输入年龄：");
		scanf("%d", &(ps->data[pos].age));
		printf("请输入性别：");
		scanf("%s", ps->data[pos].sex);
		printf("请输入电话：");
		scanf("%s", ps->data[pos].tele);
		printf("请输入地址：");
		scanf("%s", ps->data[pos].addr);
		printf("修改完成\n");
	}
}
void DestroyContact(Contact* ps) {
	free(ps->data);
	ps->data = NULL;
}
void SaveContact(Contact* ps) {
	FILE* pfWrite = fopen("contat.txt", "wb");
	if (pfWrite == NULL) {
		perror("保存通讯录失败:%s\n");
		return;
	}
	int i = 0;
	for (i = 0; i < ps->size; i++) {
		fwrite(&(ps->data[i]), sizeof(PeoInfo), 1, pfWrite);
	}
	fclose(pfWrite);
	pfWrite = NULL;
	printf("保存成功\n");
}

void ExportContact(Contact* ps) {
	int i=0;
	char addr[40];
	printf("请输入你要保存的路径及文件名:\n");
	scanf("%s",addr);
	FILE *pfExport = fopen(addr, "w");
	if (pfExport == NULL) {
		perror("通讯录数据导出失败：");
		return;
	}
	fprintf(pfExport,"%-20s\t %-4s\t %-5s\t %-12s\t %-20s\n", "名字", "年龄", "性别", "电话", "地址");
	for (i = 0; i < ps->size; i++) {
		fprintf(pfExport,"%-20s\t %-4d\t %-5s\t %-12s\t %-20s\n",
		        ps->data[i].name, ps->data[i].age, ps->data[i].sex, ps->data[i].tele, ps->data[i].addr);
	}

	fclose(pfExport);
	pfExport = NULL;
}
