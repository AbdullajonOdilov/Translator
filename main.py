import logging
from aiogram import Bot, Dispatcher, executor, types
from oxfordlookup import getDefinitions
from googletrans import Translator
translator = Translator()

API_TOKEN = '5933870908:AAHtMD_w1Pdcpm1TjVWVDxFyHk4ZF7nLBCc'
logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def set_default_commands(db):
    await db.bot.set_my_commands(
        [
            types.BotCommand('start', "Launching the bot"),
            types.BotCommand('help', 'yordam'),
        ]
    )
async def on_startup(dispatcher):
    #Buyruqlarni qo'samiz
    await set_default_commands(dispatcher)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("hi👋, Welcome to translator bot")


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply("For suggestions and complaints @AbdullajonOdilov")

@dp.message_handler()
async def translate(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text


        lookup = getDefinitions(word_id)
        if lookup:
            sentence = (f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            await message.reply(translator.translate(sentence, dest='uz').text)
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])

        else:
            await message.reply("There is no word! Please, check it")





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
