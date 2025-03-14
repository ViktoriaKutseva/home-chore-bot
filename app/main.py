# import logging.config
# from config.logging_config import logging_config
from config.env_vars import get_env_vars
from clients.tg_bot_client import TgBotClient


if __name__ == "__main__":
    # logging.config.dictConfig(logging_config)
    # bot = TgBotClient(get_env_vars().TELEGRAM_BOT_TOKEN)
    bot = TgBotClient(get_env_vars().TELEGRAM_BOT_TOKEN, get_env_vars().DB_URL)
    bot.run()
