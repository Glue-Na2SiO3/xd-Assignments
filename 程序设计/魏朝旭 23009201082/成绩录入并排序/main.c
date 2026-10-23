#include"func.h"

int main() {  
    Student students[MAX_STUDENTS];  
    int numStudents = 0;  
  
    /* 读取学生信息 */  
    readStudents(INPUT_FILE, students, &numStudents);  
  
    /* 计算平均成绩 */ 
    calculateAverage(students, numStudents);  
  
    /* 按平均成绩排序  */
    sortStudents(students, numStudents);  
  
    /* 写入排序后的学生信息 */
    writeStudents(OUTPUT_FILE, students, numStudents);  
  
    printf("排序后的成绩单成功创建于 %s\n", OUTPUT_FILE);  
    return 0;  
}  
