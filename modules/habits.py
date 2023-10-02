import modules.models as models
from datetime import datetime

class Habits():
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db

    
    def Add(self, user_id: int, name: str, icon: str, start: str, freq: int, qty: int, weekends: int):
        """Adds new habit to the database with given parameters.

        Args:
            user (str): Username that this habit belongs to.
            habit_name (str): Name of this habit
            icon (str): Id of an icon associated with this habit.
            start (str): Start date of this habit.
            freq (int): Frequency of occurence.
            qty (int): Quantity of occurences.
            weekends (int): States how this habits tasks belongs at weekend.
        """
        start = datetime.strptime(start, '%d.%m.%Y')
        self.db.add(models.Habits(user_id=user_id, name=name, icon=icon, start_date=start, frequency=freq, quantity=qty, weekends=weekends))
        self.db.commit()
        
    
    def Get(self, id: int) -> object:
        """Gets details of given habit.

        Args:
            id (int): ID of lookup habit.

        Returns:
            object: Whole set of given habit's data.
        """
        return self.db.query(models.Habits).where(models.Habits.id == id).one()
        

    def GetNewest(self, user_id: int) -> list:
        """Finds the newest, added habit of given user.

        Args:
            user_id (int): ID of the user.

        Returns:
            list: List of Dictionary-like objects with 
        """
        return self.db.query(models.Habits).where(models.Habits.user_id == user_id).all()[-1]
    
    
    def GetUsersHabits(self, user_id: int) -> object:
        """Finds all habits of given user.

        Args:
            user_id (int): ID of the user.

        Returns:
            object: Dictionary-like object of given user's habits.
        """
        return self.db.query(models.Habits).where(models.Habits.user_id == user_id).all()