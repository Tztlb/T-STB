import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time

# Your Telegram bot token
BOT_TOKEN = '7751935970:AAH8XtZSCrWMCOQF9LC0cYeH5sh4S9ulOC4'

bot = telebot.TeleBot(BOT_TOKEN)

def fetch_gold_prices(chat_id):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://milli.gold/")

        while True:
            try:
                # Locate elements for prices
                current_price_element = driver.find_element(By.CLASS_NAME, "font-bold.text-title1")

                # Extract text values
                current_price = current_price_element.text.strip()

                # Send the price to the user
                bot.send_message(chat_id, f"Current Price: {current_price}")
                bot.send_message(chat_id, f"➖" * 10)

                # Wait for 10 seconds
                time.sleep(10)
                driver.refresh()
            except Exception as e:
                bot.send_message(chat_id, f"Error while fetching price: {e}")
                break

    finally:
        driver.quit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /price to start receiving gold prices.")

@bot.message_handler(commands=['price'])
def send_price(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Fetching gold prices. You will receive updates every 10 seconds.")

    # Start a new thread to run the price-fetching loop
    threading.Thread(target=fetch_gold_prices, args=(chat_id,), daemon=True).start()

# Polling to keep the bot running
bot.polling(non_stop=True)