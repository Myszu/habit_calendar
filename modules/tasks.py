import modules.models as models
from datetime import date

class Tasks():
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db

    
    def Add(self, user_id: int, name: str, date: date, state: bool = False) -> None:
        """Adds a task of a habit to the database.

        Args:
            user (str): Name of the user that this task belongs to.
            task_name (str): Task name which is basically Habit's name.
            date (date): Date of occurence.
            state (bool, optional): If fulfilled sets to True. Defaults to False.
        """
        self.db.add(models.Tasks(user_id=user_id, name=name, date=date, state=state))
        self.db.commit()
        
    
    def Get(self, id: int) -> object:
        """Gets details of given task.

        Args:
            id (int): ID of lookup task.

        Returns:
            object: Dictionary-like set of given task's data.
        """
        return self.db.query(models.Tasks).where(models.Tasks.id == id).one()
    
    
    def GetUsersTasks(self, user_id: int) -> object:
        """Finds all tasks of given user.

        Args:
            user_id (int): ID of given user.

        Returns:
            object: Dictionary-like object of given user's tasks.
        """
        return self.db.query(models.Tasks).where(models.Tasks.user_id == user_id).all()
        
