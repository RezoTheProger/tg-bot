import logging


from telegram import (

    KeyboardButton,

    KeyboardButtonPollType,

    Poll,

    ReplyKeyboardMarkup,

    ReplyKeyboardRemove,

    Update,

)

from telegram.constants import ParseMode

from telegram.ext import (

    Application,

    CommandHandler,

    ContextTypes,

    MessageHandler,

    PollAnswerHandler,

    PollHandler,

    filters,

)


# Enable logging

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

# set higher logging level for httpx to avoid all GET and POST requests being logged

logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)

import os
TOKEN = os.getenv("BOT_TOKEN")

Q_number = 0

QnA = [{"question":"1) Сколько максимум игроков может быть в комнате?","options":["5","10","15","20"], "answer":"15", "diff":0},
        {"question": "2)Кто может использовать вентиляцию?", "options": ["инженеры и предатели", "призраки и предатели","только предатели","все"], "answer": "инженеры и предатели","diff": 0},
        {"question": "3)Где расположены задания с картами в 'The Skeld' ?", "options": ["В Навигации", "В Реакторе","В Связи","В Админке"], "answer": "В Админке","diff": 0},
        {"question": "4)Кто может кикать игроков до начала игры?", "options": ["Участники с особой ролью", "Амонг Ас", "Хост", "Предатель"], "answer": "Хост","diff": 0},
        {"question": "5)Сколько максимум предателей могут быть в комнате?", "options": ["1", "5", "3", "2"], "answer": "3","diff": 0},
        {"question": "6)У кого нету никаких способностей?", "options": ["Инженер", "Предатель", "Мирный", "Фантом"], "answer": "Мирный","diff": 0},
        
    {
        "question": "7)В какой карте больше всего количество игроков?",
        "options": ["Mira HQ", "Polus", "AirShip", "The Skeld"],
        "answer": "The Skeld",
        "diff": 0
    },
    {
        "question": "8)Какое способность у паникера?",
        "options": ["летать", "прыгать через люк", "убивать", "звук при смерти"],
        "answer": "звук при смерти",
        "diff": 0
    },
    {
        "question": "9)Против кого играют предатели?",
        "options": ["мирных", "оборотня", "призраков", "всех"],
        "answer": "мирных",
        "diff": 0
    },
    {
        "question": "10)Что такое слово деф?",
        "options": ["опасный", "предатель", "чистый", "крутой"],
        "answer": "чистый",
        "diff": 0
    },
    {
        "question": "11)Что такое слово щуп?",
        "options": ["убить", "проголосовать", "ущипнуть", "кричать"],
        "answer": "проголосовать",
        "diff": 0
    },
    {
        "question": "12)Сколько задач (тасков) в игре у одного мирного в среднем?",
        "options": ["1–2", "3–4", "5–7", "8–10"],
        "answer": "5–7",
        "diff": 1
    }, 
    {
        "question": "13)На какой карте есть космическая станция с открытым пространством?",
        "options": ["Mira HQ", "Skeld", "Polus", "Airship"],
        "answer": "Skeld",
        "diff": 1
    },
    {
        "question": "14)Что произойдёт, если вы нажмёте кнопку собрания, когда активен саботаж?",
        "options": ["Будет собрание", "Предатель раскрыт", "Кнопка не сработает", "Случайная смерть"],
        "answer": "Кнопка не сработает",
        "diff": 1
    },
    {
        "question": "15)Кто может починить саботаж реактора?",
        "options": ["Только мирные", "Только предатели", "Два игрока любого типа", "Один игрок"],
        "answer": "Два игрока любого типа",
        "diff": 1
    },
    {
        "question": "16)На какой карте нельзя закрыть двери?",
        "options": ["Polus", "Mira HQ", "Skeld", "Airship"],
        "answer": "Mira HQ",
        "diff": 1
    },
    {
        "question": "17)Какой из этих саботажей можно устранить только вдвоём?",
        "options": ["Свет", "Кислород", "связь", "Не Знаю"],
        "answer": "Кислород",
        "diff": 1
    },
    {
        "question": "18)Сколько всего саботажей может сделать предатель на карте Skeld?",
        "options": ["3", "4", "5", "6"],
        "answer": "4",
        "diff": 1
    },
    {
        "question": "19)Что будет с инженером во время саботажа с связью?",
        "options": ["Нечего", "умрет", "Выпрыгнет с ...", "починит"],
        "answer": "Выпрыгнет с ...",
        "diff": 1
    },
    {
        "question": "20)Кто может рассекретить предателя не смотря на него?",
        "options": ["никто", "ученый", "предатель", "следопыт"],
        "answer": "следопыт",
        "diff": 1
    },
    {
        "question": "21)Может ли ученый вычислить предателя с помощью пульса?",
        "options": ["конечно", "да", "нет", "не знаю"],
        "answer": "нет",
        "diff": 1
    },
      {
        "question": "22)Что произойдёт, если ты убьёшь игрока прямо перед камерой на Skeld, но никто не смотрит?",
        "options": [
            "Тебя всё равно спалят",
            "Камера моргнёт",
            "Камера не зафиксирует",
            "Никто не узнает, пока не увидит тело"
        ],
        "answer": "Камера не зафиксирует",
        "diff": 2
    },
    {
        "question": "23)Максимальное количество времени между убийствами у предателя?",
        "options": ["15", "30", "60", "не знаю"],
        "answer": "60",
        "diff": 2
    },
    {
        "question": "24)Можно ли летать в Among Us?",
        "options": ["никак", "нет", "можно", "не знаю"],
        "answer": "можно",
        "diff": 2
    },
    {
        "question": "25)Сколько серверов существуют в Among Us?",
        "options": ["5", "больше 10", "3", "не знаю"],
        "answer": "3",
        "diff": 2
    },
    {
        "question": "26)Что не влияет на скорость перемещения в игре?",
        "options": [
            "Размер лобби",
            "Настройки хоста",
            "Количество предателей",
            "Баги"
        ],
        "answer": "Количество предателей",
        "diff": 2
    },
    {
        "question": "27)Что будет если наступить на зеленый гриб в Fungle?",
        "options": ["нечего", "будет анимка", "ты умрешь", "дым"],
        "answer": "дым",
        "diff": 2
    },
    {
        "question": "28)Какой самый лучший саботаж в Among Us?",
        "options": ["свет", "реактор", "связь", "грибной"],
        "answer": "грибной",
        "diff": 2
    },
    {
        "question": "29)Какая самая не популярная карта в Among Us?",
        "options": ["Fungle", "Mira", "AirShip", "Polus"],
        "answer": "AirShip",
        "diff": 2
    },
    {
        "question": "30)В какой карте связаны все люки?",
        "options": ["Skeld", "Mira", "Polus", "Airship"],
        "answer": "Mira",
        "diff": 2
    },
    {
        "question": "31)Кто основатель Among Us?",
        "options": ["Маркус", "Мистер Бист", "Эмилья", "Не знаю"],
        "answer": "Маркус",
        "diff": 2
    }, 
        {
        "question": "32) Прямо на ваших глазах убили мирного, у предателя кд (кулдаун) убийство 20 секунд, что бы вы сделали?",
        "options": ["Убежать", "Следить", "Репортнуть", "Ничего"],
        "answer": "Следить",
        "diff": 3
    }, 

        {
        "question": "33)Инженер заметил что ты Морфнулся и бежит в люк, ты не успеваешь убить его, так как он растояние далёкое, что бы вы сделали?",
        "options": ["Закрыть деври", "Отрицать свою ошибку", "Убежать", "Сделать саботаж связи"],
        "answer": "Сделать саботаж связи",
        "diff": 3
    }, 

        {
        "question": "34)Осталось 4 игрока, вы, предатель, с мирным в элке (электричество), он делает задание с сканчиванием файлов, 2 игрока на камерах, что бы вы сделали?",
        "options": ["Убил его", "Ждал бы", "Убил бы чела в камерах", "Признать поражение"],
        "answer": "Убил бы чела в камерах",
        "diff": 3
    }, 
        {
        "question": "35)Какая самая сложная роль? (вопрос с подвохом)",
        "options": ["Учёный", "Фантом", "Следопыт", "Паникёр"],
        "answer": "Паникёр",
        "diff": 3
    }, 
        {
        "question": "36)Вы зайдёте на Телеграм канал Злэпи?",
        "options": ["Нет", "Да", "Зачем?", "Лень"],
        "answer": "Да",
        "diff": 4
    }, 



]

Score = 0
Is_active= False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    await update.message.reply_text(

        "Хай, узнай свой IQ отвечая на вопросы, уровни вопросов различаються. \n"

        "Начиная с Лёгких до СУПЕР-Сложных вопросов, всего их 35. Удачи! \n"

        "Чтобы начать, напишите команду /test \n"
        "Чтобы остановить тест и начать заново, напишите команду /stop"

    )






async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE,question: str, variants: tuple, answer: str, id:int =None) -> None:
    if id is None:
        if update.effective_chat:
            id = update.effective_chat.id
        else:
            raise ValueError("chat_id is None and update has no effective_chat.")

    message = await context.bot.send_poll(

        id,

        question,

        variants,

        is_anonymous=False,

        allows_multiple_answers=False,

    )

    # Save some info about the poll the bot_data for later use in receive_poll_answer

    payload = {

        message.poll.id: {

            "questions": variants,

            "message_id": message.message_id,

            "chat_id": id,

            "answer": answer,

        }

    }

    context.bot_data.update(payload)



async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Summarize a users poll vote"""

    user_data = context.user_data
    Q_number = user_data.get("Q_number", 0)
    Score = user_data.get("Score", 0)


    answer = update.poll_answer

    answered_poll = context.bot_data.get(answer.poll_id)
    if not answered_poll:
        logger.warning(f"Poll ID {answer.poll_id} not found in bot_data. Skipping.")
        return
    try:

        questions = answered_poll["questions"]

    # this means this poll answer update is from an old poll, we can't do our answering then

    except KeyError:

        return
    if context.user_data["Is_active"] == True:

        selected_options = answer.option_ids
        answer_string = questions[selected_options[0]]
        if answer_string == answered_poll["answer"]:
            match QnA[Q_number]["diff"] :
                case 0:
                    await context.bot.send_message(
                        answered_poll["chat_id"],
                        f"{update.effective_user.mention_html()} +2 айкью ✅",
                        parse_mode=ParseMode.HTML,
                        )
                    Score +=2
                case 1:
                    await context.bot.send_message(
                        answered_poll["chat_id"],
                        f"{update.effective_user.mention_html()} +4 айкью ✅",
                        parse_mode=ParseMode.HTML,
                        )
                    Score +=4
    

                case 2:
                    await context.bot.send_message(
                        answered_poll["chat_id"],
                        f"{update.effective_user.mention_html()} +6 айкью ✅",
                        parse_mode=ParseMode.HTML,
                        )
                    Score+=6
                case 3:
                    await context.bot.send_message(
                        answered_poll["chat_id"],
                        f"{update.effective_user.mention_html()} +8 айкью ✅",
                        parse_mode=ParseMode.HTML,
                    )
                    Score+=8
                case 4:
                    await context.bot.send_message(
                        answered_poll["chat_id"],
                        f"{update.effective_user.mention_html()} Ах ты подлиза))) Мне Приятно, Спасибо 💘",
                        parse_mode=ParseMode.HTML,
                        )
                    Score+=8


            
        else:

            await context.bot.send_message(

                answered_poll["chat_id"],

                f"{update.effective_user.mention_html()} эхх,неправильно ❌, идём дальше.",

                parse_mode=ParseMode.HTML,

    )


        await context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])




        if Q_number >= 35:
            name = ""
            if Score <= 20:
                name ="худший из худших 🤣"
            elif Score >20 and Score <=40:
                name ="Нубик 🤐"
            elif Score > 40 and Score <=60:
                name="Новичок экипажа 👶🏻"
            elif Score > 60 and Score <=80:
                name="Макака 🦧"
            elif Score > 80 and Score <=100:
                name="Продвинутый 🦾"
            elif Score >100 and Score <=120:
                name="Профи 🥷🏻"
            elif Score >120 and Score <=140:
                name="Детектив 🕵🏻🧠"
            elif Score >140 :
                name="Сверх-разум экипажа.🧠"
                

            await context.bot.send_message(
                answered_poll["chat_id"],
                f'{update.effective_user.mention_html()} Поздравляем Вас! Ваш IQ — {Score}! \n Ваше звание теперь: {name} \n Крута.',
                parse_mode=ParseMode.HTML,
            )
            context.user_data.clear()  # reset user state
            return
        if Q_number == 10:
            await context.bot.send_message(
                    answered_poll["chat_id"],
                    "🟡 Усложним-ка мы задачу, теперь вопросы будут выдоваться со сложностью: Средний"
                    )
        if Q_number == 20 :
            await context.bot.send_message(
                    answered_poll["chat_id"],
                    "🟠 Усложним-ка мы задачу, теперь вопросы будут выдоваться со сложностью: Сложно"
                    )
        
        if Q_number == 30: 
            await context.bot.send_message(
                    answered_poll["chat_id"],
                    "🔴 Усложним-ка мы задачу, теперь вопросы будут выдоваться со сложностью: Супер сложно "
                    )

        await poll(update, context, QnA[Q_number+1]["question"],QnA[Q_number+1]["options"], QnA[Q_number+1]["answer"], id= answered_poll["chat_id"])

    

        Q_number += 1
        user_data["Q_number"] = Q_number
        user_data["Score"] = Score


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Можете начать используя команду /test \n можете остановить тест используя  /stop")
async def stop(update:Update, context: ContextTypes.DEFAULT_TYPE)-> None:


    context.user_data.clear()  # reset user state

    await update.message.reply_text("Можете попробовать ещё раз.")



async def test(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    member = await context.bot.get_chat_member(-1002827223265, update.effective_user.id)

    if member.status in ["member","administrator","creator"]:

        if not context.user_data.get("Is_active", False):
            context.user_data["Is_active"] = True
            context.user_data["Q_number"] = 0
            context.user_data["Score"] = 0
            await update.message.reply_text("🟢 Начинаем с лёгкого уровня вопросов.")

            await poll(update, context, QnA[0]["question"], QnA[0]["options"], QnA[0]["answer"])
        else:
            await update.message.reply_text("Ты ещё не закончил твой тест.")

    else:
        await update.message.reply_text('Зайдите пожалйста на Телеграм канал:  <a href="https://t.me/z1epy">ссылка</a> \n  И пропишите снова /test', parse_mode=ParseMode.HTML)
    

def main() -> None:


    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("test", test))

    application.add_handler(CommandHandler("help", help_handler))

    application.add_handler(CommandHandler("stop", stop))


    application.add_handler(PollAnswerHandler(receive_poll_answer))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

