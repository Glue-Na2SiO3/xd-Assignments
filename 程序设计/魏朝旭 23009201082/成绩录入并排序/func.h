#include <stdio.h>  
#include <stdlib.h>  
#include <string.h>  
 
#define MAX_LINE_LENGTH 256  
#define MAX_STUDENTS 100  
#define MAX_NAME_LENGTH 20 
#define INPUT_FILE "students.txt"  
#define OUTPUT_FILE "sorted_students.txt"  
  
typedef struct {  
    char name[MAX_NAME_LENGTH];  
    float subject1;  
    float subject2;  
    float subject3;  
    float average;  
} Student;  
  
void readStudents(const char *filename, Student students[], int *numStudents);  
void calculateAverage(Student students[], int numStudents);  
void sortStudents(Student students[], int numStudents);  
void writeStudents(const char *filename, Student students[], int numStudents);  
