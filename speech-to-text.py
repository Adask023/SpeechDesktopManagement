import speech_recognition as sr
import pyttsx3 as tts
import webbrowser
import sys
import time
import os
from weatherAPI import WeatherItem
import datetime

# chrome load
# chrome = 'C:\\"Program Files (x86)"\\Google\\Chrome\\Application\\chrome.exe'

# special words declarations
ACTIVATE_WORDS = ['adam', 'adamie']
DEACTIVATE_WORDS = ['do widzenia', 'wyłącz', 'zgaś']
SEARCH_WORDS = ['wyszukaj', 'szukaj', 'google', 'znajdź']
OPEN_LOL_WORDS = ['league of legends', 'lol', 'liga', 'liga legend', 'ligę legend', 'ligę']
SEARCH_WEATHER_WORDS = ['sprawdź pogodę w', ' sprawdź pogodę', 'aktualna pogoda', 'aktualna pogoda w', 'pogoda w',
                        'pogoda']
THANKS_WORDS = ['dzięki', 'dziena', 'thanks', 'thx', 'dziękuję']
DATE_WORDS = ["data", "który dzisiaj jest", "dzień", ]
TIME_WORDS = ["godzina", "aktualna godzina", "jaka jest teraz godzina"]


def speechBot():
    # Objects / setting the pyttsx3 engine
    r = sr.Recognizer()

    engine = tts.init()
    engine.setProperty('voice', engine.getProperty('voices')[0].id)
    engine.setProperty("rate", 125)

    today = datetime.datetime.today()

    # speaking(text)
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # getting the text from microphone input (may require PyAudio)
    def getText():
        try:
            with sr.Microphone() as source:

                audio = r.listen(source)
                # print("Słucham...", end='\r')
                text = r.recognize_google(audio, language="pl-PL")
            if text == "":
                return None
            else:
                return text
        except:
            return None

    # checks if any list contains a word from the input
    def contains(string, words):
        return [element for element in words if element in string.lower()]

    # alternative version of loop above
    # for element in words:
    #   if element in string.lower():
    #       lista.append(element)
    # return lista

    # handle information about weather
    def weatherInformation(city, temperature, humidity, status):

        minusTemp = ""
        if temperature < 0:
            minusTemp = "minus"

        textToShow = (f'temperatura w {city} wynosi: {minusTemp} {temperature} '
                      f'stopni celcjusza, wilgotność {humidity} procent'
                      f', status: {status}')

        return textToShow

    speak("Słucham")
    print("Aby wyjść powiedz 'do widzenia'")

    # main logic of the application
    while True:
        time.sleep(0.5)
        current = getText()
        print(current)
        # print("" * 50, end="\r")

        if current is not None:
            if len(contains(current, ACTIVATE_WORDS)):
                if len(contains(current, DEACTIVATE_WORDS)):
                    speak("Żegnaj")
                    break

                # searching with browser
                elif len(contains(current, SEARCH_WORDS)):
                    link = current.lower().split('' + contains(current, SEARCH_WORDS)[0] + '')[1]
                    print("Oto efekt twojego wyszukiwania")
                    speak("Oto efekt twojego wyszukiwania")
                    url = "https://www.google.com/search?q=" + link.replace(" ", "+").replace("?", "%3F")
                    webbrowser.open(url, new=2)

                # open application LOL
                elif len(contains(current, OPEN_LOL_WORDS)):
                    speak('otwieram league of legends')
                    print('ootwieram league of legends')
                    os.system('E:\\LOL\\"Riot Games"\\"League of Legends"\\LeagueClient.exe')

                # thanks
                elif len(contains(current, THANKS_WORDS)):
                    speak('Nie ma za co, po to mnie stworzyłeś')

                # temperature in given town name
                elif len(contains(current, SEARCH_WEATHER_WORDS)):
                    try:
                        town = current.lower().split('' + contains(current, SEARCH_WEATHER_WORDS)[0] + '')[1]
                        if not town:
                            town = 'bielsko-biala'
                        weatherTown = WeatherItem(town)

                        print(
                            weatherInformation(weatherTown.getCityName(), weatherTown.getTemperature(),
                                               weatherTown.getHumidity(), weatherTown.getStatus()))
                        speak(
                            weatherInformation(weatherTown.getCityName(), weatherTown.getTemperature(),
                                               weatherTown.getHumidity(), weatherTown.getStatus()))

                    except:
                        print(f'Błąd, nie udało się wyszukać miasta')
                        speak(f'Błąd, nie udało się wyszukać miasta')

                # actual date
                elif len(contains(current, DATE_WORDS)):
                    d1 = today.strftime("%d/%m/%Y")
                    print(f'dzisiaj jest: {d1}')
                    speak(f'dzisiaj jest: {d1}')

                # actual time
                elif len(contains(current, TIME_WORDS)):
                    timeNow = today.strftime("%H:%M:%S")
                    print(f'Aktualna godzina to: {timeNow}')
                    speak(f'Aktualna godzina to: {timeNow}')


if __name__ == "__main__":
    speechBot()

# transformer