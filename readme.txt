I'm using this automation to post blog articles daily.

deploy to modal:
modal deploy: --name <function name> <file name>
Example: modal deploy --name daily_blog_post main.py                            

Run locally:
python3 main.py

Install dependencies:
1. Add them to requirements.txt
2. Run: python3 -m pip install -r requirements.txt

Notes:
- Make sure that you're adding an .env file (based on .env.sample file)
- Remember to add the secrets in the Modal app
- Remeber to give the Google Service account sheet editing permissions for the keywords spreadsheet