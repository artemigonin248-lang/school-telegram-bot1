from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8250696390:AAE8UFDQ8DmzpOw_hrEIitd2DbkpuEn8fVM"

main_keyboard = [
    ["📅 Расписание"],
    ["🏫 О школе", "📞 Контакты"]
]

days_keyboard = [
    ["Понедельник", "Вторник"],
    ["Среда", "Четверг"],
    ["Пятница"],
    ["⬅ Назад"]
]

main_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
days_markup = ReplyKeyboardMarkup(days_keyboard, resize_keyboard=True)


def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except:
        return "Файл не найден."


def get_schedule_for_day(day):
    text = read_file("schedule.txt")
    parts = text.split("\n\n")

    for part in parts:
        if part.startswith(day):
            return part

    return "Расписание для этого дня не найдено."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Я школьный бот-помощник.\nВыберите раздел:",
        reply_markup=main_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📅 Расписание":
        await update.message.reply_text(
            "Выберите день недели:",
            reply_markup=days_markup
        )

    elif text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]:
        schedule = get_schedule_for_day(text)
        await update.message.reply_text(schedule)

    elif text == "🏫 О школе":
        await update.message.reply_text(read_file("info.txt"))

    elif text == "📞 Контакты":
        await update.message.reply_text(read_file("contacts.txt"))

    elif text == "⬅ Назад":
        await update.message.reply_text(
            "Вы вернулись в главное меню.",
            reply_markup=main_markup
        )

    else:
        await update.message.reply_text(
            "Пожалуйста, используйте кнопки меню."
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()

