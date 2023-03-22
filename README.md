# **PRIME VOLLEY DATA ANALYSIS**

#### Project Description

A data analysis project concentrating on the in-depth individual and team performance of each players and
teams which played in the Rupay Prime Volleyball League 2023.
This analysis is built from the statistics available publicly on the [Volleyball World](https://en.volleyballworld.com/volleyball/competitions/prime-volleyball-league-2023/) website. Some of the questions being answered with this analysis are "who are the most defensive setters in this league?" and "what teams do your favourite team found most challenging to play against?" etc.

For scraping the data, this project uses Selenium to run the chrome webdriver to the webpages of the individual matches of the tournament, then saves the full page source.
Then used Pandas to do read_html on the saved page source to do the necessary steps for the analysis.


#### Visualizations

The Interface for the visualizations are made in a way that makes them intuitive and engaging.
All the items are clickable and are used to navigate further

![Screenshot 2023-03-23 045002](https://user-images.githubusercontent.com/78293634/227060714-c8fabdd8-2309-492c-95b5-0766241f6b60.png)


![Screenshot 2023-03-23 045145](https://user-images.githubusercontent.com/78293634/227060734-5be42713-ea2d-444b-841e-59edada2cc8f.png)


#### Prerequisites

1. Pandas Library
2. Selenium Library
3. Chrome Webdriver Installed


#### How To Run

Download Chrome Driver from [here](https://chromedriver.chromium.org/downloads) if not installed already.

Download all the files from the repo and edit the main.py file - change the location of the webdriver (driver_binary_location) and the chrome browser app (binary_app_location) to the correct location on your system. In Windows, the webdriver location(driver_binary_location) should contain "/" between directories.
But for the chrome browser app location(binary_app_location) it should be having regular "\\".

**example :**
```
# WebDriver and app location
driver_binary_location = "C:/Program Files/Google/Chrome/Application/chromedriver.exe"
binary_app_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
```
