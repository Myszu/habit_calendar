import modules.models as models

class Users():
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db
        
    
    def GetActive(self) -> dict:
        """Returns all the data of currently `active user` from database.

        Returns:
            dict: Data packed into dictionary.
        """
        return self.db.query(models.Users).where(models.Users.active == 1).one()
        
        
    def Update(self, column: str, value: str) -> dict | None:
        """Updates a field of given `column` in database with `value` for `active user`. 

        Args:
            column (str): Name of column of which field should be updated.
            value (str): Value that should be inserted.

        Returns:
            dict | None: Dictionary with all the data of updated user or nothing if fails.
        """
        active = self.GetActive()
        columns = {
            'name': models.Users.name,
            'password': models.Users.password,
            'language': models.Users.language,
            'shorts': models.Users.shorts,
            'theme': models.Users.theme,
            'mode': models.Users.mode,
            'admin': models.Users.admin,
            'active': models.Users.active
        }
        if column in columns.keys():
            self.db.query(models.Users).where(models.Users.id == active.id).update({columns.get(column): value})
            self.db.commit()
            return self.GetActive()
        return
    
    
    def Add(self, name: str, password: str, language: str, shorts: bool, theme: str, mode: str, admin: bool, active: bool) -> None:
        """Adds user to the database.

        Args:
            name (str): User's name.
            password (str): Users password (might remain empty initially if user does not care about privacy).
            language (str): User's preferable app display language.
            shorts (bool): If true app displays shorted version of week days.
            theme (str): User's preferable app theme.
            mode (str): User's preferable app mode (light, dark, default).
            admin (bool): Is user an administrator of this app?
            active (bool): If true, user becomes active (logged in).
        """
        self.db.add(models.Users(name=name, password=password, language=language, shorts=shorts, theme=theme, mode=mode, admin=admin, active=active))
        self.db.commit()
        
        
    def CountUsers(self) -> int:
        """Returns number of users in database.

        Returns:
            int: User count.
        """
        return self.db.query(models.Users).count()
