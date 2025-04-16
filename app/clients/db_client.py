# import logging
from datetime import UTC, datetime
from typing import List

from loguru import logger
import sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String, create_engine, exists, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from enums.complexity import Complexity
from enums.frequency import Frequency

Base = declarative_base()


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
    tg_user_id = Column(Integer, unique=True, nullable=False)

class Chore(Base):
    __tablename__ = 'chores'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
    
    name = Column(String, nullable=False)
    complexity = Column(sqlalchemy.Enum(Complexity), nullable=False)
    frequency = Column(sqlalchemy.Enum(Frequency), nullable=False)
    
class TaskSent(Base):
    __tablename__ = 'sent_tasks'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    
class PreviousAssignment(Base):
    __tablename__ = 'tasks_history'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    chore_id = Column(Integer, ForeignKey('chores.id'), nullable=False)

    person = relationship("Person")
    chore = relationship("Chore")

class DBClient:
    def __init__(
        self,
        db_url: str,
    ) -> None:
        logger.info("Initializing db client")
        self._engine = create_engine(url=db_url, echo=False)
        Base.metadata.create_all(self._engine)
        self._sessionmaker = sessionmaker(bind=self._engine)
    
    
    def add_person(self, person: Person):
        logger.info("Adding person")
        session = self._sessionmaker()
        try:
            session.add(person)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            logger.warning(f"User {person.tg_user_id} is already in the database.")
            session.rollback()
        finally:
            session.close()      
    
    def add_chore(
        self,
        chore: Chore
    ) -> None:
        logger.info("Adding chore")
        session = self._sessionmaker()
        try:
            session.add(chore)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            logger.warning(f"Chore {chore.name} is already in the database.")
            session.rollback()
        finally:
            session.close()
            
    def get_chore(
        self, 
        name: str
    ):
        logger.info("Getting chore")
        session = self._sessionmaker()
        try:
            chore = session.query(Chore).filter_by(name=name).first()
            return chore
        finally:
            session.close()
            
    def was_task_sent_today(self) -> bool:
        logger.info("Checking if a task was sent today")
        session = self._sessionmaker()
        try:
            task_exist = session.query(
                exists().where(TaskSent.created_at >= datetime.now(UTC).date())
            ).scalar()
            return task_exist
        finally:
            session.close()

    def mark_task_as_sent(self) -> None:
        """Marks that a task  sent today by inserting a new record."""
        logger.info("Marking task as sent")
        session = self._sessionmaker()
        try:
            sent_task = TaskSent()
            session.add(sent_task)
            session.commit()
            logger.info("Task successfully marked as sent")
        except Exception as e:
            session.rollback()
            logger.error(f"Error marking task as sent: {e}")
        finally:
            session.close()
