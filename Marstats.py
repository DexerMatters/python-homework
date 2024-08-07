import gradio as gr
import requests


DEFAULT_API_KEY = "SMuoFVWDjpQRpM6aZwEwhfUXTFphCe3bXnyI9fRD"

CAMERAS = ["all", "FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"]

URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"


inputs = [
  gr.Textbox(
    label="API key", 
    value=DEFAULT_API_KEY,
    info = "The default key is provided by Dexer's own."
  ),
  gr.Number(
    label="Sol",
    info="Martian solar day."
  ),
  gr.Slider(label='Pages', minimum=1, maximum=20, value=1, step=1),
  gr.Dropdown(label="Camera", choices=CAMERAS, value="MAST")
]

outputs = [
  gr.Text(label="Stats:"),
  gr.Gallery(label="Photographs")
]


def get_response(api_key, sol, page, cam):
  params = {
    'api_key': api_key,
    'sol': sol,
    'camera': cam,
    'page': page
  }

  response = requests.get(URL, params)
  stats = "Network Error."

  if response.status_code == 200:
    photos = response.json().get('photos', [])
    photo_urls = [photo['img_src'] for photo in photos]
    stats = "Photo captured."

    if photo_urls == []:
      stats = "There doesn't seem to be any photos in your query."

    print(stats)
    return stats, photo_urls

  print(stats)
  return stats, []


gr.Interface(
  fn=get_response, 
  inputs=inputs, 
  outputs=outputs
).launch()