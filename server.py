from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from chemical_laws import chemical_laws, building_substance, recognition, get_data, PeriodicTable, Acids, AcidResides
import make_database

make_database.main()

reply_keyboard = [['/reaction_response', '/substance_response'],
                  ['/help', '/stop']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start_reaction_response(update, context):
    await update.message.reply_text(
        "Введите реагенты в формате: А + Б, при этом сначала большие соединения - кислоты, соли и гидроксиды, "
        "например (если они есть), а затем - более лёгкие - оксиды или простые вещества")
    return 1


async def reaction_response(update, context):
    await update.message.reply_text(chemical_laws(recognition(update.message.text)))
    return ConversationHandler.END


async def start_substance_response(update, context):
    await update.message.reply_text("Введите вещество, данные о котором хотите узнать")
    return 1


async def substance_response(update, context):
    result = "Вещество не найдено"
    if len(update.message.text.split("+")) == 1:
        for i in [PeriodicTable, Acids, AcidResides]:
            text = building_substance(recognition(update.message.text))
            data = get_data(text, i)
            if data:
                result = data.wiki
    await update.message.reply_text(result)
    return ConversationHandler.END


async def stop(update, context):
    return ConversationHandler.END


async def help(update, context):
    await update.message.reply_text("Бот для работы с химическими реакциями и веществами.\n"
                                    "/reaction_response - введите реагенты, чтобы получить продукты реакции;\n"
                                    "/substance_response - введите элемент таблицы менделеева, кислоту или "
                                    "кислотный остаток для получения ссылки на википедию\n"
                                    "/help - справка\n"
                                    "/stop - отмена команды", reply_markup=markup)


def main():
    application = Application.builder().token("7075554962:AAEm5IHCA6cqozznouaD7-KzFHI4AVB9DoU").build()

    help_handler = CommandHandler(["help", "start"], help)
    reaction_handler = ConversationHandler(
        entry_points=[CommandHandler('reaction_response', start_reaction_response)],
        states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, reaction_response)]},
        fallbacks=[CommandHandler('stop', stop)]
    )
    response_handler = ConversationHandler(
        entry_points=[CommandHandler('substance_response', start_substance_response)],
        states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, substance_response)]},
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(reaction_handler)
    application.add_handler(response_handler)
    application.add_handler(help_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
