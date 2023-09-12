import configparser
import xml.etree.ElementTree as ET

cfg = configparser.ConfigParser()
cfg.read('./modules/config.cfg')

LANGUAGE = cfg.get('Main', 'language')
RES = cfg.get('Main', 'resolution')
SCALE = cfg.getfloat('Main', 'scaling')
FONT = cfg.get('Main', 'font')

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
        
        main = [set.text for set in root.find('main')]
               
        days = root.find('days')
        short_days = [day.text for day in days.find('short')]
        full_days = [day.text for day in days.find('full')]
        
        pack = [main, short_days, full_days]
        return pack
            

def SaveChanges(section: str, setting: str, value):
    """Save changes made by user to the config file.

    Args:
        section (str): Section in config file.
        setting (str): Setting's name in the config file.
        value (_type_): The value of setting user want's to set.
    """
    cfg.set(section, setting, value)
    with open('./modules/config.cfg', 'w') as configfile:
        cfg.write(configfile)
