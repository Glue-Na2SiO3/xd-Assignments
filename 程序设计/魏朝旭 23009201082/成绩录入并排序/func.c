#include "func.h"

void readStudents(const char *filename, Student students[], int *numStudents) {  
    FILE *file = fopen(filename, "r");  
    if (!file) {  
        perror("Error opening file");  
        exit(EXIT_FAILURE);  
    }  
  
    char line[MAX_LINE_LENGTH];  
    while (fgets(line, sizeof(line), file) && *numStudents < MAX_STUDENTS) {  
        char *token = strtok(line, " \n");  
        if (token) {  
            strcpy(students[*numStudents].name, token);  
            token = strtok(NULL, " \n");  
            students[*numStudents].subject1 = atof(token);  
            token = strtok(NULL, " \n");  
            students[*numStudents].subject2 = atof(token);  
            token = strtok(NULL, " \n");  
            students[*numStudents].subject3 = atof(token);  
            (*numStudents)++;  
        }  
    }  
  
    fclose(file);  
}  
  
void calculateAverage(Student students[], int numStudents) { 
	int i=0; 
    for (i = 0; i < numStudents; i++) {  
        students[i].average = (students[i].subject1 + students[i].subject2 + students[i].subject3) / 3.0;  
    }  
}  
  
void sortStudents(Student students[], int numStudents) {  
	int i=0,j=0;
    for (i = 0; i < numStudents; i++) {  
        for (j = i+1; j < numStudents; j++) {  
            if (students[j].average > students[i].average) {  
                Student temp = students[j];  
                students[j] = students[i];  
                students[i] = temp;  
            }  
        }  
    }  
}  
  
void writeStudents(const char *filename, Student students[], int numStudents) {  
	int i=0;
    FILE *file = fopen(filename, "w");  
    if (!file) {  
        perror("输出成绩单创建失败");  
        exit(EXIT_FAILURE);  
    }  
  
    for (i = 0; i < numStudents; i++) {  
        fprintf(file, "%d %s %.2f %.2f %.2f %.2f\n", i + 1, students[i].name, students[i].average, students[i].subject1, students[i].subject2, students[i].subject3);  
    }  
  
    fclose(file);  
}
