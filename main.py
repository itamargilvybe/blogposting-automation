from blog_bot.utils import *
from blog_bot.sheets import get_unused_keyword, mark_keyword_used
from blog_bot.generate import generate_blog_post, generate_image
from blog_bot.sanity import post_to_sanity
import json
import modal
import os
from config import MODAL_APP_NAME

app = modal.App(MODAL_APP_NAME)

# Create image with required packages
image = modal.Image.debian_slim().pip_install(
    "google-auth",
    "google-auth-oauthlib",
    "google-auth-httplib2",
    "google-api-python-client",
    "gspread",
    "oauth2client",
    "openai",
    "python-dotenv",
    "beautifulsoup4",
    "requests",
    "lxml",
    "promptlayer"
)

# @app.function(image=image)
def test():
    print("hey")

# @app.function(image=image, secrets=[modal.Secret.from_name("custom-secret")], schedule=modal.Cron("0 4 * * *"))
def daily_blog_post():
    try:
        print("Starting daily blog automation...")

        keyword = get_unused_keyword()

        print(f"Generating blog post for keyword: {keyword}")

        if keyword:
            blog_data = generate_blog_post(keyword)
            print(blog_data)
            print("Generating image...")
            
            asset_id = generate_image(blog_data['image_prompt'])

            print("Posting to Sanity...")
            
            success = post_to_sanity(blog_data, asset_id)

            if success:
                print(f"Published: {keyword}")
                mark_keyword_used(keyword)
                print("Done ✅")
            else:
                print(f"Failed publishing: {keyword}")
        else:
            print(f"No keywords to process")
    except Exception as e:
        print(f"Error occurred: {e}")

def test_utils():
    try:
        # Get latest debug files
        json_file = get_latest_debug_files()
        if not json_file:
            print("Could not find debug files")
            return
        # Read blog data
        with open(json_file, 'r', encoding='utf-8') as f:
            blog_data = json.load(f)
            
        asset_id = "image-f6ede5c0c0792f070843dfe9162e32246bbc103e-1792x1024-png"

        post_to_sanity(blog_data, asset_id)
        
        print("Done ✅")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    daily_blog_post()
    # test_utils()

# @app.local_entrypoint()
# def main():
#     print("Scheduled function is set up and will run at 4:00 AM UTC daily")