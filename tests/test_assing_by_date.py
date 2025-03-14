import pytest
from datetime import date
from unittest.mock import patch
from app.logic.assing_by_date import ChoreDistributionService
from app.clients.db_client import Chore, Person, Frequency, Complexity

@pytest.fixture
def chore_distribution_service():
    return ChoreDistributionService()


@pytest.mark.parametrize('day_of_year, frequency, expected', [
    [1, Frequency.DAILY, 1],
    [1, Frequency.WEEKLY, 0],
    [4, Frequency.WEEKLY, 1],
])
def test_get_chores_due_today(chore_distribution_service, day_of_year, frequency, expected):
    today_date = date(2025, 1, day_of_year)

    chore1 = Chore(name='chore1', frequency=frequency, complexity=Complexity.EASY)
    all_chores = [chore1]

    with patch("app.logic.assing_by_date.datetime.date") as mock_date:
        mock_date.today.return_value = today_date
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)
        result = chore_distribution_service.get_chores_due_today(all_chores)
    
    assert len(result) == expected

def test_assign_tasks(chore_distribution_service):
    person1 = Person(tg_user_id='user1')
    person2 = Person(tg_user_id='user2')
    persons = [person1, person2]

    chore1 = Chore(name='chore1', complexity=Complexity.EASY, frequency=Frequency.DAILY)
    chore2 = Chore(name='chore2', complexity=Complexity.HARD, frequency=Frequency.WEEKLY)
    chores = [chore1, chore2]

    result = chore_distribution_service.assign_tasks(chores, persons)
    
    assert len(result) == 2
    assert len(result[0]['tasks']) + len(result[1]['tasks']) == 2
    assert any(task['name'] == 'chore1' for task in result[0]['tasks'] + result[1]['tasks'])
    assert any(task['name'] == 'chore2' for task in result[0]['tasks'] + result[1]['tasks'])