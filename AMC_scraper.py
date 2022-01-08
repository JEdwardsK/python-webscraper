from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import json
from datetime import timedelta, datetime



def get_film_showtimes_dict (film):
    """generates a list of dictionaries with details of screen showtimes

    Args:
        film ([bs4.element.Tag]): [a Beautiful Soup Tag element]

    Returns:
        [list]: [a list of screen objects containing screenType (e.g. IMAX, digital, Real3D), screenFeatures (e.g. "Reserved Seating", "Closed Caption", "Audio Description") and showTimes]
    """
    screens = []
    
    # get all screens, first screen section has -First in class, get separately, then concat with rest
    first_screen_section = [film.find("div", class_="Showtimes-Section-Wrapper-First")]
    screen_sections = first_screen_section + film.find_all("div", class_="Showtimes-Section-Wrapper")

    for screen in screen_sections:
        screen_type = screen.h4.get_text()
        screen_features = [feature.get_text() for feature in screen.find_all('li')]
        # make an list of button objects for the show times
        showtimes_buttons = film.find('section', class_="ShowtimeButtons").find_all("div", class_="Showtime")
        showtimes = [{'time': button.get_text(), 'href': button.a['href']} for button in showtimes_buttons]
        screen_info = {
          'screenType': screen_type,
          'screenFeatures': screen_features,
          'showTimes': showtimes
        }

        screens.append(screen_info)
    return screens

def get_date_from_URL(url):
  """finds the date 2022-MM-DD from the input URL string and returns it

  Args:
      url (string): AMC url string
  """
  path_list = urlparse(url).path.split('/')
  for item in path_list:
      if '2022' in item:
          return item

def update_film_json(url):
    """scrapes the input url for film show time data, exports result to data.JSON 

    Args:
        url (string): [AMC theatres url string]
        date (string) : 
    """

    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    films = soup.find_all("div", class_="ShowtimesByTheatre-film")
    film_data_list = []
    film_titles = set()
    for film in films:
        film_header = film.find('a', class_="MovieTitleHeader-title")
        film_data = {
        'filmName': film_header.get_text(),
        'href': film_header['href']
        }
        film_titles.add(film_data['filmName'])
        screens = get_film_showtimes_dict(film)
        film_data['screens']= {'day0': screens}
        film_data_list.append(film_data)

    # The size of each step in days
    date_str = get_date_from_URL(url)
    start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    day_delta = timedelta(days=1)
    end_date = start_date + 7 * day_delta
    prev_date = start_date

    #  loop through each day for seven days
    for i in range((end_date - start_date).days):
        loop_date = start_date + i * day_delta
        prev_date = str(loop_date - 1 * day_delta)
        url = url.replace(prev_date, str(loop_date))
        print(i)
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        films = soup.find_all("div", class_="ShowtimesByTheatre-film")
        # film_data_list = []
        # titles = [film.]
        for film in films:
            film_title = film.find('a', class_="MovieTitleHeader-title").get_text()
            film_href = film.find('a', class_="MovieTitleHeader-title")['href']
            screens = get_film_showtimes_dict(film)
            if film_title in film_titles:
            # find the right film object in data and add showtimes
                for film in film_data_list:
                    if film['filmName'] == film_title:
                        film['screens'][f"day{i + 1}"] = screens
                        break
            else:
                new_film_data = {
                    'filmName': film_title,
                    'href': film_href,
                    'screens': {
                        f"day{i + 1}" : screens
                    }
                }
                film_data_list.append(new_film_data)
                film_titles.add(film_title)

    with open('data.json', 'w') as f:
        json.dump(film_data_list, f, indent=2)