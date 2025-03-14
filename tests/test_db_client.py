import logging
import pytest
from app.clients.db_client import DBClient, Person, Chore, Frequency, Complexity

log = logging.getLogger(__name__)


@pytest.fixture
def db_client():
    db_url = 'sqlite:///:memory:'
    return DBClient(db_url=db_url)


def test_add_person(db_client):
    tg_user_id = '123'
    tg_group_id = 'group1'

    db_client.add_person(Person(tg_user_id=tg_user_id, tg_group_id=tg_group_id))
    result = db_client.get_person_by_tg_user_id(tg_user_id)
    log.info(f'{result.tg_group_id} == {tg_group_id}')
    assert result.tg_group_id == tg_group_id
    assert result.tg_user_id == tg_user_id


def test_get_persons_by_tg_group_id(db_client):
    tg_group_id = 'group1'
    tg_user_id1 = '123'
    tg_user_id2 = '456'

    person1 = Person(tg_user_id=tg_user_id1, tg_group_id=tg_group_id)
    person2 = Person(tg_user_id=tg_user_id2, tg_group_id=tg_group_id)
    db_client.add_person(person1)
    db_client.add_person(person2)
    result = db_client.get_persons_by_tg_group_id(tg_group_id)
    assert len(result) == 2
    assert result[0].tg_user_id == tg_user_id1
    assert result[1].tg_user_id == tg_user_id2


def test_get_person_by_user_and_group(db_client):
    tg_user_id = '123'
    tg_group_id = 'group1'
    person = Person(tg_user_id=tg_user_id, tg_group_id=tg_group_id)
    db_client.add_person(person)
    
    result = db_client.get_person_by_user_and_group(tg_user_id, tg_group_id)
    assert result is not None
    assert result.tg_user_id == tg_user_id
    assert result.tg_group_id == tg_group_id


def test_delete_person_by_tg_user_id(db_client):
    tg_user_id = '123'
    tg_group_id = 'group1'

    db_client.add_person(Person(tg_user_id=tg_user_id, tg_group_id=tg_group_id))
    db_client.delete_person_by_tg_user_id(tg_user_id)
    result = db_client.get_person_by_tg_user_id(tg_user_id)
    assert result is None


def test_add_chore(db_client):
    tg_group_id = 'group1'
    name = 'chore1'
    complexity = Complexity.EASY
    frequency = Frequency.DAILY

    chore = Chore(tg_group_id=tg_group_id, name=name, complexity=complexity, frequency=frequency)
    db_client.add_chore(chore)
    result = db_client.get_chores_by_tg_group_id(tg_group_id)
    assert len(result) == 1
    assert result[0].name == name
    assert result[0].complexity == complexity
    assert result[0].frequency == frequency


def test_get_chore_by_name_and_tg_group_id(db_client):
    tg_group_id = 'group1'
    name = 'chore1'
    complexity = Complexity.EASY
    frequency = Frequency.DAILY
    chore = Chore(tg_group_id=tg_group_id, name=name, complexity=complexity, frequency=frequency)
    db_client.add_chore(chore)
    
    result = db_client.get_chore_by_name_and_tg_group_id(name, tg_group_id)
    assert result is not None
    assert result.name == name
    assert result.tg_group_id == tg_group_id
    assert result.complexity == complexity
    assert result.frequency == frequency


def test_update_chore_by_id(db_client):
    tg_group_id = 'group1'
    name = 'chore1'
    complexity = Complexity.EASY
    frequency = Frequency.DAILY

    new_name = 'chore2'
    new_complexity = Complexity.HARD
    new_frequency = Frequency.WEEKLY

    chore = Chore(tg_group_id=tg_group_id, name=name, complexity=complexity, frequency=frequency)
    db_client.add_chore(chore)
    result = db_client.get_chores_by_tg_group_id(tg_group_id)
    chore_id = result[0].id
    db_client.update_chore_by_id(chore_id, name=new_name, complexity=new_complexity, frequency=new_frequency)
    result = db_client.get_chores_by_tg_group_id(tg_group_id)
    assert len(result) == 1
    assert result[0].name == new_name
    assert result[0].complexity == new_complexity
    assert result[0].frequency == new_frequency


def test_delete_chore_by_id(db_client):
    tg_group_id = 'group1'
    name = 'chore1'
    complexity = Complexity.EASY
    frequency = Frequency.DAILY

    chore = Chore(tg_group_id=tg_group_id, name=name, complexity=complexity, frequency=frequency)
    db_client.add_chore(chore)
    result = db_client.get_chores_by_tg_group_id(tg_group_id)
    chore_id = result[0].id
    db_client.delete_chore_by_id(chore_id)
    result = db_client.get_chores_by_tg_group_id(tg_group_id)
    assert len(result) == 0
