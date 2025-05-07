from promptlayer import PromptLayer
import openai
import json
import base64
from config import OPENAI_API_KEY, PROMPTLAYER_API_KEY
from .sitemap import get_blog_urls_from_sitemap
from .utils import format_blog_url_list_for_prompt
from .sanity import upload_image_to_sanity

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY
pl_client = PromptLayer(api_key=PROMPTLAYER_API_KEY)
OpenAI = pl_client.openai.OpenAI

def generate_blog_post(keyword):
    try:
        print("Starting blog post generation for keyword:", keyword)

        valid_blog_links = get_blog_urls_from_sitemap()
        formatted_links = format_blog_url_list_for_prompt(valid_blog_links)

        print("Fetched all available MindCheck URLs from sitemap")

        # STEP 1: Generate the blog post
        prompt_name = "MINDCHECK_BLOG_STEP1"
        input_variables = {"keyword": keyword, "formatted_links": formatted_links}
        template = pl_client.templates.get(prompt_name, {"input_variables": input_variables})
        prompt = template['llm_kwargs']['messages'][1]['content'][0]['text']
        system_prompt = template['llm_kwargs']['messages'][0]['content']

        print("Prompt:", prompt)

        print("Sending request to OpenAI...")
        
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            pl_tags=["blog-generation"]
        )
        print("Got response from OpenAI")
        
        # Get the content and parse it as JSON
        content = response.choices[0].message.content
        print("Raw content:", content)

        # STEP 2: Generate the structured response
        prompt_name = "MINDCHECK_BLOG_STEP2"
        input_variables = {"plain_article": content}
        template = pl_client.templates.get(prompt_name, {"input_variables": input_variables})
        prompt = template['llm_kwargs']['messages'][1]['content'][0]['text']
        system_prompt = template['llm_kwargs']['messages'][0]['content']

        print("Sending request to OpenAI...")
        
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            pl_tags=["blog-generation"]
        )
        print("Got response from OpenAI")
        
        # Get the content and parse it as JSON
        content = response.choices[0].message.content
        print("Structured response:", content)
        
        try:
            # Try to find JSON in the content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                print("Found JSON string:", json_str)
                return json.loads(json_str)
            else:
                print("No JSON found in response")
                return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
            
    except Exception as e:
        print(f"Error generating blog post: {e}")
        return None
    
def generate_image(image_prompt):
    try:
        print("Starting image generation for prompt:", image_prompt)
        client = openai.OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1792x1024",
            response_format="b64_json"
        )
        print("Got response from OpenAI")
        image_b64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_b64)
        asset_id = upload_image_to_sanity(image_bytes)
        return asset_id
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
