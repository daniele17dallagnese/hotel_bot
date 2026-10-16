import telebot
from playwright.sync_api import sync_playwright
from datetime import date, timedelta

# TELEGRAM
TOKEN = "8806333128:AAFjcPD45SKExETlv58bI_Mc8gkmZUlBlY8"
CHAT_ID = 829659118
CHAT_ID = 6611621429

bot = telebot.TeleBot(TOKEN)

# DESTINAZIONE
DESTINAZIONE = "Lonate Pozzolo"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for giorno in range(7):

        checkin = date.today() + timedelta(days=giorno)
        checkout = checkin + timedelta(days=1)

        url = (
            f"https://www.booking.com/searchresults.it.html"
            f"?ss={DESTINAZIONE}"
            f"&checkin={checkin.strftime('%Y-%m-%d')}"
            f"&checkout={checkout.strftime('%Y-%m-%d')}"
        )

        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(5000)

        try:

            hotel = page.locator(
                '[data-testid="title"]'
            ).all_inner_texts()

            prezzi = page.locator(
                '[data-testid="price-and-discounted-price"]'
            ).all_inner_texts()

            totale = min(len(hotel), len(prezzi))

            messaggio = (
                f"📅 {checkin.strftime('%d/%m/%Y')} - "
                f"{checkout.strftime('%d/%m/%Y')}\n\n"
            )

            for i in range(min(totale, 10)):
                messaggio += (
                    f"{i+1}. {hotel[i]}\n"
                    f"💰 {prezzi[i]}\n\n"
                )

            print(messaggio)

            bot.send_message(
                CHAT_ID,
                messaggio
            )

        except Exception as e:
            print("Errore:", e)

    browser.close()

print("Messaggi inviati su Telegram")

import os

os.system("shutdown /s /t 60")