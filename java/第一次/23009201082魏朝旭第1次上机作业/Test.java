package com.xuexi.calendar;
import java.util.Scanner;
public class Test {
	public static void main(String[] args) {
		System.out.println("该程序有两种功能:");
		System.out.println("功能一（代号为1）:输出您指定年份的日历");
		System.out.println("功能二（代号为2）:输出您指定日期的星期");
		System.out.println("输入其他数字将结束程序。");
		System.out.println("注：由于1900年1月1日作为基准，所有的日期只能在1900年之后。");
		Scanner scanner = new Scanner(System.in);
		while (true) {

			System.out.print("请输入功能代号：");
			int cmd = scanner.nextInt();
			if (cmd == 1) {
				// 方便函数内部读取用户输入，直接将scanner作为参数传入函数
				printYearCalendar(scanner);
			} else if (cmd == 2) {
				printWeekday(scanner);
			} else {
				System.out.println("哈哈，程序退出了，再见！！！");
				break;
			}
		}
		scanner.close();
	}

	private static void printWeekday(Scanner scanner) {
		int[] daysInMonth = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
		System.out.print("请输入指定日期的年：");
		int year = scanner.nextInt();
		if(isLeapYear(year)){
			daysInMonth[1]=29;
		}
		System.out.print("请输入指定日期的月：");
		int month = scanner.nextInt();
		// 保证输入的月份正常在1-12内
		while (month<1||month>12){
			System.out.println("您输入的月份不对，请重新输入试试？");
			System.out.print("请输入指定日期的月：");
			month = scanner.nextInt();
		}
		System.out.print("请输入指定日期的日：");
		int day = scanner.nextInt();
		while (day<1||day>daysInMonth[month-1]){
			System.out.println("您输入月份没有这一天，是不是输错了？重新输入试试把！");
			System.out.print("请输入指定日期的日：");
			day = scanner.nextInt();
		}
		int weekday=(getFirstDayOfWeek(year, month)+day-1)%7;
		String[] daysOfWeek = {  "Sunday", "Monday",  "Tuesday",  "Wednesday",  "Thursday",  "Friday",  "Saturday"    };
		System.out.println(daysOfWeek[weekday]);
	}
	private static void printYearCalendar(Scanner scanner) {
		System.out.print("请输入一个年份：");
		int year = scanner.nextInt();
		// 遍历每一个月份
		for (int month = 1; month <= 12; month++) {
			printMonth(year,month);
		}
	}

	private static void printMonth(int year, int month) {
		// 定义每个月的默认天数
		int[] daysInMonth = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

		String[] monthNames = {"", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
		// 闰年2月29天
		if(month == 2 && isLeapYear(year)){
			daysInMonth[1] = 29;
		}
		// 打印月份名称
		System.out.println("\n"+monthNames[month]);
		// 打印周六到周日的标题
		System.out.println("Sun Mon Tue Wed Thu Fri Sat");
		// 计算这个月的第一天是星期几（0为周天，1为周一……）
		int firstDay = getFirstDayOfWeek(year,month);
		// 打印空格直到这个月的第一天
		for (int i = 0; i < firstDay; i++) {
			System.out.print("    ");
		}
		// 打印这个月每一天
		for(int day = 1;day <=daysInMonth[month-1];day++){
			System.out.printf("%-4d", day);
			//打印到周六或者这个月结束就换行
			if ((firstDay+day-1)%7==6||day==daysInMonth[month-1]) {
				System.out.println();
			}
		}
	}

	// 判断是否为闰年
	private static boolean isLeapYear(int year) {
		return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
	}

	// 计算某年某月的第一天是星期几（0代表星期天，1代表星期一，依此类推）
	private static int getFirstDayOfWeek(int year, int month) {
		int[] daysInMonth = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
		if(isLeapYear(year)){
			daysInMonth[1] = 29;
		}
		// 经过查询，设置基准日期：1900年1月1日是星期一（这里假设为1，代表星期一）
		int baseYear = 1900;
		int baseMonth = 1;
		int baseWeekday = 1; // 星期一
		int totalDays = 0;

		// 计算基准日期到目标日期之间的总天数
		for (int y = baseYear; y < year; y++) {
			totalDays += isLeapYear(y) ? 366 : 365;
		}

		for (int m = baseMonth; m < month; m++) {
			totalDays += daysInMonth[m - 1];
		}

		// 计算并返回目标日期的星期几（0代表星期天，1代表星期一，依此类推）
		return (baseWeekday + totalDays) % 7;
	}
}
