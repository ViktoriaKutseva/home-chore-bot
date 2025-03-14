# import pytest
# from unittest.mock import AsyncMock, MagicMock
# from app.enums.complexity import Complexity
# from app.enums.frequency import Frequency
# from app.logic.chore_distribution import split_list_to_groups
# from telegram import Update, Message
# from telegram.ext import ContextTypes
# from app.clients.db_client import Chore, Person, DBClient
# from app.clients.tg_bot_client import TgBotClient  # Replace with the actual file name containing your bot

# @pytest.fixture
# def mock_db_client():
#     """Mock DBClient instance."""
#     mock = MagicMock()
#     mock.get_persons_by_tg_group_id.return_value = []
#     mock.get_chores_by_tg_group_id.return_value = []
#     return mock

# @pytest.fixture
# def tg_bot(mock_db_client):
#     """Initialize the bot with a mocked DBClient."""
#     bot = TgBotClient(token="test-token")
#     bot.db_client = mock_db_client
#     return bot

# @pytest.fixture
# def mock_update():
#     """Mock the Telegram Update object."""
#     update = AsyncMock(spec=Update)
#     update.message = AsyncMock(spec=Message)
#     update.message.chat_id = 12345
#     update.message.reply_text = AsyncMock()
#     return update

# @pytest.fixture
# def mock_context():
#     """Mock the Telegram Context object."""
#     context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
#     context.args = []
#     return context


# # Test add_chore_command
# @pytest.mark.asyncio
# async def test_add_chore_command_success(tg_bot, mock_update, mock_context):
#     mock_context.args = ["Dishes", "EASY", "DAILY"]
#     tg_bot.db_client.add_chore = MagicMock()

#     await tg_bot.add_chore_command(mock_update, mock_context)

#     tg_bot.db_client.add_chore.assert_called_once_with(
#         tg_group_id="12345",
#         name="Dishes",
#         complexity=Complexity.EASY,
#         frequency=Frequency.DAILY,
#     )
#     mock_update.message.reply_text.assert_called_once_with("Chore 'Dishes' added to group 12345.")



# @pytest.mark.asyncio
# async def test_add_chore_command_invalid_args(tg_bot, mock_update, mock_context):
#     mock_context.args = ["Dishes", "UNKNOWN", "DAILY"]

#     await tg_bot.add_chore_command(mock_update, mock_context)

#     mock_update.message.reply_text.assert_called_once_with(
#         "Usage: /add_chore <name> <complexity> <frequency>"
#     )


# # Test add_person_command
# @pytest.mark.asyncio
# async def test_add_person_command_success(tg_bot, mock_update, mock_context):
#     mock_context.args = ["111"]

#     await tg_bot.add_person_command(mock_update, mock_context)

#     tg_bot.db_client.add_person.assert_called_once_with(
#         tg_user_id="111",
#         tg_group_id="12345",
#     )
#     mock_update.message.reply_text.assert_called_once_with(
#         "Person with TG user ID 111 added to group 12345."
#     )


# @pytest.mark.asyncio
# async def test_add_person_command_invalid_args(tg_bot, mock_update, mock_context):
#     mock_context.args = []

#     await tg_bot.add_person_command(mock_update, mock_context)

#     mock_update.message.reply_text.assert_called_once_with(
#         "Usage: /add_person <tg_user_id>"
#     )


# # Test assign_tasks_command
# @pytest.mark.asyncio
# async def test_assign_tasks_command_success(tg_bot, mock_update, mock_context):
#     tg_bot.db_client.get_persons_by_tg_group_id.return_value = [
#         Person(tg_user_id="111", tg_group_id="12345"),
#         Person(tg_user_id="222", tg_group_id="12345"),
#     ]
#     tg_bot.db_client.get_chores_by_tg_group_id.return_value = [
#         Chore(name="Dishes", complexity=Complexity.EASY, frequency=Frequency.DAILY),
#         Chore(name="Vacuum", complexity=Complexity.MEDIUM, frequency=Frequency.WEEKLY),
#     ]
#     tg_bot.assign_tasks_command = AsyncMock(return_value=None)

#     await tg_bot.assign_tasks_command(mock_update, mock_context)

#     mock_update.message.reply_text.assert_called_once_with("Task Assignments:\n👤 111: Dishes\n👤 222: Vacuum\n")



# @pytest.mark.asyncio
# async def test_assign_tasks_command_success(tg_bot, mock_update, mock_context):
#     tg_bot.db_client.get_persons_by_tg_group_id.return_value = [
#         Person(tg_user_id="111", tg_group_id="12345"),
#         Person(tg_user_id="222", tg_group_id="12345"),
#     ]
#     tg_bot.db_client.get_chores_by_tg_group_id.return_value = [
#         Chore(name="Dishes", complexity=Complexity.EASY, frequency=Frequency.DAILY),
#         Chore(name="Vacuum", complexity=Complexity.MEDIUM, frequency=Frequency.WEEKLY),
#     ]
#     split_list_to_groups.return_value = [
#         {"person": tg_bot.db_client.get_persons_by_tg_group_id()[0], "tasks": [{"name": "Dishes"}]},
#         {"person": tg_bot.db_client.get_persons_by_tg_group_id()[1], "tasks": [{"name": "Vacuum"}]},
#     ]


#     await tg_bot.assign_tasks_command(mock_update, mock_context)

#     mock_update.message.reply_text.assert_called_once_with(
#         "Task Assignments:\n👤 111: Dishes\n👤 222: Vacuum\n"
#     )
