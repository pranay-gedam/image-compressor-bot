High-Precision Image Compressor Bot
A powerful yet simple Telegram bot that compresses your images to a specific target file size with the highest possible quality. Perfect for preparing images for web uploads, email attachments, or online forms with strict size limits.

🌟 What Does It Do?
This bot solves a common problem: needing an image to be just under a certain file size (e.g., "upload a photo under 250 KB").

Instead of guessing with a "quality" slider in a photo editor, this bot uses a smart algorithm (a binary search) to find the absolute best quality setting that gets the image as close as possible to your target size without going over.

Key Features
🎯 Target Size Compression: Specify the exact maximum size you want in kilobytes (KB).

✨ Maximum Quality: Automatically finds the highest quality setting to stay within your size limit.

📁 Handles Original Files: Works exclusively with uncompressed images sent as a "File" or "Document" to ensure precision.

✔️ Multi-Format Support: Can process JPEG, PNG, and WEBP files.

🤖 Easy to Use: A simple, conversational interface with helpful commands.

📊 Usage Analytics: A /stats command to track how many images have been processed and how much data has been saved.

🚀 How to Use the Bot (Step-by-Step)
To get the correct result, it is very important to send your image as a File, not as a Photo. This sends the original, untouched image to the bot.

Step 1: Start a Chat with the Bot

Find the bot on Telegram and press the "Start" button or type /start. You can also type /help at any time for instructions.

Step 2: Attach Your Image as a File

Tap the paperclip icon (📎) in the message bar.

From the menu that appears, select the "File" option.

Browse your phone's storage and select the image you want to compress.

Step 3: Add the Target Size in the Caption

Before sending, tap on the "Add a caption..." field.

Type the target size you want in kilobytes, for example, 250.

Press Send.

Step 4: Receive Your Compressed Image

The bot will process your image and send it back to you, showing the final compressed size in the caption. That's it!

🛠️ For Developers: How to Run This Bot Yourself
You can host and run your own instance of this bot.

Prerequisites
Python 3.8+

A Telegram Bot Token from @BotFather

1. Clone the Repository
git clone [https://github.com/pranay-gedam/image-compressor-bot.git]
cd image-compressor-bot

2. Install Dependencies
The required Python libraries are python-telegram-bot and Pillow. You can create a requirements.txt file with the following content:

python-telegram-bot[ext]
Pillow

Then install them using pip:

pip install -r requirements.txt

3. Configure Your Bot Token
Open the compress_bot.py file and replace the placeholder token with your own.

# Find this line in the code
TELEGRAM_BOT_TOKEN = 'YOUR_HTTP_API_TOKEN' 

# Replace it with your actual token
TELEGRAM_BOT_TOKEN = '1234567890:ABCdEfgHiJKLmnoPqrs-tuvWxyz123456'

4. Run the Bot
Execute the main script from your terminal.

python compress_bot.py

Your bot is now running locally! As long as the script is active, it will poll Telegram for new messages. For a 24/7 bot, you should deploy this script to a hosting service like Railway, Heroku, or PythonAnywhere.

🔮 Future Improvements (To-Do)
[ ] Allow users to specify output format (e.g., PNG, WEBP).
[ ] Allow users to specify dimensions (width/height) in addition to file size.
[ ] Implement persistent analytics using a database like SQLite.
[ ] Add language localization for user messages.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.