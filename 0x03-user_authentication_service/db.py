#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Returns the first row found in the users table as filtered
            by the method input arguments.
        """
        for k, v in kwargs.items():
            try:
                getattr(User, k)
            except AttributeError:
                raise InvalidRequestError

            user = self._session.query(User).filter(
                getattr(User, k) == v).first()

            if not user:
                raise NoResultFound

            return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates the user attributes as passed in the method arguments
        """
        user = self.find_user_by(id=user_id)

        for k, v in kwargs.items():
            try:
                getattr(User, k)
            except AttributeError:
                raise ValueError

            user.__setattr__(k, v)

        self._session.commit()
