from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC



from bs4 import BeautifulSoup
# import requests



if __name__=="__main__":
    species = [("Llissa Vera", 250654), ("Orada", 68960), ("Mabre", 48596),("Sarg", 12553),
    ("Esparrall", 34841),("Verada",34798),("Oblada",240400),("Salpa",34805),("Boga",246899),
    ("Aranyó",245401),("Moll de roca",35125),("Escórpora",34965),("Serrà",13755),("Anfós",246069),
    ("Vaca serrana",13765),("Joell",240394),("LLobarro",34837),("Xucladits",243584),("Castanyoletes",35225),("Fadrí",35194),("Juliola",34835),("Espatarc",35216 ),("Planxeta",34986),("Roqueret",240397),("Tacó",35282)]
    speciesToImg={}

    for name, taxon_id in species[:10]:
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
        for observation_url in list(set(observations))[:5]:
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