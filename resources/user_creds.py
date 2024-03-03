import os
from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    EMAIL = ""
    USERNAME = ""
    PASSWORD = os.getenv('SUPER_ADMIN_TOKEN')
