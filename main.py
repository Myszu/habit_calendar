from datetime import date, timedelta
import customtkinter

# LOCAL IMPORTS
import modules.settings as set
from modules.database import SessionLocal, engine
import modules.models as models

class Main(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        language = set.Language()
        self.langpack = language.LoadLangpack(set.LANGUAGE)
        
        self.InitializeDB()
        self.users = self.CheckUsers()
        
        if self.users == 0:
            self.db.add(models.Users(name='Admin', password='', admin=True))
            self.db.commit()
        
        self.title(self.langpack[0][0])
        self.geometry(set.RES)
        customtkinter.set_widget_scaling(set.SCALE)
        # self.protocol("WM_DELETE_WINDOW", self.OnClose)
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.cards = []
        
        # FONTS TEMPLATES
        self.font_title = customtkinter.CTkFont(family=set.FONT, size=20, weight="bold")
        self.font_label = customtkinter.CTkFont(family=set.FONT, size=14)
        self.font_weekend = customtkinter.CTkFont(family=set.FONT, size=14, slant='italic')
        self.font_info = customtkinter.CTkFont(family=set.FONT, size=26)
        
        # MENU FRAME
        self.menu_frame = customtkinter.CTkFrame(self, corner_radius=0, width=220)
        self.menu_frame.columnconfigure(0, weight=0)
        self.menu_frame.grid(row=0, rowspan=2, column=0, padx=0, pady=0, sticky="nswe")
        
        # CONTENT FRAME
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)
        self.content_frame.rowconfigure(0, weight=0)
        self.content_frame.rowconfigure([1, 2, 3, 4, 5, 6], weight=1)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        self.today = date.today()
        self.first_day = (self.today - timedelta(self.today.day - 1))
        self.first_day_weekday = int(self.first_day.strftime("%w"))
        self.cal: list = self.langpack[1]
        
        for day in range(42):
            self.cal.append((self.first_day + timedelta(day - self.first_day_weekday + 1)))
            
        current_row = 0
        current_col = 0
        
        for i in range(len(self.cal)):
            if (i) % 7 == 0 and i > 1:
                current_row += 1
                current_col = 0
                
            card = customtkinter.CTkFrame(self.content_frame)
            card.grid(row=current_row, column=current_col, padx=5, pady=5, sticky="nswe")
            card.rowconfigure(0, weight=1)
            card.columnconfigure(0, weight=1)
            
            if i < 7:
                date_label = customtkinter.CTkLabel(card, text=f'{self.cal[i]}', font=self.font_weekend)
                date_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")
            else:
                if int(self.cal[i].strftime("%w")) == 6 or int(self.cal[i].strftime("%w")) == 0:
                    date_label = customtkinter.CTkLabel(card, text=f'{self.cal[i].strftime("%d")}', font=self.font_weekend)
                    date_label.configure(text_color='red')
                else:
                    date_label = customtkinter.CTkLabel(card, text=f'{self.cal[i].strftime("%d")}', font=self.font_label)
                    
                if self.cal[i] == self.today:
                    date_label.configure(text_color='cyan')
                    
                date_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nwe")

            self.cards.append(card)
            current_col += 1
            
        self.mainloop()
        
        
    def InitializeDB(self):
        models.Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
       
        
    def CheckUsers(self):
        return self.db.query(models.Users).count()
        
    
if __name__ == "__main__":
    Main()
