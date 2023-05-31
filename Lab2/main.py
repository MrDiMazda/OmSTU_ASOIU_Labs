import Lab2, aiogram

if __name__ == "__main__":
    aiogram.executor.start_polling(Lab2.dp,skip_updates=True)