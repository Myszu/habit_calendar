import xml.etree.ElementTree as ET

class Language():    
    def LoadLangpack(self, lang: str) -> list:
        """Loads a XML language pack from `lang` folder.

        Args:
            lang (str): Short code of chosen language.

        Returns:
            list: Words included in the interface.
        """
        tree = ET.parse(f'./modules/lang/{lang}.xml')
        root = tree.getroot()
        
        main = {record.tag: record.text for record in root.find('main')}
        user_panel = {record.tag: record.text for record in root.find('user')}
        weekends = [tab.text for tab in root.find('user').find('weekends')]
        tips = [tab.text for tab in root.find('user').find('tips')]
        tabs = [tab.text for tab in root.find('user').find('tabs')]
        settings = {record.tag: record.text for record in root.find('settings')}
        
        languages_names = [record.text for record in root.find('languages')]
               
        days = root.find('days')
        short_days = [day.text for day in days.find('short')]
        full_days = [day.text for day in days.find('full')]
        
        pack = [main, user_panel, weekends, tips, tabs, settings, languages_names, short_days, full_days]
        return pack
