import requests, json, aiogram, logging, time, asyncio

API_TOKEN = "6266863305:AAFKWnKGJzvX-Kbri2sWG6tpmTl1wKm3V4s"

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=API_TOKEN)
dp = aiogram.Dispatcher(bot)

mode = -1
working = True

@dp.message_handler(commands=['start','help']) 
async def HelpMessage(message: aiogram.types.Message):
    global mode, exchange_max, exchange_min
    await message.reply('''
    Привет!
Я бот, мониторящий изменение курса доллара за пределы Вами проставленных границ!
    ''')
    try:
        with open(f"{message.from_user.id}.txt") as file:
            global data
            data = json.load(file)
            exchange_min = data["min"]
            exchange_max = data["max"]
            await Monitoring(message)
    except json.decoder.JSONDecodeError:
        mode = 0
        await CreateBorders(message)
    except FileNotFoundError:
        f = open(f"{message.from_user.id}.txt",'w+')
        f.close()
        mode = 0
        await CreateBorders(message)

@dp.message_handler(lambda message: message.text in ["Изменить нижний предел","Изменить верхний предел"] or message.text.isdecimal() == True)
async def CreateBorders(message: aiogram.types.Message):
    global mode, exchange_min, exchange_max, working, emin
    working = False
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Главная")
    if message.text in ["Изменить нижний предел","Изменить верхний предел"]:
        mode = 0
        if message.text == "Изменить верхний предел": mode = 1
    if mode == 0:
        mode = (2 if message.text == "Изменить нижний предел" else 1)
        emin = (1 if message.text == "Изменить нижний предел" else 0)
        await message.answer("Выберите нижний предел:",reply_markup=aiogram.types.ReplyKeyboardRemove())
    
    elif mode == 1:
        mode = 2
        if message.text.isdecimal(): exchange_min = message.text
        await message.answer("Выберите верхний предел:",reply_markup=aiogram.types.ReplyKeyboardRemove())

    elif mode == 2:
        mode = -1
        if message.text.isdecimal():
            if emin == 1:
                exchange_min = message.text
                emin = 0
            else: exchange_max = message.text
        with open(f"{message.from_user.id}.txt","r+") as file:
            data = {
                "min": exchange_min,
                "max": exchange_max
            }
            json.dump(data,file)
            await message.answer("Новые пределы заданы!",reply_markup=keyboard)
            working = True

@dp.message_handler(lambda message: message.text == "Главная")
async def Monitoring(message: aiogram.types.Message):
    global working
    kboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    kboard.add(*["Изменить нижний предел","Изменить верхний предел"])
    while working:
        print('sas')
        baseUrl=r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
        mainUrl=baseUrl + f"&from_currency=USD&to_currency=RUB&apikey=TCV8VLPF0AYONHB3"
        result = requests.get(mainUrl).json()

        price = round(float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]),2)
        msg = f"1 USD = {price} RUB."
        with open(f"{message.from_user.id}.txt","r") as file:
            data = json.load(file)
        if float(price) < float(data["min"]):
            msg += f" Стоимость ниже границы ({data['min']})"
        elif float(price) > float(data["max"]):
            msg += f" Стоимость выше границы ({data['max']})"
        await message.answer(msg,reply_markup=kboard)
        await asyncio.sleep(30)