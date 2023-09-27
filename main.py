from datetime import date, timedelta
import customtkinter as ctk
import hashlib as hash
import os

# LOCAL IMPORTS
from modules.database import SessionLocal, engine
from modules.users import Users
from modules.habits import Habits
from modules.tasks import Tasks
from modules.language import Language
import modules.settings as set
import modules.models as models
from PIL import ImageTk

INSTANCES = []

class Main(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        self.protocol("WM_DELETE_WINDOW", self.OnClose)
    
        self.iconpath = ImageTk.PhotoImage(file=os.path.join("","icon.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        
        self.language = Language()
        
        self.InitializeDB()
        self.users, self.habits, self.tasks = Users(self.db), Habits(self.db), Tasks(self.db)
        self.users_count = self.users.CountUsers()
        
        if self.users_count == 0:
            self.users.Add(
                name='Admin',
                password='',
                language=set.LANGUAGE,
                shorts=set.SHORTCUTS,
                theme=set.THEME,
                mode=set.MODE,
                admin=True,
                active=True
                )            
        
        self.active_user = self.users.GetActive()
        self.ApplyUserPref()
        
        # MAIN WINDOW CONFIGURATION
        self.title(self.lp_main['title'])
        self.geometry(set.RES)
        ctk.set_widget_scaling(set.SCALE)
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.cards = []
        self.icons = {
            'weights': '🏋️',
            'cycling': '🚴',
            'run': '🏃',
            'swim': '🏊',
            'read': '📖',
            'guitar': '🎸',
            'violin': '🎻',
            'percussion': '🥁',
            'trumpet': '🎺'
            }
        
        # FONTS TEMPLATES
        self.font_title = ctk.CTkFont(family=set.FONT, size=20, weight="bold")
        self.font_username = ctk.CTkFont(family=set.FONT, size=18, weight="bold")
        self.font_label = ctk.CTkFont(family=set.FONT, size=14)
        self.font_today = ctk.CTkFont(family=set.FONT, size=16, weight='bold')
        self.font_weekend = ctk.CTkFont(family=set.FONT, size=14, slant='italic')
        self.font_info = ctk.CTkFont(family=set.FONT, size=26)
        self.font_footer = ctk.CTkFont(family=set.FONT, size=12, slant='italic')
        self.font_tip = ctk.CTkFont(family=set.FONT, size=12, slant='italic')
        
        # MENU FRAME
        self.menu_frame = ctk.CTkFrame(self, corner_radius=0, width=220)
        self.menu_frame.columnconfigure(0, weight=0)
        self.menu_frame.rowconfigure(2, weight=1)
        self.menu_frame.grid(row=0, rowspan=2, column=0, padx=0, pady=0, sticky="nswe")
        
        self.current_user_label = ctk.CTkLabel(self.menu_frame, text=f'{self.lp_main["active-user"]}', font=self.font_title)
        self.current_user_label.grid(row=0, column=0, padx=50, pady=(15, 5), sticky="we")
        self.username_label = ctk.CTkLabel(self.menu_frame, text=f'{self.active_user.name}', font=self.font_username)
        self.username_label.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="we")
        self.username_label.configure(text_color=self.main_color)
        
        self.user_panel_button = ctk.CTkButton(self.menu_frame, text=f'{self.lp_main["user-panel"]}', font=self.font_label, command=self.OpenUserPanel)
        self.user_panel_button.grid(row=2, column=0, padx=40, pady=(5, 15), sticky="swe")
        
        # CONTENT FRAME
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)
        self.content_frame.rowconfigure(0, weight=0)
        self.content_frame.rowconfigure([1, 2, 3, 4, 5], weight=1)
        self.content_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nswe")

        # FOOTER
        self.footer_label = ctk.CTkLabel(self, text=set.VER, font=self.font_footer)
        self.footer_label.grid(row=1, column=1, padx=5, pady=(5, 0), sticky="e")
        self.footer_label.configure(text_color='gray50')
        
        # BUILD CALENDAR
        self.today = date.today()
        self.first_day = (self.today - timedelta(self.today.day - 1))
        self.first_day_weekday = int(self.first_day.strftime("%w"))
            
        for day in range(35):
            self.cal.append((self.first_day + timedelta(day - self.first_day_weekday + 1)))
            
        current_row = 0
        current_col = 0
        current_month = date.today().month
        
        for i in range(len(self.cal)):
            if (i) % 7 == 0 and i > 1:
                current_row += 1
                current_col = 0
                
            card = ctk.CTkFrame(self.content_frame)
            card.grid(row=current_row, column=current_col, padx=5, pady=5, sticky="nswe")
            card.rowconfigure(0, weight=1)
            card.columnconfigure(0, weight=1)
            
            if i < 7:
                date_label = ctk.CTkLabel(card, text=f'{self.cal[i]}', font=self.font_weekend, text_color=self.main_color)
                date_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")
            else:
                if int(self.cal[i].strftime("%w")) == 6 or int(self.cal[i].strftime("%w")) == 0:
                    date_label = ctk.CTkLabel(card, text=f'{self.cal[i].strftime("%d")}', font=self.font_weekend)
                    
                    if self.cal[i].month != current_month:
                        date_label.configure(text_color="darkred")
                    else:
                        date_label.configure(text_color='red')
                else:
                    date_label = ctk.CTkLabel(card, text=f'{self.cal[i].strftime("%d")}', font=self.font_label)
                
                    if self.cal[i].month != current_month:
                        date_label.configure(text_color="gray50")
                        
                date_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nwe")

            if self.cal[i] == self.today:
                card.configure(border_width=2, border_color=self.main_color)
                date_label.configure(font=self.font_today, text_color=self.main_color)
                
            self.cards.append(card)
            current_col += 1
        
        
    def ApplyUserPref(self) -> None:
        """Applies users preferences to various settings.
        """
        self.lp_main, self.lp_user_panel, self.lp_weekends, self.lp_tips, self.lp_tabs_names, self.lp_habit_statuses, self.lp_settings, self.languages_names, self.lp_short_days, self.lp_full_days = self.language.LoadLangpack(self.active_user.language)
        
        if self.active_user.theme == 'blue':
            ctk.set_default_color_theme("dark-blue")
            self.main_color = '#3a7ebf'
        else:
            ctk.set_default_color_theme(self.active_user.theme)
            self.main_color = self.active_user.theme
            
        if self.active_user.mode == 'default':
            ctk.set_appearance_mode('system')
        else:
            ctk.set_appearance_mode(self.active_user.mode)
            
        if self.active_user.shorts:
            self.cal: list = self.lp_short_days
        else:
            self.cal: list = self.lp_full_days
        
        
    def InitializeDB(self) -> None:
        """Initializes connection with database.
        """
        models.Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
    
    
    def OpenUserPanel(self) -> None:
        """Opens panel where user may change the username, password, and manage his habits.
        """
        self.user_panel = ctk.CTkToplevel(self)

        self.user_panel.geometry('800x600')
        self.user_panel.attributes('-topmost', True)
        self.user_panel.title(self.lp_main['user-panel'])
        
        self.user_panel.grid_columnconfigure(0, weight=0)
        self.user_panel.grid_columnconfigure(1, weight=1)
        self.user_panel.grid_rowconfigure(0, weight=1)
        
        # MENU FRAME
        self.user_menu_frame = ctk.CTkFrame(self.user_panel, corner_radius=0, width=220)
        self.user_menu_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")
        
        # USERNAME
        self.change_username_label = ctk.CTkLabel(self.user_menu_frame, text=f'{self.lp_user_panel["name"]}', font=self.font_label)
        self.change_username_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 0), sticky="nswe")
        
        self.change_username_entry = ctk.CTkEntry(self.user_menu_frame, placeholder_text=self.active_user.name)
        self.change_username_entry.grid(row=1, column=0, padx=(10, 5), pady=0, sticky="nswe")
        
        self.change_username_button = ctk.CTkButton(self.user_menu_frame, text=f'{self.lp_settings["change"]}', width=40, font=self.font_label, command=self.ChangeUsername)
        self.change_username_button.grid(row=1, column=1, padx=(5, 20), pady=0, sticky="nswe")
        
        self.change_username_status = ctk.CTkLabel(self.user_menu_frame, text=f'', font=self.font_label)
        self.change_username_status.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 2), sticky="nswe")
        
        # PASSWORD
        self.change_password_label = ctk.CTkLabel(self.user_menu_frame, text=f'{self.lp_user_panel["password"]}', font=self.font_label)
        self.change_password_label.grid(row=3, column=0, columnspan=2, padx=15, pady=0, sticky="nswe")
        
        self.change_password_entry = ctk.CTkEntry(self.user_menu_frame, show="*")
        self.change_password_entry.grid(row=4, column=0, padx=(10, 5), pady=0, sticky="nswe")
        
        if not self.active_user.password:
            self.change_password_button = ctk.CTkButton(self.user_menu_frame, text=f'{self.lp_settings["set"]}', width=40, font=self.font_label, command=self.ChangePassword)
        else:
            self.change_password_button = ctk.CTkButton(self.user_menu_frame, text=f'{self.lp_settings["change"]}', width=40, font=self.font_label, command=self.ChangePassword)
        self.change_password_button.grid(row=4, column=1, padx=(5, 20), pady=0, sticky="nswe")
        
        self.change_password_status = ctk.CTkLabel(self.user_menu_frame, text=f'', font=self.font_label)
        self.change_password_status.grid(row=5, column=0, columnspan=2, padx=15, pady=(0, 5), sticky="nswe")
        
        # LANGUAGE
        self.change_language_label = ctk.CTkLabel(self.user_menu_frame, text=f'{self.lp_user_panel["language"]}', font=self.font_label)
        self.change_language_label.grid(row=6, column=0, columnspan=2, padx=15, pady=0, sticky="nswe")
        
        self.change_language_combo = ctk.CTkComboBox(self.user_menu_frame, font=self.font_label, values=self.languages_names)
        self.change_language_combo.grid(row=7, column=0, padx=15, pady=0, sticky="nswe")
        
        self.change_language_button = ctk.CTkButton(self.user_menu_frame, text=f'{self.lp_settings["change"]}', width=40, font=self.font_label, command=self.ChangeLanguage)
        self.change_language_button.grid(row=7, column=1, padx=(5, 20), pady=0, sticky="nswe")
        
        # SHORTCUTS
        self.off_on = [self.lp_settings['off'], self.lp_settings['on']]
        self.change_shortcuts_label = ctk.CTkLabel(self.user_menu_frame, text=f'{self.lp_user_panel["shortcuts"]}', font=self.font_label)
        self.change_shortcuts_label.grid(row=8, column=0, columnspan=2, padx=15, pady=0, sticky="nswe")
        
        self.change_shortcuts_segbutton = ctk.CTkSegmentedButton(self.user_menu_frame, font=self.font_label, values=self.off_on, command=self.ChangeShortcuts)
        self.change_shortcuts_segbutton.grid(row=9, column=0, columnspan=2, padx=15, pady=0, sticky="nswe")
        self.change_shortcuts_segbutton.set(self.off_on[int(self.active_user.shorts)])
        
        # THEME
        self.themes_colors = [self.lp_settings['blue'], self.lp_settings['green']]
        self.change_theme_label = ctk.CTkLabel(self.user_menu_frame, text=f'{self.lp_user_panel["theme"]}', font=self.font_label)
        self.change_theme_label.grid(row=10, column=0, columnspan=2, padx=15, pady=0, sticky="nswe")
        
        self.change_theme_combo = ctk.CTkComboBox(self.user_menu_frame, font=self.font_label, values=self.themes_colors)
        self.change_theme_combo.grid(row=11, column=0, padx=15, pady=0, sticky="nswe")
        
        self.change_theme_button = ctk.CTkButton(self.user_menu_frame, text=f'{self.lp_settings["change"]}', width=40, font=self.font_label, command=self.ChangeTheme)
        self.change_theme_button.grid(row=11, column=1, padx=(5, 20), pady=0, sticky="nswe")
        
        # MODE
        self.modes = [self.lp_settings['light'], self.lp_settings['dark'], self.lp_settings['default']]
        self.change_mode_label = ctk.CTkLabel(self.user_menu_frame, text=f'{self.lp_user_panel["mode"]}', font=self.font_label)
        self.change_mode_label.grid(row=12, column=0, columnspan=2, padx=15, pady=0, sticky="nswe")
        
        self.change_mode_segbutton = ctk.CTkSegmentedButton(self.user_menu_frame, font=self.font_label, values=self.modes, command=self.ChangeMode)
        self.change_mode_segbutton.grid(row=13, column=0, columnspan=2, padx=15, pady=0, sticky="nswe")
        self.change_mode_segbutton.set(self.lp_settings[(self.active_user.mode)])
        
        # CONTENT FRAME
        self.user_content_frame = ctk.CTkTabview(self.user_panel)
        self.user_content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        self.user_content_frame.columnconfigure(0, weight=1)
        
        for tab_name in self.lp_tabs_names:
            self.user_content_frame.add(tab_name)
            self.user_content_frame.tab(tab_name).columnconfigure((0, 1, 2), weight=1)
            self.user_content_frame.tab(tab_name).columnconfigure(3, weight=0)
        
        ## HABITS TAB
        # NAME
        self.habit_name_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), text=f'{self.lp_user_panel["habit-name"]}', font=self.font_label)
        self.habit_name_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w")

        self.habit_name_entry = ctk.CTkEntry(self.user_content_frame.tab(self.lp_tabs_names[0]), placeholder_text=self.lp_user_panel["habit-ph"])
        self.habit_name_entry.grid(row=1, column=0, columnspan=2, padx=15, pady=0, sticky="we")
        
        # ICON
        self.habit_icon_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), text=f'{self.lp_user_panel["habit-icon"]}', font=self.font_label)
        self.habit_icon_label.grid(row=0, column=2, columnspan=2, padx=10, pady=(5, 0), sticky="w")

        self.habit_icon_combo = ctk.CTkComboBox(self.user_content_frame.tab(self.lp_tabs_names[0]), values=list(self.icons.values()))
        self.habit_icon_combo.grid(row=1, column=2, columnspan=2, padx=15, pady=0, sticky="we")
        
        # START DATE
        self.habit_start_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), text=f'{self.lp_user_panel["habit-start"]}', font=self.font_label)
        self.habit_start_label.grid(row=4, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")

        self.habit_start_combo = ctk.CTkComboBox(self.user_content_frame.tab(self.lp_tabs_names[0]), values=self.MonthDatesList())
        self.habit_start_combo.grid(row=5, column=0, columnspan=4, padx=15, pady=0, sticky="we")
        
        # FREQUENCY
        self.habit_freq_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), text=f'{self.lp_user_panel["habit-freq"]}', font=self.font_label)
        self.habit_freq_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")

        self.habit_freq_slider = ctk.CTkSlider(self.user_content_frame.tab(self.lp_tabs_names[0]), from_=1, to=7, number_of_steps=6)
        self.habit_freq_slider.grid(row=7, column=0, columnspan=3, padx=15, pady=0, sticky="we")
        self.habit_freq_slider.set(1)
        
        self.habit_freq_days_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), text=f'', font=self.font_label)
        self.habit_freq_days_label.grid(row=7, column=3, padx=(0, 10), pady=(5, 0), sticky="w")
        self.habit_freq_slider.configure(command=self.UpdateSliderLabel)
        self.UpdateSliderLabel(self.habit_freq_slider.get())
        
        # QUANTITY OF DAYS
        self.habit_qty_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), text=f'{self.lp_user_panel["habit-qty"]}', font=self.font_label)
        self.habit_qty_label.grid(row=8, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")

        self.habit_qty_entry = ctk.CTkEntry(self.user_content_frame.tab(self.lp_tabs_names[0]), placeholder_text=self.lp_user_panel["habit-qty-ph"])
        self.habit_qty_entry.grid(row=9, column=0, columnspan=4, padx=15, pady=0, sticky="we")
        
        # WEEKEND SKIP
        self.habit_weekend_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), text=f'{self.lp_user_panel["habit-weekend"]}', font=self.font_label)
        self.habit_weekend_label.grid(row=10, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")
        
        self.habit_weekend_segbutton = ctk.CTkSegmentedButton(self.user_content_frame.tab(self.lp_tabs_names[0]), font=self.font_label, values=self.lp_weekends, command=self.UpdateTipLabel)
        self.habit_weekend_segbutton.grid(row=11, column=0, columnspan=4, padx=15, pady=0, sticky="we")
        
        self.habit_tip_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), font=self.font_tip, text_color='gray60')
        self.habit_tip_label.grid(row=12, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="w")
        self.habit_weekend_segbutton.set(self.lp_weekends[-1])
        self.UpdateTipLabel(self.lp_weekends[-1])
        
        # SUBMIT
        self.add_habit_button = ctk.CTkButton(self.user_content_frame.tab(self.lp_tabs_names[0]), text=f'{self.lp_user_panel["habit-add"]}', font=self.font_label, command=self.AddNewHabit)
        self.add_habit_button.grid(row=13, column=0, columnspan=4, padx=200, pady=(10, 5), sticky="we")
        
        # STATUS
        self.status_label = ctk.CTkLabel(self.user_content_frame.tab(self.lp_tabs_names[0]), font=self.font_tip, text='', text_color='gray60')
        self.status_label.grid(row=14, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="w")
    
    
    def AddNewHabit(self) -> None:
        """Processes the data in `habit` form and if it's valid adds it to database as new `habit`.
        """
        spec = '!@#$%^&*()[]{}\'"?,.<>;:\\|'
        test = [char for char in self.habit_name_entry.get() if char in spec]
        name_length = len(self.habit_name_entry.get())
        if test:
            self.status_label.configure(text=self.lp_habit_statuses['name-chars'], text_color='red')
            return
        
        if name_length < 3:
            self.status_label.configure(text=self.lp_habit_statuses['name-short'], text_color='red')
            return
        
        if name_length > 25:
            self.status_label.configure(text=self.lp_habit_statuses['name-long'].replace('X', str(name_length-25)), text_color='red')
            return
        
        try:
            int(self.habit_qty_entry.get())
        except:
            self.status_label.configure(text=self.lp_habit_statuses['qty-type'].replace('X', self.habit_qty_entry.get()), text_color='red')
            return
        
        if int(self.habit_qty_entry.get()) > 365:
            self.status_label.configure(text=self.lp_habit_statuses['qty-big'], text_color='red')
        
        self.habits.Add(
            self.active_user.id,
            self.habit_name_entry.get(),
            list(self.icons.keys())[list(self.icons.values()).index(self.habit_icon_combo.get())],
            self.habit_start_combo.get(),
            int(self.habit_freq_slider.get()),
            int(self.habit_qty_entry.get()),
            self.lp_weekends.index(self.habit_weekend_segbutton.get())
        )

        success = self.lp_habit_statuses['habit-added'].replace('[1]', self.habit_name_entry.get()).replace('[2]', self.habit_start_combo.get()).replace('[3]', str(int(self.habit_freq_slider.get()))).replace('[4]', str(int(self.habit_qty_entry.get())))
        self.status_label.configure(text=success, text_color='lightgreen')
        
        
    def GenerateTasks(self, habit_id: int) -> None:
        """Generates tasks to fulfill based on the parent Habit.

        Args:
            habit_id (int): ID of a Habit to base on.
        """
        habit = self.habits.Get(habit_id)
        tasks = int(habit.quantity)
        match habit.weekends:
            case 2:
                for iteration in range(habit.quantity):
                    self.tasks.Add(self.active_user.id, habit.name, habit.start_date + timedelta(iteration*habit.frequency))
            
            case 1:
                # Work in progress
                
                pass
                    
            case _:
                iteration = 0
                while tasks > 0:
                    iteration += 1
                    current_date =  habit.start_date + timedelta(iteration*habit.frequency)
                    
                    if int(current_date.strftime("%w")) == 6 or int(current_date.strftime("%w")) == 0:
                        continue
                    
                    self.tasks.Add(self.active_user.name, habit.name, current_date)
                    tasks -= 1
                        
    
    def UpdateSliderLabel(self, value: int) -> None:
        """Updates the content of label showing current slider state.

        Args:
            value (int): Value sent from slider.
        """
        if value != 1:
            self.habit_freq_days_label.configure(text=f"{int(value)} {self.lp_user_panel['days']}")
        else:
            self.habit_freq_days_label.configure(text=f"{int(value)} {self.lp_user_panel['day']} ")
    
    
    def UpdateTipLabel(self, value: str) -> None:
        """Updates the label containing discription of currently chosen `Skip Weekend` mode.

        Args:
            value (str): Value of the currently set mode.
        """
        if value == self.lp_weekends[0]:
            self.habit_tip_label.configure(text=self.lp_tips[0])
        elif value == self.lp_weekends[1]:
            self.habit_tip_label.configure(text=self.lp_tips[1])
        else:
            self.habit_tip_label.configure(text=self.lp_tips[2])
            
        
    def ChangeUsername(self) -> None:
        """Changes username if the field is not empty, input is at least 3 characters long, does not contain
        any special character and is not the same as current username.
        """
        if not self.change_username_entry.get():
            self.change_username_status.configure(text=self.lp_user_panel['name-empty'], text_color="red")
            return
        
        if len(self.change_username_entry.get()) < 3:
            self.change_username_status.configure(text=self.lp_user_panel['name-short'], text_color="red")
            return
        
        spec = '!@#$%^&*()[]{}\'"?,.<>;:\\| '
        test = [char for char in self.change_username_entry.get() if char in spec]
        
        if test:
            self.change_username_status.configure(text=self.lp_user_panel['name-chars'], text_color="red")
            return
        
        if self.change_username_entry.get() == self.active_user.name:
            self.change_username_status.configure(text=self.lp_user_panel['name-same'], text_color="red")
            return
        
        self.active_user = self.users.Update('name', self.change_username_entry.get())
        
        self.username_label.configure(text=self.active_user.name)
        self.change_username_status.configure(text=self.lp_user_panel['name-done'], text_color="lightgreen")
        
        
    def ChangePassword(self) -> None:
        """Changes password if the field is not empty, input is at leastn 3 characters long, does not contain
        any special character and is not the same as current password. Password sent to database is encoded with
        sha256 before sending.
        """
        hashed = hash.sha256(self.change_password_entry.get().encode()).hexdigest()
        
        if not self.change_password_entry.get():
            self.change_password_status.configure(text=self.lp_user_panel['pass-empty'], text_color="red")
            return
        
        if len(self.change_password_entry.get()) < 8:
            self.change_password_status.configure(text=self.lp_user_panel['pass-short'], text_color="red")
            return
        
        spec = '!@#$%^&*()[]{}\'"?,.<>;:\\| '
        test = [char for char in self.change_password_entry.get() if char in spec]
        if test:
            self.change_password_status.configure(text=self.lp_user_panel['pass-chars'], text_color="red")
            return
        
        if hashed == self.active_user.password:
            self.change_password_status.configure(text=self.lp_user_panel['pass-same'], text_color="red")
            return
        
        self.active_user = self.users.Update('password', hashed)

        self.change_password_status.configure(text=self.lp_user_panel['pass-done'], text_color="lightgreen")
    
        
    def ChangeLanguage(self) -> None:
        """Change language in database, user's settings and apply change.
        """
        match self.languages_names.index(self.change_language_combo.get()):
            case 0:
                chosen = 'pl'
            case _:
                chosen = 'en'
        
        self.active_user = self.users.Update('language', chosen)
        self.ForceRefresh()
        
        
    def ChangeShortcuts(self, state: str) -> None:
        """Change setting of day names length in database, user's setting and applies the change.

        Args:
            state (str): State of setting - `ON` or `OFF`.
        """
        self.active_user = self.users.Update('shorts', self.off_on.index(state))
        self.ForceRefresh()
        
        
    def ChangeTheme(self) -> None:
        """Changes theme in database, user's setting and applies change.
        """
        if not self.themes_colors.index(self.change_theme_combo.get()):
            chosen = 'blue'
        else:
            chosen = 'green'
            
        self.active_user = self.users.Update('theme', chosen)
        ctk.set_default_color_theme(chosen)
        self.ForceRefresh()
        
    
    def ChangeMode(self, state: str) -> None:
        """Changes mode in database, user's setting and applies change.
        """
        match self.modes.index(state):
            case 0:
                chosen = 'light'
            case 1:
                chosen = 'dark'
            case _:
                chosen = 'default'
            
        self.active_user = self.users.Update('mode', chosen)
        
        if chosen == 'default':
            chosen = 'system'
        ctk.set_appearance_mode(chosen)
        self.user_panel.destroy()
            
            
    def MonthDatesList(self) -> list:
        """Creates a list of dates in current month.

        Returns:
            list: All the dates.
        """
        current = date(date.today().year, date.today().month, 1)
        dates = []
        while current.month == date.today().month:
            dates.append(current.strftime('%d.%m.%Y'))
            current += timedelta(1)
        return dates
            
        
    def ForceRefresh(self) -> None:
        """Destroying interface object to rebuild it with new settings applied.
        """
        self.destroy()
        self.__init__()
        self.mainloop()
        INSTANCES[0].quit()
    
    
    def OnClose(self) -> None:
        """Defines all actions to be done before closing the app.
        """
        self.db.close()
        self.quit()
        
    
if __name__ == "__main__":
    app = Main()
    INSTANCES.append(app)
    app.mainloop()
