from telethon import TelegramClient
import csv
import logging
import os
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram API credentials
TG_API_ID = 29294185
TG_API_HASH = 'aab7ac1b04800f8cacd9bb582779349e'
PHONE = '+251954737771'
SESSION_NAME = 'telegram_scraper'

# Target channels
CHANNELS = [
    'https://t.me/lobelia4cosmetics',
    'https://t.me/DoctorsET',
    'https://t.me/CheMed123',
    'https://t.me/yetenaweg',
    'https://t.me/EAHCI'
]

def save_to_csv(data):
    file_exists = os.path.isfile('Medical_data.csv')
    with open('Medical_data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Channel Title", "Channel Username", "ID", "Message", "Date", "Mediapath"])
        writer.writerow(data)

async def scrape_telegram(search_term=""):  # Default to an empty string
    client = TelegramClient(SESSION_NAME, TG_API_ID, TG_API_HASH)
    await client.start(PHONE)

    # Prompt for the verification code directly in the notebook cell
    if not await client.is_user_authorized():
        print("Please enter the verification code sent to your phone.")
        code = input("Enter verification code: ").strip()  # Input the verification code manually
        await client.sign_in(PHONE, code)
    
    for channel in CHANNELS:
        try:
            async for message in client.iter_messages(channel):
                text = message.text or ''
                if search_term and search_term.lower() not in text.lower():
                    continue
                
                media_path = None
                # Download media if available
                if message.media:
                    os.makedirs("photos", exist_ok=True)
                    media_path = f'photos/{channel.split("/")[-1]}_{message.id}.jpg'
                    await message.download_media(file=media_path)
                
                # Save to CSV
                save_to_csv([channel, channel.split("/")[-1], message.id, text, message.date, media_path])
                
                logging.info(f'Scraped from {channel}: {text[:50]}')
        except Exception as e:
            logging.error(f'Error scraping {channel}: {e}')
    
    await client.disconnect()

if __name__ == "__main__":
    # Run scraping without search term input
    if not asyncio.get_event_loop().is_running():
        asyncio.run(scrape_telegram())
    else:
        asyncio.create_task(scrape_telegram())
