import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



Rangliste = []


def all_pages(pages):
    """Mit dieser Funktion werden die vorhandenen sieben Seiten der Youtube-Charts All-time gescrapted."""
    for Seite in range(1, 8):
        myheader = {"User Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
        url1 = "https://imvdb.com/charts/all"
        page = "?page="
        #Zusammen mit myheader, url1 und page wird jeweils eine neue Seite angefragt. Mit Variable Seite werden die jeweiligen Seitenzahlen generiert.
        response = requests.get(url1 + page + str(Seite), headers=myheader)
        #print(response)
        soup = BeautifulSoup(response.text, "html.parser")
        charts = soup.find_all("tr")   #Innerhalb einer Seite sind alle relevanten Inhalte im tr Tag
        for eintrag in charts:
            artist = eintrag.find("p", "href" == True).text.strip() #Hier werden die Künstler/innen pro Eintrag gesucht
            song_title = eintrag.find("p").a.text.split("\n")[-1].strip() #Hier wird der Song gesucht
            #print(song_title)
            director = eintrag.find("p", class_="node_info") #Bei manchen Songs war ein Director zuständig für den Videoclip für andere war keiner erwähnt
            if director != None:
                director = director.text.split(":")[1:] #Hier wurde der Präfix Director: ausgeschnitten
                director = director[0].strip()
                #print(director)
            else:
                director = "No director" #Dieser Eintrag erleichterte die Übersicht später bei der Bearbeitung des csv-Files
            views_on_youtube = eintrag.find("span", attrs={"class": "viewsCount"}).text.strip() #Hier wird Anzahl der Youtube-Views gesucht
            #Hier werden die vorhandenen Strings in einem Dictionary zusammengeführt
            eintrag_dict = {"Artist": artist, "Song titel": song_title, "Director": director, "Views auf Youtube": views_on_youtube}
            #Das Dictionary wird nun in die Liste Rangliste hinzugefühgt
            Rangliste.append(eintrag_dict)
        #Hier kann beobachtet werden, ob pro Seite wirklich 40 Einträge gescrapt werden, als kleine Kontrolle
        print(len(Rangliste))
        time.sleep(3) #Damit die Seite nicht überlastet wird, wird eine kleine Pause zwischen den Loops definiert

        #Aus der Liste wird nun ein Dataframe und anschliessend ein csv-File
        df = pd.DataFrame(Rangliste)
        df.to_csv("Hubacher_Lars_src.csv", header=True)

all_pages(Rangliste)