import modules.models as models
from datetime import date, datetime

class Habits():
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db

    
    def Add(self, user: str, habit_name: str, icon: str, start: str, freq: int, qty: int, weekends: str):
        start = datetime.strptime(start, '%d.%m.%Y')
        self.db.add(models.Habits(user=user, habit_name=habit_name, icon=icon, start_date=start, frequency=freq, quantity=qty, weekends=weekends))
        self.db.commit()