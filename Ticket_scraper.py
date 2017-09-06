### ----------------------------------------------------------------- ###
### ----------------------------------------------------------------- ###
### ----           _____                                         ---- ###
### ----          / ____|                                        ---- ###
### ----         | (___   ___ _ __ __ _ _ __   ___ _ __          ---- ###
### ----          \___ \ / __| '__/ _` | '_ \ / _ \ '__|         ---- ###
### ----          ____) | (__| | | (_| | |_) |  __/ |            ---- ###
### ----         |_____/ \___|_|  \__,_| .__/ \___|_|            ---- ###
### ----                               | |                       ---- ###
### ----                               |_|                       ---- ###
### ----------------------------------------------------------------- ###
### ----------------------------------------------------------------- ###

__author__ = 'j.kromme'
__description__ = 'Scrape cheaptickets for all available airports and dates to find the cheapest and fastest flights'

# import packages
import time, datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import selenium.webdriver.support.ui as ui
now = datetime.datetime.now()


def scrape(go_dates, go_airports_from, go_airports_to, return_dates, return_airports_from, return_airports_to, driver, wait, filename):
    '''
    scrape cheaptickets
    '''

    
    # paths to elements
    xpaths = {
        'price' : "//span[@class='price__value value']",
        'time' : "//div[@class='flight-info__travel-time']"
    }

    # counter
    i = 0

    # loop through all dates and airports
    for go_date in go_dates:
        for go_airport_from in go_airports_from:
            for go_airport_to in go_airports_to:
                for return_date in return_dates:
                    for return_airport_from in return_airports_from:
                        for return_airport_to in return_airports_to:
                            
                            # fix date notation
                            go_date1 = go_date[-4:]+ '-'+ go_date[3:5] + '-' + go_date[0:2]
                            return_date1 = return_date[-4:]+ '-'+ return_date[3:5] + '-' + return_date[0:2]

                            # define URL
                            url = 'https://www.cheaptickets.nl/vluchtresultaten?adt=1&chd=0&cls=Y&inf=0&dep1=%s&dep1_all=false&date1=%s&arr1=%s&arr1_all=false&dep2=%s&dep2_all=false&date2=%s&arr2=%s&arr2_all=false' %(go_airport_from,go_date1,  go_airport_to,  return_airport_from, return_date1, return_airport_to )
                            driver.get(url)
                            
                            # wait until done
                            wait.until(lambda driver: driver.find_elements_by_xpath(xpaths['price']))

                            # get price and flight time of first flight
                            price = driver.find_element_by_xpath(xpaths['price']).text
                            times = driver.find_elements_by_xpath(xpaths['time'])
                            tim = times[0].text +'-' +  times[1].text                                          

                            # save results
                            with open(filename, 'a') as f:
                                f.write(go_airport_from + ';'  + go_airport_to + ';' +go_date + ';' +return_airport_from + ';' + return_airport_to + ';' +return_date + ';' + tim + ';' + price + ';' + url + '\n')
                            i+=1




if __name__ == "__main__":
    # define output file
    filename = now.strftime("%Y%m%d") + '_scrapertickets.csv'

    # start driver
    driver = webdriver.Chrome('C:/Users/j.kromme/Documents/chromedriver.exe')
    wait = ui.WebDriverWait(driver, 20)

    # define elements

    # --- first flight
    go_dates = [ '01-10-2017', '02-10-2017', '03-10-2017', '04-10-2017'
                 ,'05-10-2017', '06-10-2017', '07-10-2017', '08-10-2017'
                 ,'09-10-2017', '10-10-2017', '11-10-2017', '12-10-2017'
                 ,'15-10-2017', '16-10-2017', '17-10-2017', '18-10-2017' 
                 ,'19-10-2017', '20-10-2017', '21-10-2017', '22-10-2017'
                 ,'19-10-2017', '20-10-2017', '21-10-2017', '22-10-2017'
                ]
    go_airports_from = ['AMS', 'DUS']
    go_airports_to = ['BOG',  'MDE']


    # --- return flight
    return_dates = [ '01-12-2017','02-12-2017', '03-12-2017', '04-12-2017'
                 ,'05-12-2017','06-12-2017', '07-12-2017', '08-12-2017'
                 ,'09-12-2017','10-12-2017', '11-12-2017', '12-12-2017'
                 ,'13-12-2017','14-12-2017', '15-12-2017', '16-12-2017'
                 ,'17-12-2017','18-12-2017', '19-12-2017', '20-12-2017'
                 ,'21-12-2017','22-12-2017', '23-12-2017', '24-12-2017'
                 ,'25-12-2017','26-12-2017', '27-12-2017', '28-12-2017'
                 ,'29-12-2017','30-12-2017', '31-12-2017'
    ]

    return_airports_from = ['TGU', 'MGA', 'SJO']
    return_airports_to = ['AMS']

    # how many flights are checked
    no_of_flights_to_check = len(go_dates) * len(go_airports_from) * len(go_airports_to) * len(return_dates) * len(return_airports_from) * len(return_airports_to)
    print 'checking %d flights' % no_of_flights_to_check

    # scrape!
    scrape(go_dates, go_airports_from, go_airports_to, return_dates, return_airports_from, return_airports_to, driver, wait, filename)