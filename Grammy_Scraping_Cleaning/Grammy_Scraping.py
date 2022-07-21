from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

url_list_grammy = ['https://www.grammy.com/grammys/awards/63rd-annual-grammy-awards-2020',
                   'https://www.grammy.com/grammys/awards/62nd-annual-grammy-awards-2019',
                   'https://www.grammy.com/grammys/awards/61st-annual-grammy-awards-2018',
                   'https://www.grammy.com/grammys/awards/60th-annual-grammy-awards-2017',
                   'https://www.grammy.com/grammys/awards/59th-annual-grammy-awards-2016',
                   'https://www.grammy.com/grammys/awards/58th-annual-grammy-awards-2015',
                   'https://www.grammy.com/grammys/awards/57th-annual-grammy-awards-2014',
                   'https://www.grammy.com/grammys/awards/56th-annual-grammy-awards-2013',
                   'https://www.grammy.com/grammys/awards/55th-annual-grammy-awards-2012',
                   'https://www.grammy.com/grammys/awards/54th-annual-grammy-awards-2011',
                   'https://www.grammy.com/grammys/awards/53rd-annual-grammy-awards-2010',
                   'https://www.grammy.com/grammys/awards/52nd-annual-grammy-awards-2009',
                   'https://www.grammy.com/grammys/awards/51st-annual-grammy-awards-2008',
                   'https://www.grammy.com/grammys/awards/50th-annual-grammy-awards-2007',
                   'https://www.grammy.com/grammys/awards/49th-annual-grammy-awards-2006',
                   'https://www.grammy.com/grammys/awards/48th-annual-grammy-awards',
                   'https://www.grammy.com/grammys/awards/47th-annual-grammy-awards-2004',
                   'https://www.grammy.com/grammys/awards/46th-annual-grammy-awards-2003',
                   'https://www.grammy.com/grammys/awards/45th-annual-grammy-awards-2002',
                   'https://www.grammy.com/grammys/awards/44th-annual-grammy-awards-2001',
                   'https://www.grammy.com/grammys/awards/43rd-annual-grammy-awards-2000']

def grammy_winner(url_list):
    '''Bei der Funktion grammy_winner handelt es sich um eine Funktion, welche die Gewinner der
    Grammy-Awards von der offiziellen Internetseite scrapt. Die Funktion benötigt 1 Argument.
    Es handelt sich dabei um eine Liste der URL's der Grammys, die gescrapt werden sollen. Diese Liste
    ist in absteigender Reihenfolge zu halten. Beispiel: url_list = ['url_grammy_2021', 'url_grammy_2020',...]'''
    count_year = 2021

    #Hierbei handelt es sich um den "Haupt"-Loop. Das Programm wird für jede URL in der übergebenen Liste druchlaufen.
    for url in url_list:
        #Der count_year wird später für die Abspeicherung der einzelnen Daten benötigt.
        count_year -= 1

        #der html-text wird in einer Variabel gespeichert
        html_txt = requests.get(url).text
        soup = BeautifulSoup(html_txt,'lxml')
        #Die benötigten html-Elemente werden in eine Variabel gespeichert
        grammys = soup.find_all('div', class_ = 'view-grouping')


        #Die Variabel Grammys enthält nun sämtliche benötigten Elemente. Im nächsten Schritt werden
        #Listen erstellt, welche nach den gewünschten Informationen benennt werden. Über diese Listen
        # werden nun die HTML-Elemente triagiert.
        #categories:    Enthält sämtliche vergebenen Kategorien in diesem Jahr
        #winner:        Enthält die Gewinner der einzelnen Kategorien in diesem Jahr. Wichtig es kann sich bei
        #               diesem Feld um Song-Titel oder Künstler/-innen Namen handeln.
        #Producer:      Aufgrund des Aufbaus der Webseite sind die Gewinner der Kategorien nicht immer im gleichen
        #               HTML-Element. Sobald ein Producer oder eine Gruppe von Künstler den Award gewonnen hat,
        #               steht dieses in einem anderen HTML-Element. Diese werden in der Liste Producer gesammelt.
        #Overall:       Diese Liste wird benötigt, um die gesammelten Daten am Schluss zu vereinigen und in ein
        #               umfassendes csv-File zu laden.
        categories = []
        winner = []
        #songs = []
        producer = []
        overall = []

        #Im nachfolgenden for-Loop wird das Grammy-File aufgeteilt, und die sich darin befindenden
        #HTML-Elemente auf die zuvor erstellten Listen verteilt.
        for grammy in grammys:
            categories.append(grammy.find('div', class_ = "view-grouping-header").text)
            winner.append(grammy.find('div', class_ = "wrapper views-fieldset"))
            producer.append(grammy.find("div", class_ = "fieldset-wrapper"))

            #Hier wird die Kategorie rausgeschält
            for category in categories:
                category

            #Hier wird der Song-Name rausgeschält
            for song_title in winner:
                song = song_title.find("div", class_ = "views-field views-field-title").find("span", class_ = "field-content").text

            #Hier wird der Künstler/innen-Name, aus der Liste winner rausgeschält
            #Zu beachten ist, dass es Felder gibt, welche kein Inhalt haben. Diese werden dann als "" (NaN)
            #in die Liste übergeben
            for artist_name in winner:
                artist = artist_name.find("div", class_ = "views-field views-field-field-description").find("div", class_ = "field-content").text.strip('\n')
                # print(artist2)
                if artist != "":
                    artist
                else:
                    artist = ""

            #Hier wird der Künstler/innen-Name aus der Liste producer rausgeschält
            #Zu beachten ist, dass grundsätlich davon auszugehen ist, dass dieses Feld leer ist. Sofern jedoch
            #der artist vom vorherigen Loop leer ist, wird hier dieses Feld mit dem Eintrag artist2 gemacht.
            for artist_name2 in producer:
                artist2 = ""
                if artist == "":
                    artist2 = artist_name2.find("div", class_ = "field-content").text.strip('\n')
                    # print(artist2)

            #Die gewonnenen Daten werden zu einem Dictionary zusammengefügt und in die Liste overall eingefügt.
            artist_song_dict = {"category": category, "Song titel": song, "artist": artist, "artist2": artist2}
            overall.append(artist_song_dict)

        #Damit die Website nicht überlastet wird
        time.sleep(3)

        #Aus der Liste Overall wird ein DataFrame erstellt
        df_grammy = pd.DataFrame(overall)
        #Das DataFrame wird als csv abgespeichert. WICHTIG: Dies wird nun für jede URL (eine URL pro Jahr)
        # gemacht und somit eine csv-Datei für jedes Jahr erstellt.
        df_grammy.to_csv("grammy_" + str(count_year) + "_t" + ".csv", index=False, header=True)
    return
#should work
grammy_winner(url_list_grammy)

#Als nächstes wird aus den erstellten csv-Dateien ein DataFrame erstellt, welches dann an die Bereinigung im
#Jupyter Notebook weitergegeben werden kann.

#Zuerst werden die einzelnen csv-Datein geladen
grammy00 = pd.read_csv('grammy_2000_t.csv')
grammy01 = pd.read_csv('grammy_2001_t.csv')
grammy02 = pd.read_csv('grammy_2002_t.csv')
grammy03 = pd.read_csv('grammy_2003_t.csv')
grammy04 = pd.read_csv('grammy_2004_t.csv')
grammy05 = pd.read_csv('grammy_2005_t.csv')
grammy06 = pd.read_csv('grammy_2006_t.csv')
grammy07 = pd.read_csv('grammy_2007_t.csv')
grammy08 = pd.read_csv('grammy_2008_t.csv')
grammy09 = pd.read_csv('grammy_2009_t.csv')
grammy10 = pd.read_csv('grammy_2010_t.csv')
grammy11 = pd.read_csv('grammy_2011_t.csv')
grammy12 = pd.read_csv('grammy_2012_t.csv')
grammy13 = pd.read_csv('grammy_2013_t.csv')
grammy14 = pd.read_csv('grammy_2014_t.csv')
grammy15 = pd.read_csv('grammy_2015_t.csv')
grammy16 = pd.read_csv('grammy_2016_t.csv')
grammy17 = pd.read_csv('grammy_2017_t.csv')
grammy18 = pd.read_csv('grammy_2018_t.csv')
grammy19 = pd.read_csv('grammy_2019_t.csv')
grammy20 = pd.read_csv('grammy_2020_t.csv')


#Die csv-Dateien werden zu einem DataFrame zusammengeschlossen. Dies passiert über den concat-Befehl
#Als Keys werden die einzelnen Jahre für pro DataFrame verwendet.
df_grammy_since2000 = pd.concat([grammy20,grammy19,grammy18,grammy17,grammy16,grammy15,grammy14,
                                 grammy13,grammy12,grammy11,grammy10,grammy09,grammy08,
                                 grammy07,grammy06,grammy05,grammy04,grammy03,grammy02,
                                 grammy01,grammy00], keys=['2020','2019','2018','2017',
                                                           '2016','2015','2014','2013',
                                                           '2012','2011','2010','2009',
                                                           '2008','2007','2006','2005',
                                                           '2004','2003','2002','2001',
                                                           '2000'])

#Zum Abschluss wird für die Weitergehende Bearbeitung im Jupyter-Notebook noch die Struktur des DataFrames
#angepasst.
#Dafür wird für jeden Award ein eigenes DataFrame erstellt. Dies ermöglicht eine vereinfachte Kontrolle.
#ob die einzelnen Kategorien korrekt gescrapt wurden. Gemacht wird dies mit dem .drop()-Befehl.
indexNames = df_grammy_since2000[df_grammy_since2000['category'] != 'Record Of The Year'].index
df_grammy_Record = df_grammy_since2000.drop(indexNames)

indexNames = df_grammy_since2000[df_grammy_since2000['category'] != 'Album Of The Year'].index
df_grammy_Album = df_grammy_since2000.drop(indexNames)

indexNames = df_grammy_since2000[df_grammy_since2000['category'] != 'Song Of The Year'].index
df_grammy_Song = df_grammy_since2000.drop(indexNames)

indexNames = df_grammy_since2000[df_grammy_since2000['category'] != 'Best New Artist'].index
df_grammy_Artist = df_grammy_since2000.drop(indexNames)

indexNames = df_grammy_since2000[df_grammy_since2000['category'] != 'Best Music Video'].index
df_grammy_Video = df_grammy_since2000.drop(indexNames)

indexNames = df_grammy_since2000[df_grammy_since2000['category'] != 'Best Short Form Music Video'].index
df_grammy_Videoshort = df_grammy_since2000.drop(indexNames)

indexNames = df_grammy_since2000[df_grammy_since2000['category'] != 'Best Long Form Music Video'].index
df_grammy_Videolong = df_grammy_since2000.drop(indexNames)

# Zum Schluss wird nochmals ein neu geordnetes DataFrame erstellt und als csv-Datei abgespeichert. Diese
# Datei wird nun im Jupyter Notebook bereinigt und zur Auswertung vorbereitet.
df_grammy_relevant = pd.concat([df_grammy_Record,df_grammy_Artist,df_grammy_Album,df_grammy_Song,
                                df_grammy_Video,df_grammy_Videoshort,df_grammy_Videolong],
                               keys=['Record Of The Year','Artist Of The Year','Album Of The Year',
                                     'Song Of The Year','Best Music Video','Best Short Form Music Video',
                                     'Best Long Form Music Video'])

df_grammy_relevant.to_csv("Suter_Sandro_src.csv",index=True,header=True)