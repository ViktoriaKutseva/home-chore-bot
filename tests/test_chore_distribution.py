import pytest
from unittest.mock import MagicMock, patch # <-- Add patch
import random
import datetime # <-- Add datetime
from datetime import date as OriginalDate # <-- Import original date class

# Assuming these paths are correct relative to the test execution context (e.g., workspace root)
from app.logic.assing_by_date import ChoreDistributionService
from app.enums.complexity import Complexity
from app.enums.frequency import Frequency

# Simple mock classes/objects to mimic DB models for the purpose of this test
class MockPerson:
    def __init__(self, id, tg_user_id):
        self.id = id
        self.tg_user_id = tg_user_id

class MockChore:
    def __init__(self, id, name, complexity, frequency):
        self.id = id
        self.name = name
        self.complexity = complexity
        self.frequency = frequency

@pytest.fixture
def chore_service():
    """Provides an instance of ChoreDistributionService."""
    return ChoreDistributionService()

@pytest.fixture
def two_people():
    """Provides a list of two mock people."""
    return [
        MockPerson(id=1, tg_user_id=123),
        MockPerson(id=2, tg_user_id=456)
    ]

@pytest.fixture
def sample_chores():
    """Provides a list of mock chores with varying complexities."""
    return [
        MockChore(id=10, name="Hardest Chore", complexity=Complexity.HARDEST, frequency=Frequency.DAILY),
        MockChore(id=11, name="Hard Chore", complexity=Complexity.HARD, frequency=Frequency.WEEKLY),
        MockChore(id=12, name="Medium Chore", complexity=Complexity.MEDIUM, frequency=Frequency.DAILY),
        MockChore(id=13, name="Easy Chore", complexity=Complexity.EASY, frequency=Frequency.WEEKLY),
    ]

# New fixture for frequency testing
@pytest.fixture
def frequency_chores():
    """Provides a list of mock chores with varying frequencies."""
    return [
        MockChore(id=20, name="Daily Chore", complexity=Complexity.EASY, frequency=Frequency.DAILY),
        MockChore(id=21, name="3Day Chore", complexity=Complexity.MEDIUM, frequency=Frequency.EVERY_3_DAYS),
        MockChore(id=22, name="Weekly Chore", complexity=Complexity.HARD, frequency=Frequency.WEEKLY),
    ]

def test_distribution_two_people_no_history(chore_service, two_people, sample_chores):
    """
    Tests chore distribution between two people with no assignment history.
    Expects relatively balanced distribution based on complexity.
    """
    # We pass an empty list for history and a mock session (though it won't be used for history fetching)
    # because assign_tasks expects db_session for the history call if history is None.
    mock_session = MagicMock()
    
    # Print input data for better visibility
    print("\n=== DISTRIBUTION TEST INPUT ===")
    print("People:")
    for i, person in enumerate(two_people):
        print(f"  Person {person.id} (TG ID: {person.tg_user_id})")
    
    print("\nChores to distribute:")
    for chore in sample_chores:
        print(f"  {chore.name} - Complexity: {chore.complexity.name} ({chore.complexity.value}), Frequency: {chore.frequency.name}")
    print("=============================\n")
    
    random.seed(0) # <-- Seed the random number generator for predictability
    
    # Print a message to show we're starting the distribution process
    print("\n=== STARTING DISTRIBUTION PROCESS ===")
    print("Note: Random seed is set to 0 for consistent results")
    
    # Track the original order of chores before shuffling (they're sorted by complexity in the algorithm)
    print("\nChores will be sorted by complexity (highest to lowest):")
    sorted_chores = sorted(sample_chores, key=lambda c: c.complexity.value, reverse=True)
    for chore in sorted_chores:
        print(f"  {chore.name} - Complexity: {chore.complexity.name} ({chore.complexity.value})")
    
    # Now perform the actual distribution
    assignments = chore_service.assign_tasks(sample_chores, two_people, history=[], db_session=mock_session)

    assert len(assignments) == 2  # Should have assignments for both people

    person1_tasks = next(a for a in assignments if a['person'].id == 1)['tasks']
    person2_tasks = next(a for a in assignments if a['person'].id == 2)['tasks']

    # Print the final assignments with all details
    print("\n=== FINAL CHORE ASSIGNMENTS ===")
    print("Person 1 Tasks:")
    total_complexity_p1 = 0
    for task in person1_tasks:
        print(f"  - {task['name']} (Complexity: {task['complexity']})")
        total_complexity_p1 += task['complexity']
    print(f"  Total tasks: {len(person1_tasks)}, Total complexity: {total_complexity_p1}")
    
    print("\nPerson 2 Tasks:")
    total_complexity_p2 = 0
    for task in person2_tasks:
        print(f"  - {task['name']} (Complexity: {task['complexity']})")
        total_complexity_p2 += task['complexity']
    print(f"  Total tasks: {len(person2_tasks)}, Total complexity: {total_complexity_p2}")
    
    print("\nDistribution Fairness:")
    print(f"  Task count balance: {len(person1_tasks)} vs {len(person2_tasks)}")
    print(f"  Complexity balance: {total_complexity_p1} vs {total_complexity_p2}")
    print("=============================\n")

    # Validate task counts
    assert len(person1_tasks) == 2
    assert len(person2_tasks) == 2

    # Validate task names based on expected distribution (may vary based on shuffle, but complexities should balance)
    person1_task_names = {t['name'] for t in person1_tasks}
    person2_task_names = {t['name'] for t in person2_tasks}

    # Based on the logic: Hardest(5)->P1, Hard(4)->P2, Medium(3)->P2, Easy(2)->P1
    expected_p1_tasks = {"Hardest Chore", "Easy Chore"}
    expected_p2_tasks = {"Hard Chore", "Medium Chore"}

    assert person1_task_names == expected_p1_tasks
    assert person2_task_names == expected_p2_tasks

    # Optional: Validate total complexity (should be equal in this case)
    person1_complexity = sum(t['complexity'] for t in person1_tasks)
    person2_complexity = sum(t['complexity'] for t in person2_tasks)
    assert person1_complexity == 7 # 5 + 2
    assert person2_complexity == 7 # 4 + 3

# New test for get_chores_due_today
@patch('app.logic.assing_by_date.datetime.date') # Patch only datetime.date
def test_get_chores_due_today(mock_date, chore_service, frequency_chores): # Rename mock_datetime to mock_date
    """Tests that get_chores_due_today returns correct chores based on date and frequency."""
    print("\n=== CHORE FREQUENCY TEST ===")
    print("Available chores:")
    for chore in frequency_chores:
        print(f"  {chore.name} - Frequency: {chore.frequency.name} ({chore.frequency.value} days)")

    # Configure the mock:
    # - Calls to .today() will return our specific date.
    # - Calls to the mock itself (like datetime.date(y, m, d)) will delegate to the OriginalDate class.
    mock_date.side_effect = lambda *args, **kw: OriginalDate(*args, **kw)

    # Test Case 1: Date where Daily and 3-Day chores should be due
    test_date = OriginalDate(2024, 1, 15)
    print(f"\nTest case 1 - Date: {test_date}")
    print(f"  Jan 1, 2024 was a Monday (weekday 0)")
    print(f"  Offset calculation: (5-0)%7 = 5 days")
    print(f"  Adjusted first day: Jan 6, 2024")
    print(f"  Days since adjusted start: 9 days")
    print(f"  Expected due chores: Daily (9%1=0), 3Day (9%3=0), Weekly (9%7≠0)")
    
    mock_date.today.return_value = test_date
    due_chores_1 = chore_service.get_chores_due_today(frequency_chores)
    due_names_1 = {chore.name for chore in due_chores_1}
    
    print("  Actual chores due today:")
    for chore in due_chores_1:
        print(f"    - {chore.name} ({chore.frequency.name})")
    
    assert due_names_1 == {"Daily Chore", "3Day Chore"}

    # Test Case 2: Date where Daily and Weekly chores should be due
    test_date = OriginalDate(2024, 1, 20)
    print(f"\nTest case 2 - Date: {test_date}")
    print(f"  Days since adjusted start: 14 days")
    print(f"  Expected due chores: Daily (14%1=0), 3Day (14%3≠0), Weekly (14%7=0)")
    
    mock_date.today.return_value = test_date
    due_chores_2 = chore_service.get_chores_due_today(frequency_chores)
    due_names_2 = {chore.name for chore in due_chores_2}
    
    print("  Actual chores due today:")
    for chore in due_chores_2:
        print(f"    - {chore.name} ({chore.frequency.name})")
    
    assert due_names_2 == {"Daily Chore", "Weekly Chore"}

    # Test Case 3: Date where only Daily chores are due
    test_date = OriginalDate(2024, 1, 16)
    print(f"\nTest case 3 - Date: {test_date}")
    print(f"  Days since adjusted start: 10 days")
    print(f"  Expected due chores: Daily (10%1=0), 3Day (10%3≠0), Weekly (10%7≠0)")
    
    mock_date.today.return_value = test_date
    due_chores_3 = chore_service.get_chores_due_today(frequency_chores)
    due_names_3 = {chore.name for chore in due_chores_3}
    
    print("  Actual chores due today:")
    for chore in due_chores_3:
        print(f"    - {chore.name} ({chore.frequency.name})")
    
    assert due_names_3 == {"Daily Chore"}
    print("===========================\n") 