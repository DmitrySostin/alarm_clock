import flet as ft

file_alarm_time = 'alarm.csv'
day_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

text = ft.Text()  # Вывод тектса
check_monday = ft.Switch(label=" Monday", value=False)  # Чекбокс установки срабатывания по дням недели
check_tuesday = ft.Switch(label=" Tuesday", value=False)  # Чекбокс установки срабатывания по дням недели
check_wednesday = ft.Switch(label=" Wednesday", value=False)  # Чекбокс установки срабатывания по дням недели
check_fhursday = ft.Switch(label=" Thursday", value=False)  # Чекбокс установки срабатывания по дням недели
check_friday = ft.Switch(label=" Friday", value=False)  # Чекбокс установки срабатывания по дням недели
check_saturday = ft.Switch(label=" Saturday", value=False)  # Чекбокс установки срабатывания по дням недели
check_sunday = ft.Switch(label=" Sunday", value=False)  # Чекбокс установки срабатывания по дням недели
check_logic = ft.Switch(label=" Logic", value=False)  # Чекбокс сброс по логической задаче!!!
button_save = ft.ElevatedButton(text=" Submit", on_click=save)  # Кнопка  сохранения