import logging
import requests
from bs4 import BeautifulSoup as bs
import tweepy
import telegram
from telegram import Update,MessageEntity
from telegram.ext import Updater, CommandHandler, dispatcher, MessageHandler, Filters, CallbackQueryHandler
import emoji
import time

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)



def start(update,context) -> None:
    try:
        update.message.reply_text(
        "<b>Hi there {} {} ! \nI'm <a href=\"tg://user?id=1759506613\">Med-ish</a>."
        " I can make medium posts view free."
        "\n\nHit </b>/help<b> to find out more about how to use me.</b>".format(update.effective_user.first_name, (
            emoji.emojize(":wave:", use_aliases=True))), parse_mode='html',
        reply_to_message_id=update.message.message_id)
    except:
        update.message.reply_text(
            "<b>Hi there {} ! \nI'm <a href=\"tg://user?id=1759506613\">Med-ish</a>"
            "I can make medium posts view free."
            "\n\nHit </b>/help<b> to find out more about how to use me.</b>".format(
                emoji.emojize(":wave:", use_aliases=True)), parse_mode='html',
            reply_to_message_id=update.message.message_id)


def assist(update,context) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('*Hey*,\nHere is an short note on how to use me.\n\nProvide me any medium URL that you cannot view for free.\nI will make the whole post freely viewable without any change in it.'
                              '\n\n*NOTE : Instead using me to view medium posts there are other simple ways too.You shall clear your browser data and cookies else simply view the post in an incognito tab*'
                              '\n\nBut if you run a channel else share some medium post to your friend/subscribers, I might be efficient option'
                              "\n\n*Helpful commands:*"
                              "\n\t\t- /start: Starts me! You've probably already used this."
                              "\n\t\t- /help: Sends this message; I'll tell you more about myself!"
                              "\n\t\t- /about : About the bot."
                              "\n\t\t- /donate: Gives you info on how to support me and my creator."
                              "\n\nHere is an example medium post URL, copy the below URL and send it to me."
                              "\n`https://medium.com/swlh/telegram-bot-with-python-for-todoist-89d6cb13a04`" ,parse_mode=telegram.ParseMode.MARKDOWN)

def aboutTheBot(update, context):
    """Log Errors caused by Updates."""

    keyboard = [
        [
            telegram.InlineKeyboardButton((emoji.emojize(":loop:", use_aliases=True)) + "Channel",
                                          url="t.me/theostrich"),
            telegram.InlineKeyboardButton("👥Support Group", url="t.me/ostrichdiscussion"),
        ],
        [telegram.InlineKeyboardButton((emoji.emojize(":bookmark:", use_aliases=True)) + "Add Me In Group",
                                       url="https://t.me/medishBot?startgroup=new")],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    update.message.reply_text("<b>Hey! My name is Med-ish.</b>"
                              "\nI can handle links in different ways."
                              "\n\n<b>About Me :</b>"
                              "\n\n  - <b>Name</b>        : Med-ish"
                              "\n\n  - <b>Creator</b>      : @theostrich"
                              "\n\n  - <b>Language</b>  : Python 3"
                              "\n\n  - <b>Library</b>       : <a href=\"https://github.com/python-telegram-bot/python-telegram-bot/\">python-telegram-bot</a>"
                              "\n\n  - <b>Source Code</b>  : Currently unavailable"
                              "\n\nIf you enjoy using me and want to help me survive, do donate with the /donate command - my creator will be very grateful! Doesn't have to be much - every little helps! Thanks for reading :)",
                              parse_mode='html', reply_markup=reply_markup, disable_web_page_preview=True)



def tweed(update,context) -> None:
  url = update.message.text
  isMed = isMedium(url)
  print(isMed)
  if bool(isMed):
    auth = tweepy.OAuthHandler("", "")
    auth.set_access_token("", "")

    api = tweepy.API(auth)
    tweet = api.update_status(url)
    context.bot.sendMessage(chat_id=update.message.chat.id,text=f'Click the following URL to view the medium post for free {tweet.text}')
    time.sleep(1)
    api.destroy_status(tweet.id)
  else:
    context.bot.sendMessage(chat_id=update.message.chat.id,text='Provide a valid medium post URL')


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

def donate(update, context):
    keyboard = [
        [
            telegram.InlineKeyboardButton("Contribute",
                                          url="https://github.com/RabbitFored"),
            telegram.InlineKeyboardButton("Paypal Us",url="https://paypal.me/donateostrich"),
        ],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Thank you for your wish to contribute. I hope you enjoyed using our services. Make a small donation/contribute to let this project alive." , reply_markup=reply_markup)



def isMedium(url):
  try:
    re = requests.get(url)
    soup = bs(re.text,"html5lib")
    scDiv = soup.find_all("script")
    medsor =scDiv[10]['src']
    isMed = medsor.startswith("https://cdn-client.medium.com/")
    return isMed
  except:
    return False
def main() -> None:

    updater = Updater("")


    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", assist))
    dispatcher.add_handler(CommandHandler("about", aboutTheBot))
    dispatcher.add_handler(CommandHandler("donate", donate))
    dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(MessageHandler(Filters.text & (Filters.entity(MessageEntity.URL) |
                    Filters.entity(MessageEntity.TEXT_LINK)), tweed))

    updater.start_polling()

if __name__ == '__main__':
    main()
