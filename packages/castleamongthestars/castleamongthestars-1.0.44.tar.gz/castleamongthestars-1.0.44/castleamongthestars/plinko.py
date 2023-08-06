import cloudscraper
import requests

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    }
)
def autoplinko(auth, bet_amount, risk, rows):
    request = scraper.get("https://rest-bf.blox.land/games/plinko/roll", headers={"x-auth-token": auth},
                           json={"amount": bet_amount, "risk": risk, "rows": rows})
    checker = request['success']
    if checker == True:
        return request
    else:
        errorr = request['error']
        error = {'error': errorr, 'status': False}
        return error