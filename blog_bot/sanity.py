import requests
import json
import datetime
from datetime import timezone
from config import SANITY_TOKEN, SANITY_PROJECT_ID, SANITY_DATASET
from .utils import save_debug_data

def upload_image_to_sanity(image_bytes):
    print("\n=== Uploading Image to Sanity ===")

    headers = {
        "Authorization": f"Bearer {SANITY_TOKEN}",
        "Content-Type": "image/png"
    }

    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/assets/images/{SANITY_DATASET}?filename=generated.png"

    response = requests.post(url, headers=headers, data=image_bytes)

    print("Response status:", response.status_code)
    print("Response body:", response.text)

    if response.status_code != 200:
        print("Error uploading image")
        return None

    result = response.json()
    asset_id = result['document']['_id']
    print(f"✅ Image uploaded successfully. Asset ID: {asset_id}")
    return asset_id

def fetch_author_id():
    print("\n=== Fetching Author ID ===")
    query = '*[_type == "author" && name == "Itamar Gil"][0]{ _id }'
    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/data/query/{SANITY_DATASET}"
    headers = {"Authorization": f"Bearer {SANITY_TOKEN}"}
    params = {"query": query}

    try:
        print("Querying Sanity for author...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        result = response.json()
        if not result.get('result'):
            print("Warning: No author found with name 'Itamar Gil'")
            return None
            
        author_id = result['result']['_id']
        print(f"Successfully found author ID: {author_id}")
        return author_id
    except requests.exceptions.RequestException as e:
        print(f"Error fetching author ID: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in fetch_author_id: {e}")
        return None

def post_to_sanity(blog_data, asset_id):
    print("\n=== Publishing to Sanity ===")
    print(f"Title: {blog_data['title']}")
    
    # Save debug data
    save_debug_data(blog_data, asset_id)
    
    # Fetch author ID
    author_id = fetch_author_id()
    if not author_id:
        print("Error: Could not proceed without author ID")
        return False

    # Prepare mutation in Sanity's expected format
    mutation = {
        "mutations": [{
            "create": {
                "_type": "post",
                "title": blog_data['title'],
                "slug": {"current": blog_data['title'].lower().replace(' ', '-')},
                "publishedAt": datetime.datetime.now(timezone.utc).isoformat(),
                "author": {"_type": "reference", "_ref": author_id},
                "metaTitle": blog_data['meta_title'],
                "metaDescription": blog_data['meta_description'],
                "body": blog_data['content'],
                "mainImage": {
                    "_type": "image",
                    "asset": {"_type": "reference", "_ref": asset_id}
                }
            }
        }]
    }

    try:
        headers = {
            "Authorization": f"Bearer {SANITY_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/data/mutate/{SANITY_DATASET}?returnIds=true"
        print("Sending mutation:", json.dumps(mutation, indent=2))
        response = requests.post(url, headers=headers, json=mutation)
        print("Response status:", response.status_code)
        print("Response body:", response.text)
        response.raise_for_status()

        result = response.json()
        print(f"Success! Post ID: {result.get('results', [{}])[0].get('id', 'Unknown')}")
        print(f"Blog post '{blog_data['title']}' published successfully!")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error publishing to Sanity: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response details: {e.response.text}")
        return False
    except Exception as e:
        print(f"Unexpected error in post_to_sanity: {e}")
        return False
