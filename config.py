import configparser

def generate_config():
  # CREATE OBJECT
  cfg = configparser.ConfigParser() 

  cfg.add_section("PATH")
  cfg.set("PATH", "tesseract", "C:\\Program Files\\Tesseract-OCR\\tesseract.exe")


  cfg.add_section("General")
  cfg.set("General", "WindowName", "Nitem Client")
  cfg.set("General", "Resolution", "1280x720")


  # SAVE CONFIG FILE
  with open(r"configurations.ini", 'w') as configfileObj:
      cfg.write(configfileObj)
      configfileObj.flush()
      configfileObj.close()

def read_config():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config

def init_config():
  generate_config()
  return read_config()