from datetime import date, timedelta
import customtkinter as ctk
import hashlib as hash

# LOCAL IMPORTS
import modules.settings as set
from modules.database import SessionLocal, engine
import modules.models as models

class Main(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        self.protocol("WM_DELETE_WINDOW", self.OnClose)
        
        language = set.Language()
        self.lp_main, self.lp_user_panel, self.lp_short_days, self.lp_full_days = language.LoadLangpack(set.LANGUAGE)
        
        self.InitializeDB()
        self.users = self.CountUsers()
        
        if self.users == 0:
            self.db.add(models.Users(name='Admin', password='', admin=True, active=True))
            self.db.commit()
            
        self.active_user = self.db.query(models.Users).where(models.Users.active == 1).one()
        
        # MAIN WINDOW CONFIGURATION
        self.title(self.lp_main[0])
        self.geometry(set.RES)
        ctk.set_widget_scaling(set.SCALE)
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.cards = []
        
        # FONTS TEMPLATES
        self.font_title = ctk.CTkFont(family=set.FONT, size=20, weight="bold")
        self.font_username = ctk.CTkFont(family=set.FONT, size=18, weight="bold")
        self.font_label = ctk.CTkFont(family=set.FONT, size=14)
        self.font_today = ctk.CTkFont(family=set.FONT, size=16, weight='bold')
        self.font_weekend = ctk.CTkFont(family=set.FONT, size=14, slant='italic')
        self.font_info = ctk.CTkFont(family=set.FONT, size=26)
        self.font_footer = ctk.CTkFont(family=set.FONT, size=12, slant='italic')
        
        # MENU FRAME
        self.menu_frame = ctk.CTkFrame(self, corner_radius=0, width=220)
        self.menu_frame.columnconfigure(0, weight=0)
        self.menu_frame.grid(row=0, rowspan=2, column=0, padx=0, pady=0, sticky="nswe")
        
        self.current_user_label = ctk.CTkLabel(self.menu_frame, text=f'{self.lp_main[1]}', font=self.font_title)
        self.current_user_label.grid(row=0, column=0, padx=50, pady=(15, 5), sticky="we")
        self.username_label = ctk.CTkLabel(self.menu_frame, text=f'{self.active_user.name}', font=self.font_username)
        self.username_label.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="we")
        self.username_label.configure(text_color='#3a7ebf')
        
        self.user_panel_button = ctk.CTkButton(self.menu_frame, text=f'{self.lp_main[2]}', font=self.font_label, command=self.OpenUserPanel)
        self.user_panel_button.grid(row=2, column=0, padx=40, pady=5, sticky="we")
        
        # CONTENT FRAME
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)
        self.content_frame.rowconfigure(0, weight=0)
        self.content_frame.rowconfigure([1, 2, 3, 4, 5, 6], weight=1)
        self.content_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nswe")

        # FOOTER
        self.footer_label = ctk.CTkLabel(self, text=set.VER, font=self.font_footer)
        self.footer_label.grid(row=1, column=1, padx=5, pady=(5, 0), sticky="e")
        self.footer_label.configure(text_color='gray30')
        
        # BUILD CALENDAR
        self.today = date.today()
        self.first_day = (self.today - timedelta(self.today.day - 1))
        self.first_day_weekday = int(self.first_day.strftime("%w"))
        self.cal: list = self.lp_short_days
        
        for day in range(42):
            self.cal.append((self.first_day + timedelta(day - self.first_day_weekday + 1)))
            
        current_row = 0
        current_col = 0
        
        for i in range(len(self.cal)):
            if (i) % 7 == 0 and i > 1:
                current_row += 1
                current_col = 0
                
            card = ctk.CTkFrame(self.content_frame)
            card.grid(row=current_row, column=current_col, padx=5, pady=5, sticky="nswe")
            card.rowconfigure(0, weight=1)
            card.columnconfigure(0, weight=1)
            
            if i < 7:
                date_label = ctk.CTkLabel(card, text=f'{self.cal[i]}', font=self.font_weekend)
                date_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")
            else:
                if int(self.cal[i].strftime("%w")) == 6 or int(self.cal[i].strftime("%w")) == 0:
                    date_label = ctk.CTkLabel(card, text=f'{self.cal[i].strftime("%d")}', font=self.font_weekend)
                    date_label.configure(text_color='red')
                else:
                    date_label = ctk.CTkLabel(card, text=f'{self.cal[i].strftime("%d")}', font=self.font_label)
                            
                date_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nwe")

            if self.cal[i] == self.today:
                card.configure(border_width=2, border_color='#3a7ebf')
                date_label.configure(font=self.font_today, text_color='#3a7ebf')
                
            self.cards.append(card)
            current_col += 1
            
        self.mainloop()
        
        
    def InitializeDB(self):
        """Initializes connection with database.
        """
        models.Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
       
        
    def CountUsers(self) -> int:
        """Returns number of users in database.

        Returns:
            int: User count.
        """
        return self.db.query(models.Users).count()
    
    
    def OpenUserPanel(self) -> None:
        """Opens panel where user may change the username, password, and manage his habits.
        """
        self.user_panel = ctk.CTkToplevel(self)

        self.user_panel.geometry('800x600')
        self.user_panel.attributes('-topmost', True)
        self.user_panel.title(self.lp_main[2])
        
        self.user_panel.grid_columnconfigure(0, weight=0)
        self.user_panel.grid_columnconfigure(1, weight=1)
        self.user_panel.grid_rowconfigure(0, weight=1)
        
        # MENU FRAME
        self.user_menu_frame = ctk.CTkFrame(self.user_panel, corner_radius=0, width=220)
        self.user_menu_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")
        
        self.change_username_label = ctk.CTkLabel(self.user_menu_frame, text=f'{self.lp_user_panel[1]}', font=self.font_label)
        self.change_username_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 0), sticky="nswe")
        
        self.change_username_entry = ctk.CTkEntry(self.user_menu_frame, placeholder_text=self.active_user.name)
        self.change_username_entry.grid(row=1, column=0, padx=(10, 5), pady=0, sticky="nswe")
        
        self.change_username_button = ctk.CTkButton(self.user_menu_frame, text=f'{self.lp_user_panel[4]}', width=40, font=self.font_label, command=self.ChangeUsername)
        self.change_username_button.grid(row=1, column=1, padx=(5, 20), pady=0, sticky="nswe")
        
        self.change_username_status = ctk.CTkLabel(self.user_menu_frame, text=f'', font=self.font_label)
        self.change_username_status.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="nswe")
        
        self.change_password_label = ctk.CTkLabel(self.user_menu_frame, text=f'{self.lp_user_panel[10]}', font=self.font_label)
        self.change_password_label.grid(row=3, column=0, columnspan=2, padx=15, pady=(10, 0), sticky="nswe")
        
        self.change_password_entry = ctk.CTkEntry(self.user_menu_frame, placeholder_text="*********", show="*")
        self.change_password_entry.grid(row=4, column=0, padx=(10, 5), pady=0, sticky="nswe")
        
        if self.active_user.password:
            self.change_password_button = ctk.CTkButton(self.user_menu_frame, text=f'{self.lp_user_panel[4]}', width=40, font=self.font_label, command=self.ChangePassword)
        else:
            self.change_password_button = ctk.CTkButton(self.user_menu_frame, text=f'{self.lp_user_panel[3]}', width=40, font=self.font_label, command=self.ChangePassword)
        self.change_password_button.grid(row=4, column=1, padx=(5, 20), pady=0, sticky="nswe")
        
        self.change_password_status = ctk.CTkLabel(self.user_menu_frame, text=f'', font=self.font_label)
        self.change_password_status.grid(row=5, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="nswe")
        
        # CONTENT FRAME
        self.user_content_frame = ctk.CTkFrame(self.user_panel)
        self.user_content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        
        
    def ChangeUsername(self) -> None:
        """Changes username
        """
        if not self.change_username_entry.get():
            self.change_username_status.configure(text=self.lp_user_panel[6], text_color="red")
            return
        
        if len(self.change_username_entry.get()) < 3:
            self.change_username_status.configure(text=self.lp_user_panel[7], text_color="red")
            return
        
        spec = '!@#$%^&*()[]{}\'"?,.<>;:\\| '
        test = [char for char in self.change_username_entry.get() if char in spec]
        
        if test:
            self.change_username_status.configure(text=self.lp_user_panel[8], text_color="red")
            return
        
        if self.change_username_entry.get() == self.active_user.name:
            self.change_username_status.configure(text=self.lp_user_panel[8], text_color="red")
            return
        
        self.db.query(models.Users).where(models.Users.id == self.active_user.id).update({models.Users.name: self.change_username_entry.get()})
        self.db.commit()
        
        self.active_user = self.db.query(models.Users).where(models.Users.active == 1).one()
        self.username_label.configure(text=self.active_user.name)
        self.change_username_status.configure(text=self.lp_user_panel[5], text_color="lightgreen")
        
        
    def ChangePassword(self):
        hashed = hash.sha256(self.change_password_entry.get().encode()).hexdigest()
        
        if not self.change_password_entry.get():
            self.change_password_status.configure(text=self.lp_user_panel[12], text_color="red")
            return
        
        if len(self.change_password_entry.get()) < 8:
            self.change_password_status.configure(text=self.lp_user_panel[13], text_color="red")
            return
        
        spec = '!@#$%^&*()[]{}\'"?,.<>;:\\| '
        test = [char for char in self.change_password_entry.get() if char in spec]
        if test:
            self.change_password_status.configure(text=self.lp_user_panel[14], text_color="red")
            return
        
        if hashed == self.active_user.password:
            self.change_password_status.configure(text=self.lp_user_panel[15], text_color="red")
            return
        
        self.db.query(models.Users).where(models.Users.id == self.active_user.id).update({models.Users.password: hashed})
        self.db.commit()
        
        self.active_user = self.db.query(models.Users).where(models.Users.active == 1).one()
        self.change_password_status.configure(text=self.lp_user_panel[11], text_color="lightgreen")
        
    
    def OnClose(self):
        """Defines all actions to be done before closing the app.
        """
        self.db.close()
        self.quit()      
        
    
if __name__ == "__main__":
    Main()
