import requests
from bs4 import BeautifulSoup
import time

pageURL = "https://www.eventbrite.ca/o/daft-brewing-30029384480"
Keywords = "Thick"
refLink = None
monitorDelay = 5
checkoutLinkBase = "https://www.eventbrite.ca/checkout-external?"


def main():
    s = requests.Session()
    r = s.get(pageURL)
    if r.status_code == 200:
        print("organizer page loaded")
    #recaptchaToken = reCaptchaV3(anchor)
    soup = BeautifulSoup(r.text, 'html.parser')

    numevents = soup.find("button", {"class" : "eds-btn eds-btn--button eds-btn--follow eds-btn--following"}).text
    digits = 0
    for i in numevents:
        if i.isdigit():
            digits += 1
    numevents = numevents[10:10+digits]
    numevents = int(numevents)

    while(True):

        print("Scanning page for event")

        events = soup.find_all("a", {"class" : "eds-event-card-content__action-link","tabindex" : "0"}) 
        events = events[:numevents]
        for i in events:
            if i.text.find(Keywords) != -1:
                eventName = i.text[:int(len(i.text)/2)]
                print("Event found: " + eventName)
                refLink = i['href']
                break
        if refLink != None:
            break
        time.sleep(monitorDelay)
    
    r = s.get(refLink)
    if(r.status_code == 200):
        print("Event page loaded")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    queryLoc = refLink.find("?")
    eid = refLink[queryLoc-12:queryLoc]
    #https://www.eventbrite.ca/checkout-external?eid=523903759247&parent=https%3A%2F%2Fwww.eventbrite.ca%2Fe%2Fthick-thirsty-with-rowena-whey-tickets-523903759247%3Faff%3Debdsoporgprofile&modal=1&aff=ebdsoporgprofile
    parentURL = refLink.replace("/", "%2F")
    parentURL = parentURL.replace(":", "%3A")
    parentURL = parentURL.replace("?", "%3F")
    parentURL = parentURL.replace("=", "%3D")
    checkoutLink = checkoutLinkBase + "eid=" + eid + "&parent=" + parentURL + "%3Faff%3Debdsoporgprofile&modal=1&aff=ebdsoporgprofile"
    r = s.get(checkoutLink)
    print("Loading checkout page")
    if r.status_code == 200:
        print("Checkout page loaded")

        
    checkoutLink = "https://www.eventbrite.ca/checkout-widget-ajax/" + eid + "/"
    r = s.get(checkoutLink)
    print("Loading checkout widget")
    if r.status_code == 200:
        print("Checkout widget loaded")
    #print(r.text)




main()