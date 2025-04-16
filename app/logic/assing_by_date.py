import datetime
from datetime import timedelta
import random
from typing import List

from loguru import logger

from clients.db_client import Chore, Person, PreviousAssignment

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

    # def assign_tasks(self, chores: List[Chore], persons: List[Person]):
    #     logger.info("Assigning tasks")
    #     """Распределяет задачи по людям"""
    #     if not persons:
    #         return []

    #     random.shuffle(persons)
    #     chores.sort(key=lambda task: task.complexity.value, reverse=True)

    #     tasks_by_person = [{'person': person, 'tasks': []} for person in persons]
    #     group_sums = [0] * len(persons)
    #     group_complexities = [0] * len(persons)

    #     for task in chores:
    #         min_group_idx = min(
    #             range(len(persons)),
    #             key=lambda i: (group_sums[i], group_complexities[i])
    #         )
    #         tasks_by_person[min_group_idx]['tasks'].append({
    #             'name': task.name,
    #             'complexity': task.complexity.value
    #         })
    #         group_sums[min_group_idx] += 1
    #         group_complexities[min_group_idx] += task.complexity.value

    #     return tasks_by_person
    def get_assignment_history(self, days: int = 30, db_session=None) -> List[PreviousAssignment]:
        logger.info(f"Fetching assignment history for the last {days} days")
        today = datetime.date.today()
        start_date = today - timedelta(days=days)
        history = db_session.query(PreviousAssignment).filter(PreviousAssignment.date >= start_date).all()
        logger.info(f"Found {len(history)} assignments")
        return history
    
    def assign_tasks(self, chores: List[Chore], persons: List[Person], history: List[PreviousAssignment] = None, db_session=None):
        logger.info("Assigning tasks with history")

        if not persons:
            return []


        if history is None:
            history = self.get_assignment_history(db_session=db_session)

        random.shuffle(persons)
        chores.sort(key=lambda task: task.complexity.value, reverse=True)

        tasks_by_person = [{'person': person, 'tasks': []} for person in persons]
        group_sums = [0] * len(persons)
        group_complexities = [0] * len(persons)

        assignment_count = {}
        for record in history:
            person_hist = assignment_count.setdefault(record.person_id, {})
            person_hist[record.chore_id] = person_hist.get(record.chore_id, 0) + 1

        for chore in chores:
            min_person_idx = min(
                range(len(persons)),
                key=lambda i: (
                    assignment_count.get(persons[i].id, {}).get(chore.id, 0),
                    group_sums[i],
                    group_complexities[i]
                )
            )

            tasks_by_person[min_person_idx]['tasks'].append({
                'name': chore.name,
                'complexity': chore.complexity.value
            })
            group_sums[min_person_idx] += 1
            group_complexities[min_person_idx] += chore.complexity.value

        return tasks_by_person