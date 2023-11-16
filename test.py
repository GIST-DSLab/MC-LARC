# 파일을 쓰기 모드로 엽니다.
with open("tasks.txt", "w") as file:
    # task_0부터 task_399까지 텍스트 파일에 작성합니다.
    for i in range(400):
        file.write(f"task_{i}:\n")
        if (i + 1) % 5 == 0:  # 5 문제마다 한 줄씩 띄웁니다.
            file.write("\n")
