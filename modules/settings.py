import configparser

cfg = configparser.ConfigParser()
cfg.read('./modules/config.cfg')

LANGUAGE = cfg.get('Main', 'language')
RES = cfg.get('Main', 'resolution')
SCALE = cfg.getfloat('Main', 'scaling')
FONT = cfg.get('Main', 'font')
SHORTCUTS = cfg.getboolean('Main', 'shortcuts')
THEME = cfg.get('Main', 'theme')
MODE = cfg.get('Main', 'mode')
VER = 'ver. 1.0.10'

def SaveChanges(section: str, setting: str, value) -> None:
    """Save changes made by user to the config file.

    Args:
        section (str): Section in config file.
        setting (str): Setting's name in the config file.
        value (_type_): The value of setting user want's to set.
    """
    cfg.set(section, setting, value)
    with open('./modules/config.cfg', 'w') as configfile:
        cfg.write(configfile)
