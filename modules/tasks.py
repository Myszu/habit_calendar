import modules.models as models
from datetime import date

class Tasks():
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db

    
    def Add(self, user: str, name: str, date: date, state: bool = False):
        """Adds a task of a habit to the database.

        Args:
            user (str): Name of the user that this task belongs to.
            task_name (str): Task name which is basically Habit's name.
            date (date): Date of occurence.
            state (bool, optional): If fulfilled sets to True. Defaults to False.
        """
        self.db.add(models.Tasks(user=user, name=name, date=date, state=state))
        self.db.commit()
        
    
    def Get(self, id: int) -> dict:
        """Gets details of given task.

        Args:
            id (int): ID of lookup task.

        Returns:
            dict: Whole set of given task's data.
        """
        return self.db.query(models.Tasks).where(models.Tasks.id == id).one()
        