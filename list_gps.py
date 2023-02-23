import fastf1


def list_gps(season: int):
    events = fastf1.get_event_schedule(season, include_testing=False)
    for event in events["EventName"]:
        print(event)
