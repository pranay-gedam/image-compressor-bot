import logging
import io
from PIL import Image
from telegram import Update, File
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# --- Configuration ---
# Replace 'YOUR_HTTP_API_TOKEN' with the token you got from BotFather
TELEGRAM_BOT_TOKEN = "8297750107:AAFFkbqTQOhQntMWLPKHPDjauBaSeWB0FMY"

# --- In-Memory Analytics ---
bot_stats = {
    "images_processed": 0,
    "bytes_saved": 0
}

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Bot Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "👋 **Welcome to the Image Compressor Bot!**\n\n"
        "To compress an image, send it as a **File/Document** with a caption specifying the target size in KB (e.g., `350`).\n\n"
        "Type /help for more detailed instructions.",
        parse_mode=ParseMode.MARKDOWN
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a detailed help message."""
    help_text = (
        "**How to Use This Bot**\n\n"
        "1️⃣ **Attach an Image as a File:**\n"
        "   - Tap the paperclip icon (`📎`) and select **'File'**.\n"
        "   - Select the image you want to compress.\n"
        "   - **Important:** Do not send as a 'Photo'.\n\n"
        "2️⃣ **Set Target Size:**\n"
        "   - In the **caption** field, type your desired maximum size in kilobytes (e.g., `250`).\n\n"
        "3️⃣ **Receive Your Compressed File:**\n"
        "   - The bot will process your image and send it back.\n\n"
        "**Supported Formats:**\n"
        "I can read `JPEG`, `PNG`, and `WEBP` files. All compressed images will be returned as `JPEG`.\n\n"
        "**Available Commands:**\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/stats - Show usage statistics"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays bot usage statistics."""
    images_processed = bot_stats["images_processed"]
    bytes_saved_mb = bot_stats["bytes_saved"] / (1024 * 1024)
    
    stats_text = (
        "📊 **Bot Usage Statistics**\n\n"
        f"🖼️ **Images Processed:** {images_processed}\n"
        f"💾 **Total Data Saved:** {bytes_saved_mb:.2f} MB"
    )
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

# --- Core Logic ---

def compress_image_to_target_size(image_bytes: bytes, target_kb: int) -> io.BytesIO | None:
    """Compresses an image to get as close as possible to the target file size."""
    target_bytes = target_kb * 1024
    try:
        img = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        logger.error(f"Failed to open image: {e}")
        return None

    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    min_quality, max_quality = 1, 95
    best_image_data = None

    while min_quality <= max_quality:
        quality = (min_quality + max_quality) // 2
        if quality == 0: break
            
        buffer = io.BytesIO()
        try:
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
        except Exception as e:
            logger.error(f"Failed to save with quality {quality}: {e}")
            max_quality = quality - 1
            continue

        if buffer.tell() <= target_bytes:
            best_image_data = buffer.getvalue()
            min_quality = quality + 1
        else:
            max_quality = quality - 1

    if best_image_data:
        return io.BytesIO(best_image_data)
    
    return None

# --- Message Handlers ---

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles an image sent as a document/file."""
    if not update.message.caption:
        await update.message.reply_text("⚠️ Please include a caption with the target size (e.g., `250`).")
        return
        
    try:
        target_kb = int(update.message.caption)
        if target_kb <= 0: raise ValueError
    except (ValueError, TypeError):
        await update.message.reply_text("❌ Invalid caption. Please use a positive number for the target size in KB.")
        return
    
    await update.message.reply_text(f"⚙️ Processing your image to be under {target_kb} KB. Please wait...")

    try:
        file_object: File = await update.message.document.get_file()
        image_bytes_io = io.BytesIO()
        await file_object.download_to_memory(image_bytes_io)
        image_bytes = image_bytes_io.getvalue()

        original_size_kb = len(image_bytes) / 1024
        if original_size_kb <= target_kb:
            await update.message.reply_text(f"✅ No compression needed! Your image is already {original_size_kb:.2f} KB.")
            return

        compressed_buffer = compress_image_to_target_size(image_bytes, target_kb)
        if compressed_buffer:
            final_size_kb = len(compressed_buffer.getvalue()) / 1024
            bot_stats["images_processed"] += 1
            bot_stats["bytes_saved"] += (original_size_kb - final_size_kb) * 1024
            
            await update.message.reply_document(
                document=compressed_buffer,
                filename=f'compressed_near_{target_kb}kb.jpg',
                caption=f"✅ Compression complete!\nFinal size: **{final_size_kb:.2f} KB**",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text("😔 Sorry, I couldn't compress this image to the desired size.")

    except Exception as e:
        logger.error(f"Error processing document: {e}")
        await update.message.reply_text("😔 An unexpected error occurred. Please try again.")

async def handle_photo_rejection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rejects images sent as 'Photos' and instructs the user."""
    await update.message.reply_text(
        "❗️ **Please send your image as a File/Document, not as a Photo.**\n\n"
        "To compress your image, tap the paperclip (`📎`) and choose **'File'**.",
        parse_mode=ParseMode.MARKDOWN
    )

def main() -> None:
    """Start the bot."""
    logger.info("Starting bot...")
    
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Register message handlers
    # This handler REJECTS photos and provides instructions.
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo_rejection))
    # This handler PROCESSES images sent correctly as documents.
    application.add_handler(MessageHandler(filters.Document.IMAGE, handle_document))

    logger.info("Bot is polling for updates...")
    application.run_polling()
    logger.info("Bot has stopped.")

if __name__ == '__main__':
    main()
