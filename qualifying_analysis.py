import argparse
import logging

import fastf1

from list_drivers import list_drivers
from list_gps import list_gps
from qualifying_comparison import show_qualifying_comparison


def parse_args():
    parser = argparse.ArgumentParser(description='Command-line argument processor for a Formula 1 qualifying analysis tool')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--season', type=int, help='Season identifier', required=True)
    # Subparser for the "season"
    season_actions_subparsers = parser.add_subparsers(title='season_actions', dest='season_action', required=True)

    # Subparser for the "list" action. No further parsers
    season_actions_subparsers.add_parser('list', help='Get a list of GPS from the season')

    # Subparser for the "analyze" action
    analyze_parser = season_actions_subparsers.add_parser('analyze', help='Analyze telemetry data for a GP qualifying from the season given')
    analyze_parser.add_argument('--gp', type=str, help='GP identifier')

    # Subparsers for the "analyze" action
    gp_action_subparsers = analyze_parser.add_subparsers(title='gp_actions', dest='gp_action', required=True)

    # Subparser for the "compare" action
    gp_action_subparsers.add_parser('list_drivers', help='Show the drivers involved in the session')

    # Subparser for the "compare" action
    compare_parser = gp_action_subparsers.add_parser('compare', help='Compare the telemetry of two drivers')
    compare_parser.add_argument('--driver1', type=str, help='Driver 1 name', required=True)
    compare_parser.add_argument('--driver2', type=str, help='Driver 2 name', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(args)
    if not args.verbose:
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)

    fastf1.Cache.enable_cache('cache')

    if args.season_action == 'list':
        list_gps(args.season)
    else:
        if args.gp_action == 'list_drivers':
            list_drivers(args.season, args.gp)
        else:
            show_qualifying_comparison(args.season, args.gp, args.driver1, args.driver2)
