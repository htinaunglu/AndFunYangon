import os
import requests as req
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup

google_image = 'https://www.google.com/search?tbm=isch&q='
keyword = input('Enter Keyword ')
n_images = int(input('Enter image count '))
user_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

saved_folder = './images/' + keyword


def main():
    if not os.path.exists(saved_folder):
        os.mkdir(saved_folder)
    download_images()
    convert_csv()

def download_images():
    search_url = google_image + keyword

    response = req.get(search_url, headers=user_agent)

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    count = 1
    links = []
    for result in results:
        try:
            link = result['data-src']
            links.append(link)
            count += 1
            if(count > n_images):
                break

        except KeyError:
            continue

    print(f"Downloading {len(links)} images")

    for i, link in enumerate(tqdm(links,desc = "Download in Progress")):
        response = req.get(link)

        image_name = saved_folder + '/' + keyword +"-"+ str(i+1) + '.jpg'

        with open(image_name, 'wb') as fh:
            fh.write(response.content)
    print(f"Download done check the images in {(saved_folder)}")

def convert_csv():
    the_list = os.listdir(saved_folder)
    list_df = pd.DataFrame(the_list)
    list_df.to_csv(saved_folder+"/search_list.csv", index = None)
    print(f"Image csv file is in {(saved_folder)}/search_list.csv")


if __name__ == "__main__":
    main()