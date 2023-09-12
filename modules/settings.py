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
        tree = ET.parse(f'./modules/lang/{lang}.xml')
        root = tree.getroot()
        
        main = [set.text for set in root.find('main')]
               
        days = root.find('days')
        short_days = [day.text for day in days.find('short')]
        full_days = [day.text for day in days.find('full')]
        
        pack = [main, short_days, full_days]
        return pack
            

def SaveChanges(section: str, setting: str, value):
    cfg.set(section, setting, value)
    with open('./modules/config.cfg', 'w') as configfile:
        cfg.write(configfile)
        
