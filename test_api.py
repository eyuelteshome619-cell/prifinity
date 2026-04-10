import sys
import os

sys.path.append(os.path.abspath('backend'))
from app.services.media_api import MediaAPIService
from app.utils.database import execute_query

def test():
    print("Testing Spotify...")
    # I can't test because I don't have their keys
    pass
