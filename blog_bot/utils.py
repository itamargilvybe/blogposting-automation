import datetime
import os
import json
import glob

def save_debug_data(blog_data, image_bytes):
    try:
        # Create debug directory if it doesn't exist
        os.makedirs('debug', exist_ok=True)
        
        # Save blog data as JSON
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = f'debug/blog_data_{timestamp}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(blog_data, f, indent=2, ensure_ascii=False)
        print(f"Saved blog data to {json_path}")
        
        # Save image
        image_path = f'debug/image_{timestamp}.png'
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
        print(f"Saved image to {image_path}")
        
        return True
    except Exception as e:
        print(f"Error saving debug data: {e}")
        return False

def format_blog_url_list_for_prompt(urls):
    return "\n".join([f"- {url}" for url in urls])

def get_latest_debug_files():
    # Get the most recent JSON file
    json_files = glob.glob('debug/blog_data_20250324_151006.json')
    if not json_files:
        print("No debug files found")
        return None, None
    
    latest_json = max(json_files, key=os.path.getctime)
    print(f"Using debug file: {latest_json}")
    
    return latest_json
