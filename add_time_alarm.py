from config_alarm import day_week
from alarm import write_file_alarm

conf = []
# задать будильник
flag = input("<<< Want to create a new alarm (Y)es/(N)o: ")
if flag.lower() == 'y':
    # задать повторения?
    repit = input("<<< Set repeats (Y)es/(N)o: ")
    if repit.lower() == 'y':
        for i in range(7):
            conf.append(input(f'<<< Set alarm for {day_week[i]} (Y)es/(N)o: '))
    else:
        for _ in range(7):
            conf.append('n')
    conf.append(int(input("<<< Set hour (0-24) :")))        # установка часы
    conf.append(int(input("<<< Set minute (0-59) :")))      # установка минуты
    check_up = input("<<< Check for wake up (Y)es/(N)o :")  # точное пробуждение
    if check_up.lower() == "y":
        conf.append('y')
    else:
        conf.append('n')
elif flag.lower() == 'n':
    print("остальная часть программы")
if len(conf) == 10:
    write_file_alarm(conf)
