import requests, json, aiogram, logging

API_TOKEN = "6084681905:AAGf5WJsfuCDTfWacP-iwoY4_OTIf9EGyCs"

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=API_TOKEN)
dp = aiogram.Dispatcher(bot)

mode = 0
FromCurrency = ""
ToCurrency = ""

templates = []
buttons = ["USD","EUR","CNY","RUB"]
@dp.message_handler(lambda message: (message.text == 'Новый шаблон') or (message.text in buttons))
async def CreateTemplate(message = aiogram.types.Message): #    Создание шаблона
    global mode,FromCurrency,ToCurrency
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if mode == 0:
        keyboard.add(*buttons)
        mode = 1

        await message.answer("Выберите рассматриваемую валюту:",reply_markup=keyboard)
    elif mode == 1:
        FromCurrency = message.text
        keyboard.add(*[currency for currency in buttons if currency!=message.text])
        mode = 2
        
        await message.answer("Выберите валюту, в которую хотите перевести:",reply_markup=keyboard)
    else:
        keyboard.add("Главная")
        ToCurrency = message.text
        with open(f"{message.from_user.username}.txt",'r+') as file:
            mode = 0
            newTemplate = f"{FromCurrency} - {ToCurrency}\n"
            if newTemplate in file.readlines():
                keyboard.add("Новый шаблон")
                await message.answer("Этот шаблон у вас существует!",reply_markup=keyboard)
            else:
                file.writelines(newTemplate)
                await message.answer("Шаблон добавлен!",reply_markup=keyboard)

@dp.message_handler(lambda message:message.text == "Главная")
async def MainMenu(message = aiogram.types.Message): #  Главное меню
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    with open(f"{message.from_user.username}.txt",'r+') as file:
        templates=[]
        rawtemplates = file.readlines()
        for template in rawtemplates:templates.append(template.split("\n")[0])
    keyboard.add(*templates)
    keyboard.add("Новый шаблон")

    await message.answer("Выберите шаблон или создайте новый:",reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in templates)
async def CurrentExchangeRate(message = aiogram.types.Message): #   Вывод курса валют
    from_currency,to_currency=map(str,message.text.split("\n")[0].split(" - "))
    baseUrl=r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
    mainUrl=baseUrl + f"&from_currency={from_currency}&to_currency={to_currency}&apikey=TCV8VLPF0AYONHB3"
    result = requests.get(mainUrl).json()

    price = round(float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]),2)

    await message.reply(f"1 {from_currency} = {price} {to_currency}")

@dp.message_handler(commands=['start','help'])
async def send_welcome(message: aiogram.types.Message): #   Информация о боте
    global buttons
    await message.answer("""
    Привет!
Я бот, информирующий о любых курсах валют!
    """)
    try:
        file = open(f"{message.from_user.username}.txt")
        if file.readlines() == []: await CreateTemplate(message)
        else: await MainMenu(message)
        file.close()
    except FileNotFoundError: await CreateTemplate(message)



if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)