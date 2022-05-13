"""
This page contains the class which is used to scrape data 
from basketball reference website.

- Scrape all teams https://www.basketball-reference.com/teams/
- Scrape all players https://www.basketball-reference.com/players/
- Scrape all games in a year 
    - https://www.basketball-reference.com/leagues/NBA_2022_games-april.html
    - scrape all months
    - scrape all games including link to box scores
- Scrape all playoff games in a year
    - https://www.basketball-reference.com/playoffs/NBA_2022_games.html

Author: Dominik Zulovec Sajovic, may 2022
"""

from requests_html import HTMLSession
from datetime import datetime
import pandas as pd
import time


class BasketballReference:
    """ Class for scraping basketball-reference.com """
    
    base_url = None
    
    def __init__(self):
        """ Initializes the class """
        self.base_url = 'https://www.basketball-reference.com'
        
        
    def generate_season_games_url(self, year: int) -> str:
        """ Generates the url for all games in a year """
        return f'{self.base_url}/leagues/NBA_{year}_games.html'
    
    
    def scrape_all_months_urls(self, year: int) -> list:
        """
        Scrapes the urls to every month of a given NBA season
        :year: A year representing the year in which the NBA season ends
        :return: returns a list of month urls from Basketball Reference
        """

        with HTMLSession() as session:

            main_page = session.get(self.generate_season_games_url(year))
            if main_page.status_code == 200:
                all_months_urls = [
                    self.base_url + a.attrs['href'] 
                    for a in main_page.html.find('div.filter > div > a')]
            else:
                raise Exception(
                    f"Couldn't scrape {self.generate_season_games_url(year)}."
                    f"Status code: {main_page.status_code}")
        
        return all_months_urls
    

    def scrape_game_urls(self, page: str) -> list:
        """
        Scrapes the urls to every game (boxscore) from the webpage
        :page: web page - /leagues/NBA_YEAR_games-MONTH.html
        :return: returns a list of game urls from Basketball Reference
        """
        
        element_finder = 'td[data-stat="box_score_text"]'
        game_urls = []

        with HTMLSession() as session:
            month_page = session.get(page)
            if month_page.status_code == 200:
                for td in month_page.html.find(element_finder):
                    anch = td.find('a', first=True)
                    if anch != None:
                        url =  anch.find('a', first=True).attrs['href']
                        game_urls.append(self.base_url + url)
            else:
                raise Exception(
                    f"Couldn't scrape {page}."
                    f"Status code: {month_page.status_code}")

        return game_urls

    
    def scrape_multiple_game_url_pages(self, game_list_urls: list) -> list:
        """
        Scrapes multiple pages for urls to every game (boxscore).
        :game_list_urls: list of URLs containing list of games
        :return: returns a list of game urls from Basketball Reference
        """

        return [
            gurl for url in game_list_urls 
            for gurl in self.scrape_game_urls(url)]
    
    
    def scrape_game_data(self, game_url: str) -> dict:
        """
        Scrapes the data for the given game web page.
        :game_url: a Basketball Reference URL to a game page
        :return: returns a dictionary of game data
        """
        
        with HTMLSession() as session:
            game_page = session.get(game_url)

            if game_page.status_code != 200:
                raise Exception(
                    f"Couldn't scrape {game_page}."
                    f"Status code: {game_page.status_code}")
            
            # Team names
            team_names = game_page.html.find('a[itemprop=name]') 
            home_team = team_names[1].attrs['href'].split('/')[2]
            away_team = team_names[0].attrs['href'].split('/')[2]
            home_team_full_name = team_names[1].text
            away_team_full_name = team_names[0].text

            # game time & arena
            meta_holder = game_page.html.find('div.scorebox_meta', first=True)
            game_time = datetime.strptime(meta_holder.find('div')[1].text, "%I:%M %p, %B %d, %Y")
            arena_name = meta_holder.find('div')[2].text.split(',')[0]

            # Attendance
            if 'Attendance' in game_page.text:
                attendance_text = game_page.text[game_page.text.index('Attendance'):game_page.text.index('Attendance')+35]
                digits = [s for s in attendance_text if s.isdigit()]
                attendance = ''
                for att in digits:
                    attendance += att
                attendance = int(attendance)
            else:
                attendance = None

            game_dic = {
                'game_id':               game_url,
                'home_team':             home_team,
                'away_team':             away_team,
                'home_team_full_name':   home_team_full_name,
                'away_team_full_name':   away_team_full_name,
                'game_time':             game_time,
                'arena_name':            arena_name,
                'attendance':            attendance
            }

            # home basic
            home_basic = game_page.html.find(f'#box-{home_team.upper()}-game-basic', first=True).find('tfoot', first=True)
            game_dic['home_fg'] = int(home_basic.find('td[data-stat=fg]', first=True).text)
            game_dic['home_fga'] = int(home_basic.find('td[data-stat=fga]', first=True).text)
            game_dic['home_fg_pct'] = float(home_basic.find('td[data-stat=fg_pct]', first=True).text)
            game_dic['home_fg3'] = int(home_basic.find('td[data-stat=fg3]', first=True).text)
            game_dic['home_fg3a'] = int(home_basic.find('td[data-stat=fg3a]', first=True).text)
            game_dic['home_fg3_pct'] = float(home_basic.find('td[data-stat=fg3_pct]', first=True).text)
            game_dic['home_ft'] = int(home_basic.find('td[data-stat=ft]', first=True).text)
            game_dic['home_fta'] = int(home_basic.find('td[data-stat=fta]', first=True).text)
            game_dic['home_ft_pct'] = float(home_basic.find('td[data-stat=ft_pct]', first=True).text)
            game_dic['home_orb'] = int(home_basic.find('td[data-stat=orb]', first=True).text)
            game_dic['home_drb'] = int(home_basic.find('td[data-stat=drb]', first=True).text)
            game_dic['home_trb'] = int(home_basic.find('td[data-stat=trb]', first=True).text)
            game_dic['home_ast'] = int(home_basic.find('td[data-stat=ast]', first=True).text)
            game_dic['home_stl'] = int(home_basic.find('td[data-stat=stl]', first=True).text)
            game_dic['home_blk'] = int(home_basic.find('td[data-stat=blk]', first=True).text)
            game_dic['home_tov'] = int(home_basic.find('td[data-stat=tov]', first=True).text)
            game_dic['home_pf'] = int(home_basic.find('td[data-stat=pf]', first=True).text)
            game_dic['home_pts'] = int(home_basic.find('td[data-stat=pts]', first=True).text)

            # away basic
            away_basic = game_page.html.find(f'#box-{away_team.upper()}-game-basic', first=True).find('tfoot', first=True)
            game_dic['away_fg'] = int(away_basic.find('td[data-stat=fg]', first=True).text)
            game_dic['away_fga'] = int(away_basic.find('td[data-stat=fga]', first=True).text)
            game_dic['away_fg_pct'] = float(away_basic.find('td[data-stat=fg_pct]', first=True).text)
            game_dic['away_fg3'] = int(away_basic.find('td[data-stat=fg3]', first=True).text)
            game_dic['away_fg3a'] = int(away_basic.find('td[data-stat=fg3a]', first=True).text)
            game_dic['away_fg3_pct'] = float(away_basic.find('td[data-stat=fg3_pct]', first=True).text)
            game_dic['away_ft'] = int(away_basic.find('td[data-stat=ft]', first=True).text)
            game_dic['away_fta'] = int(away_basic.find('td[data-stat=fta]', first=True).text)
            game_dic['away_ft_pct'] = float(away_basic.find('td[data-stat=ft_pct]', first=True).text)
            game_dic['away_orb'] = int(away_basic.find('td[data-stat=orb]', first=True).text)
            game_dic['away_drb'] = int(away_basic.find('td[data-stat=drb]', first=True).text)
            game_dic['away_trb'] = int(away_basic.find('td[data-stat=trb]', first=True).text)
            game_dic['away_ast'] = int(away_basic.find('td[data-stat=ast]', first=True).text)
            game_dic['away_stl'] = int(away_basic.find('td[data-stat=stl]', first=True).text)
            game_dic['away_blk'] = int(away_basic.find('td[data-stat=blk]', first=True).text)
            game_dic['away_tov'] = int(away_basic.find('td[data-stat=tov]', first=True).text)
            game_dic['away_pf'] = int(away_basic.find('td[data-stat=pf]', first=True).text)
            game_dic['away_pts'] = int(away_basic.find('td[data-stat=pts]', first=True).text)

            # home advanced
            home_advanced = game_page.html.find(f'#box-{home_team.upper()}-game-advanced', first=True).find('tfoot', first=True)
            game_dic['home_ts_pct'] = float(home_advanced.find('td[data-stat=ts_pct]', first=True).text)
            game_dic['home_efg_pct'] = float(home_advanced.find('td[data-stat=efg_pct]', first=True).text)
            game_dic['home_fg3a_per_fga_pct'] = float(home_advanced.find('td[data-stat=fg3a_per_fga_pct]', first=True).text)
            game_dic['home_fta_per_fga_pct'] = float(home_advanced.find('td[data-stat=fta_per_fga_pct]', first=True).text)
            game_dic['home_orb_pct'] = float(home_advanced.find('td[data-stat=orb_pct]', first=True).text)
            game_dic['home_drb_pct'] = float(home_advanced.find('td[data-stat=drb_pct]', first=True).text)
            game_dic['home_trb_pct'] = float(home_advanced.find('td[data-stat=trb_pct]', first=True).text)
            game_dic['home_ast_pct'] = float(home_advanced.find('td[data-stat=ast_pct]', first=True).text)
            game_dic['home_stl_pct'] = float(home_advanced.find('td[data-stat=stl_pct]', first=True).text)
            game_dic['home_blk_pct'] = float(home_advanced.find('td[data-stat=blk_pct]', first=True).text)
            game_dic['home_tov_pct'] = float(home_advanced.find('td[data-stat=tov_pct]', first=True).text)
            game_dic['home_off_rtg'] = float(home_advanced.find('td[data-stat=off_rtg]', first=True).text)
            game_dic['home_def_rtg'] = float(home_advanced.find('td[data-stat=def_rtg]', first=True).text)

            # away advanced
            away_advanced = game_page.html.find(f'#box-{away_team.upper()}-game-advanced', first=True).find('tfoot', first=True)
            game_dic['away_ts_pct'] = float(away_advanced.find('td[data-stat=ts_pct]', first=True).text)
            game_dic['away_efg_pct'] = float(away_advanced.find('td[data-stat=efg_pct]', first=True).text)
            game_dic['away_fg3a_per_fga_pct'] = float(away_advanced.find('td[data-stat=fg3a_per_fga_pct]', first=True).text)
            game_dic['away_fta_per_fga_pct'] = float(away_advanced.find('td[data-stat=fta_per_fga_pct]', first=True).text)
            game_dic['away_orb_pct'] = float(away_advanced.find('td[data-stat=orb_pct]', first=True).text)
            game_dic['away_drb_pct'] = float(away_advanced.find('td[data-stat=drb_pct]', first=True).text)
            game_dic['away_trb_pct'] = float(away_advanced.find('td[data-stat=trb_pct]', first=True).text)
            game_dic['away_ast_pct'] = float(away_advanced.find('td[data-stat=ast_pct]', first=True).text)
            game_dic['away_stl_pct'] = float(away_advanced.find('td[data-stat=stl_pct]', first=True).text)
            game_dic['away_blk_pct'] = float(away_advanced.find('td[data-stat=blk_pct]', first=True).text)
            game_dic['away_tov_pct'] = float(away_advanced.find('td[data-stat=tov_pct]', first=True).text)
            game_dic['away_off_rtg'] = float(away_advanced.find('td[data-stat=off_rtg]', first=True).text)
            game_dic['away_def_rtg'] = float(away_advanced.find('td[data-stat=def_rtg]', first=True).text)
        
        return game_dic
    
    
    def scrape_all_games_data(self, year: int, display_time:bool=True) -> list:
        """
        Scrapes the data for all the games in the given season
        positional arguments:
        :year: A year representing the year in which the NBA season ends
        :display_time: if True will print the execution time
        :return: returns a list of dictionaries for all the games in a season
        """
        start = time.time()
        
        all_game_urls = self.scrape_all_game_urls(year)
        
        all_games = []
        
        for count, game_url in enumerate(all_game_urls):
            dict_game_data = self.scrape_game_data(game_url, year, count)
            all_games.append(dict_game_data)
        
        print(f"Scraped data for {len(all_games)} games")

        end = time.time()
        
        if display_time:
            hours, rem = divmod(end-start, 3600)
            minutes, seconds = divmod(rem, 60)
            print(f"Complete Season Scrape Execution Time: {int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f}")
            
        return all_games


    def scrape_season_schedule(self, year: int, display_time:bool=True) -> pd.DataFrame():
        """
        Scrapes the schedule for the entire season
        positional arguments:
        :year: A year representing the year in which the NBA season ends
        :display_time: if True will print the execution time
        :return: returns a list of game urls from Basketball Reference
        """
        start = time.time()

        session = HTMLSession()

        all_months_urls = self.scrape_all_month_urls(year)
        all_scheduled_games = []

        for schedule_month in all_months_urls:

            month_page = session.get(schedule_month)

            table_schedule = month_page.html.find('table[id="schedule"]', first=True).find('tbody', first=True)

            for game_row in table_schedule.find('tr'):
                game_dic = {}
                game_date = game_row.find('th[data-stat="date_game"]', first=True).text
                game_time = game_row.find('td[data-stat="game_start_time"]', first=True).text
                game_time = game_time.replace('p', 'PM')
                game_time = game_time.replace('a', 'AM')

                visitor = game_row.find('td[data-stat="visitor_team_name"]', first=True)
                away_team = visitor.text
                away_team_short = visitor.attrs['csk'].split('.')[0]

                home = game_row.find('td[data-stat="home_team_name"]', first=True)
                home_team = home.text
                home_team_short = home.attrs['csk'].split('.')[0]

                game_time = datetime.strptime(f'{game_date.strip()} {game_time.strip()}', '%a, %b %d, %Y %I:%M%p')


                game_dic['GAME_TIME'] = game_time
                game_dic['HOME_TEAM'] = home_team
                game_dic['HOME_TEAM_SHORT'] = home_team_short
                game_dic['AWAY_TEAM'] = away_team
                game_dic['AWAY_TEAM_SHORT'] = away_team_short

                all_scheduled_games.append(game_dic)

                end = time.time()

        print(f'Scraped {len(all_scheduled_games)} games for the {year} season.')

        if display_time:
            hours, rem = divmod(end-start, 3600)
            minutes, seconds = divmod(rem, 60)
            print(f"Execution Time: {int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f}")

        return pd.DataFrame(all_scheduled_games)



if __name__ == '__main__':
    pass
