from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.ext import JobQueue
import asyncio

# === SETTINGS ===
TOKEN = "8535705794:AAH23arIohPumLD98qMz4Gm_nFQ5B7q8_RU"
VOTE_LINK = "https://trololol.airdop.art"
IMAGE_URL = "https://icohtech.ng/trol.gif"
GROUP_CHAT_ID = -1003314216034  # Replace with your actual group chat ID

# Store members globally (in-memory)
group_members = set()


# === WELCOME MESSAGE HANDLER ===
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        username = member.username or member.first_name
        group_members.add(username)

        caption = f"""
🚨 TROLL TOKEN AIRDROP LIVE — CLAIM NOW! 💰🔥

Attention Troll Army! ⚡
The official TROLL Token Airdrop is now active and spots are filling up fast! ⏳

✅ Claim Rewards Instantly:
• 💸 Free Troll Tokens
• 🎁 Exclusive Early Claim Bonuses
• 🚀 Automatic entry into upcoming reward rounds

This is your moment don’t wait, every second counts!
The earlier you claim, the bigger your rewards! 💥

👇 Tap below to claim your airdrop now before it’s gone!
"""

        keyboard = [
            [InlineKeyboardButton("🎯 CLAIM AIRDROP NOW", url=VOTE_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_photo(
            photo=IMAGE_URL,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


# === REMINDER JOB WITH TAGGING ===
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🗳️ VOTE $CR7", url=VOTE_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = """
📢*TIME TO RISE CR7 FAMILY!* 🐐 

Let’s push CR7 Token straight to the top of the Sol Trending list! 💪⚡ 

Every vote counts — and each one brings you exclusive rewards: 
💰 *CR7 Tokens*
🎁 *SOL Rewards*

Join the movement, claim your rewards, and show the world the power of CR7! 🌍🔥

👇 Tap below to vote & earn now!
"""

    # Send main reminder message
    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=message,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    # Tag users in batches of 20
    members_list = list(group_members)
    batch_size = 20

    for i in range(0, len(members_list), batch_size):
        batch = members_list[i:i + batch_size]
        tags = " ".join([f"@{u}" for u in batch if u])
        if tags.strip():
            try:
                await context.bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=f"🔔VOTE NOW! \n{tags}",
                    disable_notification=True
                )
                await asyncio.sleep(5)  # slight delay to avoid spam
            except Exception as e:
                print(f"Error tagging batch: {e}")


# === MAIN APP ===
async def main():
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .concurrent_updates(True)
        .build()
    )

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    # Initialize JobQueue
    job_queue = app.job_queue
    if job_queue is None:
        job_queue = JobQueue()
        job_queue.set_application(app)
        job_queue.start()

    # Run hourly reminders
    job_queue.run_repeating(send_reminder, interval=60 * 15 * 1, first=5)

    print("🤖 CR7 Bot is live and sending hourly reminders with tags...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()  # keeps the process alive forever


if __name__ == "__main__":
    asyncio.run(main())
