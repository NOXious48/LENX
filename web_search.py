import torch
import pandas as pd
from transformers import BlipProcessor, BlipForConditionalGeneration
from duckduckgo_search import DDGS

def image_to_text(image_path):
    # Load the BLIP model and processor
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

    # Load and preprocess the image
    image = Image.open(image_path)

    # Preprocess the image and generate caption
    inputs = processor(image, return_tensors="pt").to(device)
    with torch.no_grad():
        generated_ids = model.generate(**inputs)

    # Decode the generated caption
    caption = processor.decode(generated_ids[0], skip_special_tokens=True)
    print(caption)
    return caption

# Define the function for web search using ContextualWebSearch API
""" 
Args:
keywords: keywords for query.
# https://duckduckgo.com/duckduckgo-help-pages/settings/params/
region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
safesearch: on, moderate, off. Defaults to "moderate".
timelimit: d, w, m, y. Defaults to None.
backend: api, html, lite. Defaults to api.
api html collect data from https://duckduckgo.com, collect data from https://html.duckduckgo.com,
lite collect data from https://lite.duckduckgo.com.
max_results: max number of results. If None, returns results only from the first response. Defaults to None.
"""
def perform_web_search(query):

    results=DDGS().text(
        keywords=query,
        region='in-en',
        safesearch='off',
        timelimit=None,
        max_results=50
    )
    results_df=pd.DataFrame(results)
    return results_df
