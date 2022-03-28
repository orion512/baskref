import psycopg2
import psycopg2.extras
from requests_html import HTMLSession

print('Script Start')

# Global Variables


# Functions
def scrape_games(year: int):
    br_season_games_url = f'https://www.basketball-reference.com/leagues/NBA_{year}_games.html'

    session = HTMLSession()
    r = session.get(br_season_games_url)

    schedule_table_body = r.html.find('#schedule', first=True).find('tbody', first=True)
    schedule_rows = schedule_table_body.find('tr')

    games = []
    for row in schedule_rows:
        games.append((
            row.find('th[data-stat=date_game]', first=True).text,
            row.find('td[data-stat=visitor_team_name]', first=True).find('a', first=True).text,
            row.find('td[data-stat=home_team_name]', first=True).find('a', first=True).text,
            int(row.find('td[data-stat=visitor_pts]', first=True).text),
            int(row.find('td[data-stat=home_pts]', first=True).text),
        ))

    return games


def insert_games(games_to_insert: list):

    conn = psycopg2.connect(
        dbname='nba',
        user='postgres',
        password='password',
        host='localhost',
    )

    records_list_template = ",".join(["%s"] * len(games_to_insert))

    sql_stmt = (
        f"INSERT INTO nba.game"
        f"(date, away_team, home_team, away_score, home_score)"
        f" VALUES {records_list_template} returning id"
    )

    print(sql_stmt)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql_stmt, games_to_insert)
    new_ids = [res[0] for res in cur.fetchall()]

    cur.close()

    conn.commit()
    conn.close()

    return new_ids


def select_game_cnt():

    conn = psycopg2.connect(
        dbname='nba',
        user='postgres',
        password='password',
        host='localhost',
    )

    sql_stmt = ("SELECT COUNT(id) FROM nba.game")

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql_stmt)
    res = cur.fetchall()

    cur.close()
    conn.close()

    return res


def main():
    games = scrape_games(2022)
    ins_ids = insert_games(games)
    print(f'Inserted {len(ins_ids)} rows')

    cnt = select_game_cnt()
    print(f'DB game count: {cnt}')



if __name__ == "__main__":
    main()
