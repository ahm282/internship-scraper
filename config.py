# config.py
import dotenv

# load environment
dotenv.load_dotenv()

# Browser binaries
CHROME_BINARY = "/usr/bin/chromium"
CHROMEDRIVER_PATH = "chromedriver"

# URLs
BASE_URL = "https://stages.thomasmore.be/"
PORTAL_URL = BASE_URL + "Studentenportaal/Stagevoorkeur/Stagevoorkeur.aspx"

# cookies file
COOKIES_FILE = "cookies.json"
