# import logging
from datetime import UTC, datetime
from typing import List

from loguru import logger
import sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from enums.complexity import Complexity
from enums.frequency import Frequency

# Base = declarative_base()


# class Person(Base):
#     __tablename__ = "persons"
#     id = Column(Integer, primary_key=True)
#     created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
#     updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
#     tg_user_id = Column(Integer, unique=True, nullable=False)
    
# class TeamMember(Base):
#     __tablename__ = "team_members"
#     id = Column(Integer, primary_key=True)
#     team_id = Column(Integer, sqlalchemy.ForeignKey("teams.id"), nullable=False)
#     tg_user_id = Column(Integer, nullable=False)  # Telegram user ID
#     role = Column(String, nullable=True)  # Optional: Can store "admin", "member", etc.
#     joined_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

# class Chore(Base):
#     __tablename__ = 'chores'
#     # service fields
#     id = Column(Integer, primary_key=True)
#     created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
#     updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
#     # entry fields
#     tg_group_id = Column(Integer, nullable=False)
#     name = Column(String, nullable=False)
#     complexity = Column(sqlalchemy.Enum(Complexity), nullable=False)
#     frequency = Column(sqlalchemy.Enum(Frequency), nullable=False)


# class DBClient:
#     def __init__(
#         self,
#         db_url: str,
#     ) -> None:
#         logger.info("Initializing db client")
#         self._engine = create_engine(url=db_url, echo=False)
#         Base.metadata.create_all(self._engine)
#         self._sessionmaker = sessionmaker(bind=self._engine)
    
#     def add_team(self, name: str) -> Team | None:
#         logger.info(f"Adding team: {name}")
#         session = self._sessionmaker()
#         try:
#             team = Team(name=name)
#             session.add(team)
#             session.commit()
#             logger.info(f"Team {name} successfully added!")  # Новый лог
#             return team
#         except sqlalchemy.exc.IntegrityError:
#             logger.warning(f"Team {name} already exists.")
#             session.rollback()
#         except Exception as e:
#             logger.exception(f"Error adding team: {e}")  # Лог ошибки
#         finally:
#             session.close()
#         return None

    
#     def get_teams_by_user(self, user_id: int):
#         with self._sessionmaker() as session:
#             return session.query(Team).join(TeamMember, Team.id == TeamMember.team_id) \
#                 .filter(TeamMember.tg_user_id == user_id).all()

    
#     def add_person(self, person: Person):
#         logger.info("Adding person")
#         session = self._sessionmaker()
#         try:
#             session.add(person)
#             session.commit()
#         except sqlalchemy.exc.IntegrityError:
#             logger.warning(f"User {person.tg_user_id} is already in the database.")
#             session.rollback()
#         finally:
#             session.close()
            
#     def get_person_by_tg_user_id(
#         self,
#         tg_user_id: int
#     ) -> Person | None:
#         logger.info("Getting person by tg_user_id")
#         with self._sessionmaker() as session:
#             return session.query(Person).filter_by(tg_user_id=tg_user_id).first()

#     def get_persons_by_tg_group_id(
#         self,
#         tg_group_id: int
#     ) -> List[Person]:
#         logger.info("Getting persons by tg_group_id")
#         with self._sessionmaker() as session:
#             return session.query(Person).filter_by(tg_group_id=tg_group_id).all()
            
#     def get_person_by_user_and_group(
#         self, 
#         tg_user_id: int, 
#         tg_group_id: int
#     ) -> Person | None:
#         logger.info("Getting person by user and group")
#         try:
#             with self._sessionmaker() as session:
#                 return session.query(Person).filter_by(tg_user_id=tg_user_id, tg_group_id=tg_group_id).first()
#         except Exception:
#             logger.exception("Error in get_person_by_user_and_group")
#             raise
        
#     def delete_person_by_tg_user_id(
#         self,
#         tg_user_id: int
#     ) -> None:
#         logger.info("Deleting person by tg_user_id")
#         session = self._sessionmaker()
#         try:
#             person = session.query(Person).filter_by(tg_user_id=tg_user_id).first()
#             if person:
#                 session.delete(person)
#                 session.commit()
#         except Exception:
#             logger.exception("Error in delete_person_by_tg_user_id")
#             session.rollback()
#         finally:
#             session.close()
    
#     def add_chore(
#         self,
#         chore: Chore
#     ) -> None:
#         logger.info("Adding chore")
#         session = self._sessionmaker()
#         try:
#             session.add(chore)
#             session.commit()
#         except sqlalchemy.exc.IntegrityError:
#             logger.warning(f"Chore {chore.name} is already in the database.")
#             session.rollback()
#         finally:
#             session.close()
    
#     def get_chores_by_tg_group_id(
#         self,
#         tg_group_id: str
#     ) -> List[Chore]:
#         logger.info("Getting chores by tg_group_id")
#         with self._sessionmaker() as session:
#             return session.query(Chore).filter_by(tg_group_id=tg_group_id).all()
        
#     def get_chore_by_name_and_tg_group_id(
#         self, 
#         task_name: str, 
#         tg_group_id: str
#     ) -> Chore | None:
#         logger.info("Getting chore by name and tg_group_id")
#         with self._sessionmaker() as session:
#             return session.query(Chore).filter_by(name=task_name, tg_group_id=tg_group_id).first()
        
#     def update_chore_by_id(
#         self,
#         chore_id: int,
#         name: str | None = None,
#         complexity: Complexity | None = None,
#         frequency: Frequency | None = None
#     ) -> None:
#         logger.info("Updating chore by id")
#         session = self._sessionmaker()
#         try:
#             chore = session.query(Chore).filter_by(id=chore_id).first()
#             if name:
#                 chore.name = name  # type: ignore
#             if complexity:
#                 chore.complexity = complexity  # type: ignore
#             if frequency:
#                 chore.frequency = frequency  # type: ignore
#             session.commit()
#         except Exception:
#             logger.exception("Error in update_chore_by_id")
#             session.rollback()
#         finally:
#             session.close()
    
#     def delete_chore_by_id(
#         self,
#         chore_id: int
#     ) -> None:
#         logger.info("Deleting chore by id")
#         session = self._sessionmaker()
#         try:
#             chore = session.query(Chore).filter_by(id=chore_id).first()
#             if chore:
#                 session.delete(chore)
#                 session.commit()
#         except Exception:
#             logger.exception("Error in delete_chore_by_id")
#             session.rollback()
#         finally:
#             session.close()
