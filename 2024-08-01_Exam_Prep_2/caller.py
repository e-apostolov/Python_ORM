import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


# Create queries within functions
def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_country = Q(country__icontains=search_country)

    if search_name is not None and search_country is not None:
        query = query_name & query_country
    elif search_name is not None:
        query = query_name
    else:
        query = query_country

    tennis_players = TennisPlayer.objects.filter(query).order_by('ranking')
    if not tennis_players:
        return ""
    return '\n'.join(f"Tennis Player: {t.full_name}, country: {t.country}, ranking: {t.ranking}" for t in tennis_players)


def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if not top_player:
        return ""

    return f"Top Tennis Player: {top_player.full_name} with {top_player.wins_count} wins."


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(count_matches=Count('players')).order_by('-count_matches', 'ranking').first()

    if not player or player.count_matches == 0:
        return ""

    return f"Tennis Player: {player.full_name} with {player.count_matches} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    tournaments = Tournament.objects.annotate(matches_count=Count('tournaments')).filter(surface_type__icontains=surface).order_by('-start_date')

    if not tournaments:
        return ""

    return '\n'.join(f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.matches_count}" for t in tournaments)


def get_latest_match_info():
    latest_match = Match.objects \
        .prefetch_related('players') \
        .order_by('-date_played', '-id') \
        .first()

    if latest_match is None:
        return ""

    players = latest_match.players.order_by('full_name')
    player1_full_name = players.first().full_name
    player2_full_name = players.last().full_name
    winner_full_name = "TBA" if latest_match.winner is None else latest_match.winner.full_name

    return f"Latest match played on: {latest_match.date_played}, tournament: {latest_match.tournament.name}, " \
           f"score: {latest_match.score}, players: {player1_full_name} vs {player2_full_name}, " \
           f"winner: {winner_full_name}, summary: {latest_match.summary}"


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.select_related('tournament', 'winner').filter(tournament__name__exact=tournament_name).order_by('-date_played')

    if not matches.exists():
        return "No matches found."

    return "\n".join(f"Match played on: {m.date_played}, "
                     f"score: {m.score}, "
                     f"winner: {m.winner.full_name if m.winner else 'TBA'}" for m in matches)