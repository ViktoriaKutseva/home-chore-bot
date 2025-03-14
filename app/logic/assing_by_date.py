import datetime
from datetime import timedelta
import random
from typing import List

from loguru import logger

from clients.db_client import Chore, Person

class ChoreDistributionService:
    def __init__(self) -> None:
        pass

    def get_chores_due_today(self, all_chores: List[Chore]) -> List[Chore]:
        logger.info("Getting chores due today")
        today_date = datetime.date.today()
        first_day_of_year = datetime.date(today_date.year, 1, 1)
        jan_1_weekday = first_day_of_year.weekday() 
        days_offset = (5 - jan_1_weekday) % 7
        adjusted_first_day = first_day_of_year + timedelta(days=days_offset)
        day_of_year = (today_date - adjusted_first_day).days

        return [chore for chore in all_chores if (day_of_year % chore.frequency.value) == 0]

    def assign_tasks(self, chores: List[Chore], persons: List[Person]):
        logger.info("Assigning tasks")
        """Распределяет задачи по людям"""
        if not persons:
            return []

        random.shuffle(persons)
        chores.sort(key=lambda task: task.complexity.value, reverse=True)

        tasks_by_person = [{'person': person, 'tasks': []} for person in persons]
        group_sums = [0] * len(persons)
        group_complexities = [0] * len(persons)

        for task in chores:
            min_group_idx = min(
                range(len(persons)),
                key=lambda i: (group_sums[i], group_complexities[i])
            )
            tasks_by_person[min_group_idx]['tasks'].append({
                'name': task.name,
                'complexity': task.complexity.value
            })
            group_sums[min_group_idx] += 1
            group_complexities[min_group_idx] += task.complexity.value

        return tasks_by_person
