from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Первый набор команд будет открываться при использовании команд "/start"
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="расписание на сегодня"),
            KeyboardButton(text="настройка расписания"),
        ],
        [
            KeyboardButton(text="информация"),
        ],
    ],
    resize_keyboard=True,
)

# Второй набор кнопок, для редактирования расписания

timetable_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="понедельник"),
        ],
        [
            KeyboardButton(text="вторник"),
        ],
        [
            KeyboardButton(text="среда"),
        ],
        [
            KeyboardButton(text="четверг"),
        ],
        [
            KeyboardButton(text="пятница"),
        ],
        [
            KeyboardButton(text="суббота"),
        ],
        [
            KeyboardButton(text="воскресенье"),
        ],
        [
            KeyboardButton(text="вернутся"),
        ],
    ],
    resize_keyboard=True,
)


# выбор пользователя редактировать расписание или нет

choice_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="изменить")],
        [
            KeyboardButton(text="назад"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
