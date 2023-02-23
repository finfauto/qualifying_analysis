import fastf1
from fastf1 import utils
from fastf1.core import Session
from matplotlib import pyplot as plt, colors


def get_session_data(season: int, gp: str):
    session = fastf1.get_session(season, gp, 'Q')
    session.load()
    return session


def get_fastest_lap_data(session_data: Session, driver_id: str):
    print(session_data.results.loc[driver_id])
    laps_driver = session_data.laps.pick_driver(driver_id)
    fl_driver = laps_driver.pick_fastest()

    if fl_driver["LapTime"] == session_data.results.loc[driver_id]['Q1']:
        session_id = 'Q1'
    elif fl_driver["LapTime"] == session_data.results.loc[driver_id]['Q2']:
        session_id = 'Q2'
    else:
        session_id = 'Q3'

    return fl_driver, session_id


def show_qualifying_comparison(season: int, gp: str, driver1: str, driver2: str):
    session_data = get_session_data(season, gp)
    print(type(session_data))
    fl_driver1, fl_driver1_session = get_fastest_lap_data(session_data, driver1)
    fl_driver2, fl_driver2_session = get_fastest_lap_data(session_data, driver2)

    assert fl_driver1_session == fl_driver2_session, "Laps are from different sessions and won't be compared"

    # Extract the delta time
    delta_time, ref_tel, compared_tel = utils.delta_time(fl_driver1, fl_driver2)

    plot_title = f"Qualifying comparison: Season {season}, {gp}, {driver1} vs {driver2}"
    plot_ratios = [1, 3, 3, 3]
    plot_filename = f"{season}-{gp}-{driver1}-{driver2}.png"

    fig, ax = plt.subplots(4, gridspec_kw={'height_ratios': plot_ratios})

    # Delta line
    ax[0].set_title(plot_title)
    ax[0].plot(ref_tel['Distance'], delta_time, color=colors.CSS4_COLORS["goldenrod"])
    ax[0].set_ylabel(f'<-- {driver2} ahead || {driver1} ahead -->')

    # Speed
    ax[1].plot(ref_tel['Distance'], ref_tel["Speed"], label=driver1, color="blue")
    ax[1].plot(compared_tel['Distance'], compared_tel["Speed"], label=driver2, color="red")
    ax[1].set_ylabel('Speed (km/h)')
    ax[1].legend()

    # Throttle trace
    ax[2].plot(ref_tel['Distance'], ref_tel["Throttle"], label=driver1, color="blue")
    ax[2].plot(compared_tel['Distance'], compared_tel["Throttle"], label=driver2, color="red")
    ax[2].set_ylabel('Throttle')
    ax[2].legend()

    # Brake trace
    ax[3].plot(ref_tel['Distance'], ref_tel["Brake"], label=driver1, color="blue")
    ax[3].plot(compared_tel['Distance'], compared_tel["Brake"], label=driver2, color="red")
    ax[3].set_ylabel('Brake')
    ax[3].legend()

    ax[-1].set_xlabel('Lap distance (meters)')
    fig.set_size_inches((11, 8.5), forward=False)
    plt.savefig(plot_filename)
    plt.show()
