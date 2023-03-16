# **PRIME VOLLEY DATA ANALYSIS**

#### Project Description

A data analysis project concentrating on the in-depth individual and team performance of each players and
teams which played in the Rupay Prime Volleyball League 2023.
This analysis is built from the statistics available publicly on the [Volleyball World](https://en.volleyballworld.com/volleyball/competitions/prime-volleyball-league-2023/) website. The ----continue with what specific answers this gives.
For scraping the data, this project uses Selenium to run the chrome webdriver to the webpages of the individual matches of the tournament, then saves the full page source.
Then used Pandas to do read_html on the saved page source to do the necessary steps for the analysis.


#### Prerequisites

1. Pandas Library
2. Selenium Library
3. Chrome Webdriver Installed


#### How To Run

Download Chrome Driver from [here](https://chromedriver.chromium.org/downloads) if not installed already.
Download all the files and edit the main.py file - change the location of the webdriver (driver_binary_location) and the chrome browser app (binary_app_location) to the correct location on your system. In Windows, the webdriver location(driver_binary_location) should contain "/" between directories.
But for the chrome browser app location(binary_app_location) it should be having regular "\".

**example :**
```
# WebDriver and app location
driver_binary_location = "C:/Program Files/Google/Chrome/Application/chromedriver.exe"
binary_app_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
```
