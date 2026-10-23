#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define Max_Line 1024
#define Max_History 10

// 历史记录结构体
typedef struct {
    char command[Max_Line];
    int number;
} History;

// 历史记录数组
History history[Max_History];
int history_index = 0; // 当前历史命令的数量
int history_number = 0; // 当前历史命令的编号

// 分割命令函数
void split_command(char *input, char **args) {
    char *token;
    char *delim = " ";
    int i = 0;

    while ((token = strtok(input, delim)) != NULL) {
        if (i > 0 && token[0] == '"' && token[strlen(token) - 1] == '"') {
            // Remove the quotes from the token
            token[strlen(token) - 1] = '\0'; // 删除末尾的引号
            args[i++] = token + 1; // 跳过开头的引号
        } else {
            args[i++] = token;
        }
        input = NULL; // strtok 设置为 NULL，以便从上一次调用的位置开始搜索下一个 token
    }
    args[i] = NULL;
}

// 执行命令
void execute_command(char **args) {
    pid_t pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        // 子进程
        if (execvp(args[0], args) == -1) {
            perror("execvp");
            exit(EXIT_FAILURE);
        }
    } else {
        // 父进程
        int status;
        waitpid(pid, &status, 0);
        if (WIFEXITED(status)) {
            printf("Command exited with status %d\n", WEXITSTATUS(status));
        }
    }
}

// 保存命令到历史记录
void add_to_history(char *command) {
    if (history_index < Max_History) {
        strcpy(history[history_index].command, command);
        history[history_index].number = ++history_number;
        history_index++;
    } else {
        // 如果历史记录已满，覆盖最早的命令
        history[0] = history[history_index - 1];
        history[0].number = ++history_number;
        history_index = Max_History;
    }
}

// 显示历史记录
void show_history() {
    if (history_index == 0) {
        printf("No commands in history\n");
        return;
    }
    printf("History:\n");
    for (int i = history_index - 1; i >= 0; i--) {
        printf("%d: %s\n", history[i].number, history[i].command);
    }
}

// 执行历史命令
void execute_history_command(char *input) {
    char *num = strtok(input + 1, " ");
    if (num == NULL) {
        // 执行最新命令
        if (history_index > 0) {
            char *command_args[Max_Line/2+1];
            split_command(history[history_index - 1].command, command_args);
            execute_command(command_args);
        } else {
            printf("No commands in history\n");
        }
    } else {
        int index = atoi(num);
        if (index > 0 && index <= history_index) {
            // 执行指定编号的命令
            char *command_args[Max_Line/2+1];
            split_command(history[index - 1].command, command_args);
            execute_command(command_args);
        } else {
            // 无效的命令编号
            printf("No such command in history\n");
        }
    }
}

int main() {
    char buffer[Max_Line];
    char *args[Max_Line/2+1];

    while (1) {
        printf("osh> ");
        fgets(buffer, Max_Line, stdin);
        buffer[strcspn(buffer, "\n")] = 0;

        if (strcmp(buffer, "exit") == 0) {
            break;
        } else if (strncmp(buffer, "!!", 2) == 0) {
            // 执行最新命令
            execute_history_command(buffer);
        } else if (strncmp(buffer, "!", 1) == 0) {
            // 执行指定编号的命令
            execute_history_command(buffer);
        } else {
            // 分割命令并执行
            split_command(buffer, args);
            execute_command(args);

            // 保存命令到历史记录
            add_to_history(buffer);
        }
    }

    return 0;
}
