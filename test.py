import flet as ft
import csv
import time
from datetime import datetime
import threading
import os
import pygame


def main(page: ft.Page):
    page.title = "Часы с будильником"
    page.window.width = 400
    page.window.height = 750
    page.theme_mode = ft.ThemeMode.LIGHT

    pygame.mixer.init()

    # Проверка и создание файла будильников
    if not os.path.exists('alarm.csv'):
        with open('alarm.csv', 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["hour", "minute", "monday", "tuesday", "wednesday",
                             "thursday", "friday", "saturday", "sunday", "melody"])

    def save(e):
        """Сохранение будильника в CSV файл"""
        try:
            conf = [
                dd_hour.value,
                dd_minute.value,
                check_monday.value,
                check_tuesday.value,
                check_wednesday.value,
                check_thursday.value,
                check_friday.value,
                check_saturday.value,
                check_sunday.value,
                dd_melody.value
            ]

            with open('alarm.csv', 'a', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(conf)

            page.open(ft.SnackBar(ft.Text(f"Saved")))
            page.update()

            read_alarm()                                                    # Обновляем список будильников

        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {str(e)}"))
            page.snack_bar.open = True
            page.update()

    def read_alarm():
        """Чтение сохраненных будильников из файла"""
        try:
            alarms_list.controls.clear()
            with open("alarm.csv", 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Пропускаем заголовок
                for row in reader:
                    if len(row) >= 9:  # Проверяем, что строка содержит все необходимые данные
                        days = []
                        if row[2] == 'True': days.append("monday")
                        if row[3] == 'True': days.append("tuesday")
                        if row[4] == 'True': days.append("wednesday")
                        if row[5] == 'True': days.append("thursday")
                        if row[6] == 'True': days.append("friday")
                        if row[7] == 'True': days.append("saturday")
                        if row[8] == 'True': days.append("sunday")

                        alarms_list.controls.append(
                            ft.ListTile(
                                title=ft.Text(f"{row[0]}:{row[1]}"),
                                subtitle=ft.Text(f"Dey: {', '.join(days)} \nMelody: {row[9]}"),
                            )
                        )
            alarms_list.update()
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")

    def play_sound(melody_name):
        """Воспроизведение выбранной мелодии"""
        try:
            # Соответствие между названиями и файлами
            melody_map = {
                "melody_1": "alarm_sound_1.mp3",
                "melody_2": "alarm_sound_1.mp3",
                "melody_3": "alarm_sound_2.mp3",
                "melody_4": "alarm_sound_2.mp3"
            }

            # Путь к папке со звуками
            sound_path = os.path.join("alarm_sounds", melody_map.get(melody_name, "alarm_sound_1.mp3"))

            # Инициализация микшера, если еще не инициализирован
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            # Загрузка и воспроизведение звука
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(loops=-1)  # Бесконечное повторение

        except Exception as e:
            print(f"Ошибка воспроизведения звука: {e}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка воспроизведения звука!"))
            page.snack_bar.open = True
            page.update()

    def stop_sound():
        """Остановка воспроизведения звука"""
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except Exception as e:
            print(f"Ошибка остановки звука: {e}")

    def check_alarms():
        """Проверка срабатывания будильников"""
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M")

            try:
                with open("alarm.csv", 'r') as file:
                    reader = csv.reader(file)
                    next(reader)
                    for row in reader:
                        if len(row) >= 10:
                            alarm_time = f"{row[0]}:{row[1]}"
                            melody = row[9]

                            if alarm_time == current_time:
                                print("active")
                                day_active = True
                                if day_active:
                                    # Воспроизводим звук
                                    play_sound(melody)

                                    def close_dialog(e):                            # Закрываем всплывающее окно и стоп музыка
                                        stop_sound()
                                        dialog.open = False
                                        page.update()

                                    dialog = ft.AlertDialog(                        # Всплывающее окно будильник
                                        modal=True,
                                        title=ft.Text("Alarm!"),
                                        content=ft.Text(f"{melody} in {alarm_time}"),
                                        actions=[ft.TextButton("OK", on_click=close_dialog)],
                                        actions_alignment=ft.MainAxisAlignment.END,
                                    )

                                    page.open(dialog)
                                    dialog.open = True
                                    page.update()
            except Exception as e:
                print(f"Ошибка проверки будильников: {e}")

            time.sleep(30)
    # Элементы интерфейса
    time_display = ft.Text(size=50, color=ft.Colors.GREEN)
    date_display = ft.Text(size=20, color=ft.Colors.GREY_600)

    # Часы
    clock_container = ft.Container(
        content=ft.Column(
            [time_display, date_display],
            #alignment="center",                                          #ft.alignment.center,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=50,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLUE_100),
    )

    # Установка будильника
    dd_hour = ft.Dropdown(
        options=[ft.dropdown.Option(f"{i:02d}") for i in range(24)],
        label="Hour",
        width=150,
    )

    dd_minute = ft.Dropdown(
        options=[ft.dropdown.Option(f"{i:02d}") for i in range(60)],
        label="Minute",
        width=150,
    )

    # Дни недели
    check_monday = ft.Switch(label="monday", value=False)
    check_tuesday = ft.Switch(label="tuesday", value=False)
    check_wednesday = ft.Switch(label="wednesday", value=False)
    check_thursday = ft.Switch(label="thursday", value=False)
    check_friday = ft.Switch(label="friday", value=False)
    check_saturday = ft.Switch(label="saturday", value=False)
    check_sunday = ft.Switch(label="sunday", value=False)

    # Мелодии
    dd_melody = ft.Dropdown(
        options=[
            ft.dropdown.Option("Melody 1"),
            ft.dropdown.Option("Melody 2"),
            ft.dropdown.Option("Melody 3"),
            ft.dropdown.Option("Melody 4"),
        ],
        label="Melody",
        width=150,
    )

    # Список будильников
    alarms_list = ft.ListView(expand=True)

    # Кнопка сохранения
    save_button = ft.ElevatedButton(
        text="Save",
        icon=ft.Icons.SAVE,
        on_click=save,
    )

    # Страницы
    home_page = ft.Column(
        [
            ft.Row([clock_container], alignment=ft.MainAxisAlignment.START),
            ft.Divider(height=20),
            ft.Text("Active alarm:", size=16, weight=ft.FontWeight.W_100),
            alarms_list
        ],
        scroll=ft.ScrollMode.ALWAYS
    )

    set_alarm_page = ft.Column(
        [
            ft.Row([dd_hour, dd_minute], alignment=ft.alignment.center),
            ft.Divider(height=10),
            ft.Text("Deys:", size=16, weight=ft.FontWeight.W_100),
            check_monday,
            check_tuesday,
            check_wednesday,
            check_thursday,
            check_friday,
            check_saturday,
            check_sunday,
            ft.Divider(height=10),
            dd_melody,
            ft.Divider(height=20),
            save_button
        ],
        scroll = ft.ScrollMode.ALWAYS
    )

    # Навигация
    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 0:
            page.add(home_page)
        elif index == 1:
            page.add(set_alarm_page)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
            ft.NavigationBarDestination(icon=ft.Icons.ALARM, label="Будильник"),
        ],
        on_change=navigate
    )

    # Обновление времени
    def update_time():
        while True:
            now = datetime.now()
            time_display.value = now.strftime("%H:%M:%S")
            date_display.value = now.strftime("%A, %d %B %Y")
            page.update()
            time.sleep(1)

    # Инициализация
    page.add(home_page)
    read_alarm()

    # Запуск потоков
    threading.Thread(target=update_time, daemon=True).start()
    threading.Thread(target=check_alarms, daemon=True).start()


ft.app(target=main)