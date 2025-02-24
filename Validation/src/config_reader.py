import configparser
import os

class ConfigReader:
    def __init__(self, file_path=None):
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), "../config/config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(file_path)

    def get(self, section, key):
        try:
            return self.config.get(section, key)
        except configparser.NoOptionError:
            print(f"Error: No option '{key}' found in section '{section}'")
            return None
        except configparser.NoSectionError:
            print(f"Error: No section '{section}' found in config file")
            return None

# Example usage
if __name__ == "__main__":
    config = ConfigReader()
    print("SELENIUM Configurations:")
    for key, value in config.config.items("SELENIUM"):
        print(f"{key} = {value}")

    print("\nCREDENTIALS Configurations:")
    for key, value in config.config.items("CREDENTIALS"):
        print(f"{key} = {value}")
