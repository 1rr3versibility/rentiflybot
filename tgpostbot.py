import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Установите свой токен, полученный от BotFather
BOT_TOKEN = "7500637659:AAFzthnXpgYx-TNDmVlxFCGac_UqRnPwFao"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Функция, которая будет отправлять второе сообщение с задержкой
async def send_delayed_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет отложенное сообщение с текстом и ссылками."""
    job = context.job

    # Текст второго сообщения
    text = (
        "Если вы не собираетесь прямо сейчас сдавать квартиру, то подпишитесь на наш телеграм-канал. "
        "Там мы подробно рассказываем о долгосрочной аренде жилья и нашем сервисе. Начать можно с постов:\n\n"

        "▪️ <a href='https://t.me/rentifly/45'>Как найти надежного жильца без встречи с ним</a>\n"
        "▪️ <a href='https://t.me/rentifly/38'>Как правильно выставить цену аренды</a>\n"
        "▪️ <a href='https://t.me/rentifly/43'>Как сохранить квартиру в идеальном состоянии без лишних проверок</a>\n"
        "▪️ <a href='https://t.me/Rentifly_requestBot'>Как правильно сдавать квартиру. 22 файла для арендодателя</a>\n\n"

        "Тут можете почитать отзывы наших клиентов — <a href='https://otzovik.com/reviews/rentifly_ru-servis_umnoy_arendi/'>ТЫК</a>\n\n"
        "Если вы агент, то для вас у нас есть специальные условия, подробнее тут — <a href='https://t.me/rentiflyPro'>@rentiflyPro</a>\n\n"

    )

    await context.bot.send_message(
        chat_id=job.chat_id,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду /start, отправляет первое сообщение и планирует отправку второго."""
    user_id = update.effective_user.id
    redirect_url = "https://rentifly.ru"

    logger.info("Пользователь %s запустил бота.", user_id)

    if context.args:
        query_string = " ".join(context.args)
        utm_campaign_raw = query_string.replace('utm_campaign=', '')

        logger.info("Получены параметры от пользователя %s: %s", user_id, utm_campaign_raw)

        if "snyatkvartiru_Moscow" in utm_campaign_raw:
            redirect_url = "https://rentifly.ru?utm_campaign=snyatkvartiru_Moscow_07_25&utm_source=TG&utm_medium=TG_F_S"
        elif "tg_estate_news" in utm_campaign_raw:
            redirect_url = "https://rentifly.ru?utm_campaign=tg_estate_news_07_25&utm_source=TG&utm_medium=TG_F_S"
        elif "betonest" in utm_campaign_raw:
            redirect_url = "https://rentifly.ru?utm_campaign=betonest_07_25&utm_source=TG&utm_medium=TG_F_S"
        elif "kvadratnymaster" in utm_campaign_raw:
            redirect_url = "https://rentifly.ru?utm_campaign=kvadratnymaster_07_25&utm_source=TG&utm_medium=TG_F_S"
        elif "Serbia" in utm_campaign_raw:
            redirect_url = "https://rentifly.ru?start=utm_campaign=Serbia_07_25&utm_source=TG&utm_medium=TG_F_S"
        elif "chp_sochi" in utm_campaign_raw:
            redirect_url = "https://rentifly.ru?start=utm_campaign=chp_sochi_07_25&utm_source=TG&utm_medium=TG_F_S"
        else:
            # Если параметры не совпали, используем URL по умолчанию
            logger.warning("Параметры не совпали для пользователя %s. Используется URL по умолчанию.", user_id)
            redirect_url = "https://rentifly.ru"
    else:
        logger.info("Пользователь %s запустил бота без параметров.", user_id)

    logger.info("URL для ссылки: %s", redirect_url)

    rentifly_link = f'<a href="{redirect_url}">Rentifly</a>'

    # Текст первого сообщения
    text = (
        "Как сдать квартиру через Rentifly\n\n"
        f"🔸 Оставьте заявку на нашем сайте — {rentifly_link}\n"
        "🔸 Менеджер свяжется с вами, ответит на все вопросы и запланирует встречу\n"
        "🔸 Сделаем фото для объявления и зафиксируем состояние квартиры\n"
        "🔸 Составим договор и привяжем карту для выплат.\n\n"
        "Благодаря отсутствию комиссии риелтеру мы быстро находим арендаторов. В среднем это занимает 4 дня.\n\n"
        "Для собственника подключение бесплатно."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

    # Планируем отправку второго сообщения через 5 минут (300 секунд)
    context.job_queue.run_once(send_delayed_message, 300, chat_id=update.effective_chat.id,
                               name=str(update.effective_chat.id))


def main() -> None:
    """Запускает бота."""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()