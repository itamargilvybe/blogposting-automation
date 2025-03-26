import os
from dotenv import load_dotenv
import json

load_dotenv()

# Google Sheets
GSPREAD_CREDS_JSON_NAME = os.environ["GOOGLE_CREDENTIALS_FILE_NAME"]

GSPREAD_CREDS_JSON = os.environ["GOOGLE_CREDENTIALS_JSON"]

# OpenAI
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Sanity
SANITY_PROJECT_ID = os.environ["SANITY_PROJECT_ID"]
SANITY_DATASET = os.environ["SANITY_DATASET"]
SANITY_TOKEN = os.environ["SANITY_TOKEN"]
BLOG_BASE_URL = os.environ["BLOG_BASE_URL"]
BLOG_SITEMAP_URL = os.environ["BLOG_SITEMAP_URL"]
MODAL_APP_NAME = os.environ["MODAL_APP_NAME"]

PROMPTLAYER_API_KEY = os.environ["PROMPTLAYER_API_KEY"]