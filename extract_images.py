from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC



from bs4 import BeautifulSoup
# import requests



if __name__=="__main__":
    species = [("Esparrall", 34841)]
    speciesToImg={}

    for name, taxon_id in species:
        print(f"Scraping images for {name} with taxon_id: {taxon_id}")
        user = "xasalva"
        taxon_id = str(taxon_id)
        base_url = f"https://minka-sdg.org/lifelists/{user}?details_view=observations&taxon_id={taxon_id}"
        obs_base_url = "https://minka-sdg.org/"
        print(f"Parsing: {base_url}...\n")

        driver = webdriver.Chrome()
        driver.get(base_url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ObservationsGridCell')))

        html = driver.page_source
    
        soup = BeautifulSoup(html, 'html.parser')

        observations = []
        print("Retrieved these observations: ")
        for n in soup.find_all('a'):
            if(n.get('href').startswith( "/observations/")):
                observation_url = obs_base_url + n.get('href')
                observations.append(observation_url)

        images = []
        for observation_url in list(set(observations))[:10]:
            print(observation_url)
            driver.get(observation_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'image-gallery-image')))
            
            html = driver.page_source
            soup_obs = BeautifulSoup(html, 'html.parser')
            # Find the div with class "image-gallery-image"
            image_div = soup_obs.find('div', class_=lambda x: x and 'image-gallery-image' in x)


            # Find the img tag within this div"<div></div>"
            img_tag = image_div.find('img') if image_div else None

            # Extract the 'src' attribute (the image URL)
            img_url = img_tag['src'] if img_tag else None
            images.append(img_url)
            print(img_url)
        speciesToImg[name]=images
    print(speciesToImg)