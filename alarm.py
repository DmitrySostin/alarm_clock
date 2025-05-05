import csv
from config_alarm import file_alarm_time

def read_file_alarm():
    # чтение установок времени срабатывания будильника
    with open(file_alarm_time, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:          # первые 7 значениий дни недели в которые срабатывать
            for i in range(7):
                if int(row[i]) == 'y':
                    print('ON', end=' ')
                else:
                    print('OFF', end=' ')
            print(f'hour : {row[7]}', end=' ')
            print(f'minute: {row[8]}', end=' ')
            print(row[9])


def write_file_alarm(conf):
    #conf = ['0', '0', '0', '0', '0', '0', '0', '23', '30', '1']
    with open(file_alarm_time, 'a', newline="") as file:
        writer = csv.writer(file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows([conf])
