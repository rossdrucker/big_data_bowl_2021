"""
@author: Ross Drucker
"""
import os
import urllib

from bdb_helpers.util import get_soup


def scrape_logos(league):
    """
    """

    league_links = {

        'NCAAM': 'mens-college-basketball',
        'NCAAF': 'college-football',
        'MLB': 'mlb',
        'NFL': 'nfl',
        'NBA': 'nba',
        'NHL': 'nhl',
        'EPL': 'football'
    }

    if league == 'MLS':
        url = 'https://www.espn.com/soccer/teams/_/league/USA.1/major-league-soccer'
    elif league == 'UEFA Champions League':
        url = 'https://www.espn.com/soccer/teams/_/league/UEFA.CHAMPIONS/uefa-champions-league'
    elif league == 'UEFA Europa League':
        url = 'https://www.espn.com/soccer/teams/_/league/UEFA.EUROPA/uefa-europa-league'
    elif league == 'Spanish Primera Division':
        url = 'https://www.espn.com/soccer/teams/_/league/ESP.1/spanish-primera-división'
    elif league == 'Italian Serie A':
        url = 'https://www.espn.com/soccer/teams/_/league/ITA.1/italian-serie-a'
    elif league == 'Bundesliga':
        url = 'https://www.espn.com/soccer/teams/_/league/GER.1/german-bundesliga'
    elif league == 'NWSL':
        url = "https://www.espn.com/soccer/teams/_/league/USA.NWSL/united-states-nwsl-women's-league"
    else:
        url = f'https://www.espn.com/{league_links[league]}/teams'

    soup = get_soup(url)

    test = soup.find_all('div', attrs={'class':'ContentList__Item'})

    for item in test:
        #time.sleep(3)
        if league == 'NCAAF' or league == 'NCAAM':
            temp_league = 'ncaa'
            splitter = 'id/'
        elif league in ['EPL', 'MLS', 'UEFA Champions League',
                        'UEFA Europa League', 'Spanish Primera Division',
                        'Italian Serie A', 'Bundesliga', 'NWSL']:
            temp_league = 'soccer'
            splitter = 'id/'
        else:
            temp_league = league_links[league]
            splitter = 'name/'

        try:
            temp = item.a.get('href')
            s1 = temp.split(splitter)[1]
            s2 = s1.split('/')
            myid = s2[0]
            title = s2[1]
        except:
            continue

        url = f'https://a.espncdn.com/combiner/i?img=/i/teamlogos/{temp_league}/500/{myid}.png'
        folder = os.path.join(os.getcwd(), 'img', 'logos')
        try:
            os.chdir(folder)
        except:
            os.mkdir(folder)
            os.chdir(folder)
        
        try:
            urllib.request.urlretrieve(url, f'{title}.png')
            print(f'Saved {title}')
        except:
            continue

    print(f'Done scraping {league} logos')
    return None

if __name__ == '__main__':
    leagues = ['NFL']

    for league in leagues:
        scrape_logos(league)