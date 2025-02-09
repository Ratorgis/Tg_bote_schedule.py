from aiogram.types import Message
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from datetime import datetime
import aiogram.utils.markdown as fmt
from kbds import reply


# Алгоритм необходимый для более приятного вывода расписания
def fine_format_string(input_str):
    # Разбиваем строку на отдельные строки и удаляем лишние пробелы
    lines = input_str.strip().split("\n")
    # Добавляем порядковые номера к каждой строке
    numbered_lines = [f"{i+1}) {line}" for i, line in enumerate(lines)]
    output_str = "\n".join(numbered_lines)  # Объединяем строки обратно в одну строку
    return output_str


# Добавление пользователя прав для записи в расписание, переключатель для различия записи вне команды и плана расписания
writer = {}

# Показание на какой день недели пользователь хочет записать расписание
week_days_writer = {}

# В функции writer и week_days_writer ключи - id пользователя, для writer значение - 1(Может записывать) или 0 (Нет), week_days_writer значение - номер дня недели

# Хранение расписания пользователей, ключ - id пользователя, значение - массив из 7 других массивов для каждого дня недели
memory = {}


week_days_translate = [  # будет использоваться для вывода дня недели по индексу
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]


week_days = {  # Словарь, который необходим для работы week_days_writer
    "понедельник": 0,
    "Monday": 0,
    "вторник": 1,
    "Tuesday": 1,
    "среда": 2,
    "Wednesday": 2,
    "четверг": 3,
    "Thursday": 3,
    "пятница": 4,
    "Friday": 4,
    "суббота": 5,
    "Saturday": 5,
    "воскресенье": 6,
    "Sunday": 6,
}

user_router = Router()


@user_router.message(CommandStart())
async def get_start(message: Message):
    writer[message.from_user.id] = 0  # Сразу выставил права на 0
    await message.answer(
        "Здравствуйте!\nЯ - телеграмм бот, который поможет вам эффективно записывать планы на день",
        reply_markup=reply.main_kb,
    )


@user_router.message(F.text.lower() == "информация")
async def short_information(message: Message):
    await message.answer(
        fmt.text(
            fmt.text(fmt.hbold("Информация о возможности бота")),
            fmt.text(),
            fmt.text(
                fmt.hbold("1."),
                "Хранение вашего расписания(заметок, событий не связанных со временем) на любой день недели.",
            ),
            fmt.text(),
            fmt.text(
                fmt.hbold(
                    "2. Вывод расписания на текущей день по нажатию одной кнопки."
                ),
                "алгоритмы бота позволяют автоматически определять текущей день недели и выводить ваши планы.",
            ),
            fmt.text(),
            fmt.text(
                fmt.hbold("3. Свобода записи."),
                "Вы можете записывать все, что только захотите, бот будет корректно выводить запланированное.",
            ),
            fmt.text(),
            fmt.text(
                fmt.hbold("4."),
                " Бот написан на Python, используя модуль aiogram. Дополнитель информацию можно найти в описании бота.",
            ),
            sep="\n",
        ),
        parse_mode="HTML",
    )


@user_router.message(F.text.lower() == "настройка расписания")
async def setting_up(message: Message):
    # Добавление id пользователя, где значение 0
    week_days_writer[message.from_user.id] = 0
    # Проверка на существование ключа-значения в memory этого пользователя
    if message.from_user.id in memory:
        await message.answer(
            "Выбирайте, какой день недели хотите настроить:",
            reply_markup=reply.timetable_kb,
        )
    else:
        # Создание, если такого не было
        memory[message.from_user.id] = [[] * n for n in range(7)]
        await message.answer(
            "Выбирайте, какой день недели хотите настроить",
            reply_markup=reply.timetable_kb,
        )


@user_router.message(F.text.lower() == "расписание на сегодня")
async def timetable_weekday(message: Message):
    # Получаю текущий день недели благодаря datetime
    current_date = datetime.now().strftime("%A")
    number_day = week_days[current_date]  # Получаю индекс дня недели
    if message.from_user.id in memory:
        await message.answer(
            f"Планы на сегодня - {week_days_translate[number_day]}\n\n{fine_format_string(memory[message.from_user.id][number_day])}"  # Вывожу день недели и через memory вывожу расписание пользователя на этот день
        )
    else:
        await message.answer(
            'Простите, но вы еще не настроили свое расписание.\nВоспользуйтесь кнопкой "настройка расписания"'
        )


@user_router.message()
async def echo(message: types.Message):
    # Получил на ввод, какой-то день недели, который дальше переводим в week_days_writer, те в какой день недели пользователь хочет вставить свое расписание
    if (message.text in week_days) == True:
        index = week_days[message.text]
        week_days_writer[message.from_user.id] = index
        if len(memory[message.from_user.id][index]) == 0:
            await message.answer(
                "К сожалению, у вас еще ничего не запланировано на этот день.",
                reply_markup=reply.choice_kb,
            )
        else:
            await message.answer(
                f"Вот ваше расписание на этот день:\n\n{memory[message.from_user.id][index]}",
                reply_markup=reply.choice_kb,
            )
    elif message.text == "изменить":
        # Изменение прав на 1, для адекватного получение расписание
        writer[message.from_user.id] = 1
        await message.answer(
            fmt.text(
                fmt.text(fmt.hbold("Памятка по изменениям")),
                fmt.text(),
                fmt.text(
                    fmt.hbold("1. Запись."),
                ),
                fmt.text(
                    "Если хотите записывать несколько дел сразу, то стоит разделить их символом '\\n'. Это можно сделать сочетанием клавиш 'Ctrl+Enter', или кнопкой 'Ввод'.",
                ),
                fmt.text(),
                fmt.text(
                    fmt.hbold("2. Добавление / Замена / Удаление."),
                ),
                fmt.text(
                    "Если хотите сделать одну из этих операций, то стоит посто скопировать предварительный ид ваших планов на день, который выдает бот. И проделать необходимые вам операции."
                ),
                sep="\n",
            ),
            parse_mode="HTML",
        )
    else:
        if writer[message.from_user.id] == 1:  # Вот тут замечательная проверка прав
            memory[message.from_user.id][
                week_days_writer[message.from_user.id]
            ] = message.text  # Сама запись расписания
            await message.answer(
                "Ваши планы успешно записаны",
                reply_markup=reply.choice_kb,
            )
            # Вернул права на запись в базовое значение
            writer[message.from_user.id] == 0
        else:
            # Пользователь написал откровенную чушь
            await message.answer("Воспользуйтесь командами бота")
