import os
from pathlib import Path
from os.path import join
from dotenv import load_dotenv


dotenv_path = join(Path(__file__).parent.absolute(), '.env')
load_dotenv(dotenv_path)
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']