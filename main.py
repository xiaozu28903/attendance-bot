from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = "8955108031:AAH43TAZM_GX6mvfSC38dKZL8gHUsuAYil8"

SHEET_ID = "13nJZDY20mUO5H0XSGaVIeonrbjeldPV1QjbS6u7RjxM"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "long-nation-498022-q3-827dc3d2824b.json",
    scope
)

client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

keyboard = [
    ["✅ Check In"],
    ["🍜 Eating"],
    ["☕ Break Time"],
    ["🚬 Smoke Break"],
    ["🏢 Back To Work"],
    ["❌ Check Out"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Attendance Bot Ready",
        reply_markup=markup
    )

async def attendance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = update.effective_user.username

    if username:
        username = "@" + username
    else:
        username = update.effective_user.first_name

    action = update.message.text
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([username, action, now])

    await update.message.reply_text(
        f"{action}\n{now}"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, attendance))

print("Bot Running...")
app.run_polling()
