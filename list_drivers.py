from qualifying_comparison import get_session_data


def list_drivers(season: int, gp: str):
    session = get_session_data(season=season, gp=gp)
    print(session.results)
