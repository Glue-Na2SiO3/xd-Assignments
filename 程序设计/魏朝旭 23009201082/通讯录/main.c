#include"func.h" 
void menu()
{
	printf("***********************************\n");
	printf("******1.add        2.del    *******\n");
	printf("******3.search     4.modify *******\n");
	printf("******5.show       6.save   *******\n");
	printf("******7.export     0.exit   *******\n");
	printf("***********************************\n");
}

int main()
{
	int input = 0;
	Contact con;//con就是通讯录，里面包含data指针,size,capacity 
	InitContact(&con);//初始化通讯录 
	do
	{
		menu();
		printf("请选择：");
		scanf("%d", &input);
		switch (input)
		{
		case ADD:
			AddContact(&con);
			break;
		case DEL:
			DelContact(&con);
			break;
		case SEARCH:
			SearchContact(&con);
			break;
		case MODIFY:
			ModifyContact(&con);
			break;
		case SHOW:
			ShowContact(&con);
			break;
		case EXIT:
			SaveContact(&con);
			DestroyContact(&con);
			printf("退出通讯录\n");
			break;
        case SAVE:
			SaveContact(&con);
			break;
		case EXPORT:
			ExportContact(&con);
			break; 
		default:
			printf("选择错误\n");
			break;
		};
	} while (input);

	return 0;
}
