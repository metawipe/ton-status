from vkbottle import Bot
from config import VK_API_KEY
from handlers import register_handlers


def main():
    bot = Bot(token=VK_API_KEY)

    register_handlers(bot)

    print("Бот запущен...")

    bot.run_forever()


if __name__ == "__main__":
    main()
