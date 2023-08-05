import cloudscraper

scraper = cloudscraper.create_scraper(delay=10,interpreter='nodejs',
  captcha={'provider': 'return_response'})


def crashsite():
   games = scraper.get("https://rest-bf.blox.land/games/crash").json()
   return games

def crashpredictor():
    try:
     games = crashsite()
    except Exception as e:
      return f'Error {e}'
    def lol():
          r=scraper.get("https://rest-bf.blox.land/games/crash").json()["history"]
          yield [r[0]["crashPoint"], [float(crashpoint["crashPoint"]) for crashpoint in r[-2:]]]
    for game in lol():
            games = game[1]
            lastgame = game[0]
            avg = sum(games) / len(games)
            chance = 1
            for game in games:
                chancee = chance = 95 / game
                prediction = (1 / (1 - (chancee)) + avg) / 2

                amo = {'crashchance': chancee, 'crashprediction': prediction}
                return amo
