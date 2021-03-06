import json
import subprocess

from django.core.management.base import BaseCommand
from uuslug import slugify

import election.models as election
import entity.models as entity
import geography.models as geography
import server_config
import vote.models as vote


def _get_division_level(row):
    return geography.DivisionLevel.objects.get(
        name=row['level']
    )


def _get_division(row, level):
    kwargs = {
        'level': level
    }

    if row['reportingunitname']:
        name = row['reportingunitname']
    else:
        name = row['statename']

    if level.name in ['county', 'township']:
        kwargs['code'] = row['fipscode']
    else:
        kwargs['name'] = name

    return geography.Division.objects.get_or_create(**kwargs)[0]


def _get_or_create_election_cycle(row):
    year = row['electiondate'].split('-')[0]

    return election.ElectionCycle.objects.get_or_create(
        name=year
    )[0]


def _get_or_create_election_day(row, election_cycle):
    return election.ElectionDay.objects.get_or_create(
        date=row['electiondate'],
        cycle=election_cycle
    )[0]


def _get_or_create_jurisdiction(row):
    us = geography.Division.objects.get(code='00')

    if row['officename'] == 'Governor':
        state = geography.Division.objects.get(
            name=row['statename']
        )

        return entity.Jurisdiction.objects.get(
            division=state
        )

    else:
        return entity.Jurisdiction.objects.get(
            division=us,
            name='U.S. Federal Government'
        )


def _get_or_create_body(row, jurisdiction):
    if row['officename'] in ['President', 'Governor']:
        return None

    if 'house' in row['officename'].lower():
        full_name = 'U.S. House of Representatives'
        slug = 'house'
    elif 'senate' in row['officename'].lower():
        full_name = row['officename']
        slug = 'senate'
    else:
        full_name = row['officename']
        slug = slugify(row['officename'])

    return entity.Body.objects.get_or_create(
        slug=slug,
        label=full_name,
        name=full_name,
        jurisdiction=jurisdiction
    )[0]


def _get_or_create_office(row, body, division=None, jurisdiction=None):
    if row['officename'] == 'President':
        return entity.Office.objects.get(
            label='President',
            name='President of the United States'
        )

    office = '{0} {1}'.format(
        row['statename'],
        row['officename'],
    )

    if row['seatname']:
        office_label = '{0}, {1}'.format(office, row['seatname'])
    else:
        office_label = office

    if row['level'] not in ['state', 'national']:
        if row['fipscode'] == '02000':
            code = '02'
        else:
            code = division.code_components.get('fips').get('state')

        return entity.Office.objects.get(
            name=office_label,
            division__code=code,
        )

    return entity.Office.objects.get_or_create(
        slug=slugify(row['officename']),
        label=office_label,
        name=office_label,
        division=division,
        jurisdiction=jurisdiction,
        body=body
    )[0]


def _get_or_create_party(row):
    if row['party'] in ['Dem', 'GOP']:
        aggregable = False
    else:
        aggregable = True

    return election.Party.objects.get_or_create(
        ap_code=row['party'],
        name=row['party'],
        aggregate_candidates=aggregable
    )[0]


def _get_or_create_election_type(row):
    return election.ElectionType.objects.get_or_create(
        label=row['racetype'],
        name=row['racetype'],
        ap_code=row['racetypeid']
    )[0]


def _get_or_create_election(row, election_day, division, election_type, race):
    if row['level'] in ['state', 'national']:
        state = division
    else:
        if row['fipscode'] == '02000':
            state = geography.Division.objects.get(
                code='02'
            )
        else:
            state = geography.Division.objects.get(
                code=division.code_components.get('fips').get('state')
            )

    if election_type.label not in ['General', 'Runoff']:
        if election_type.ap_code in ['D', 'E']:
            party = election.Party.objects.get(ap_code='Dem')
        elif election_type.ap_code in ['R', 'S']:
            party = election.Party.objects.get(ap_code='GOP')
        else:
            party = None
    else:
        party = None

    return election.Election.objects.get_or_create(
        election_day=election_day,
        election_type=election_type,
        division=state,
        party=party,
        race=race
    )[0]


def _get_or_create_race(row, office, cycle):
    return election.Race.objects.get_or_create(
        office=office,
        cycle=cycle
    )[0]


def _get_or_create_person(row):
    return entity.Person.objects.get_or_create(
        first_name=row['first'],
        last_name=row['last']
    )[0]


def _get_or_create_candidate(row, person, party, race, election_obj):
    id_components = row['id'].split('-')
    candidate_id = '{0}-{1}'.format(
        id_components[1],
        id_components[2]
    )

    if party.ap_code in ['Dem', 'GOP']:
        aggregable = False
    else:
        aggregable = True

    defaults = {
        'party': party
    }

    return election.Candidate.objects.get_or_create(
        person=person,
        race=race,
        ap_candidate_id=candidate_id,
        defaults=defaults)[0]


def _get_or_create_candidate_election(row, election, candidate, party):
    if party.ap_code in ['Dem', 'GOP']:
        aggregable = False
    else:
        aggregable = True

    return election.update_or_create_candidate(candidate, aggregable)


def _get_or_create_ballot_measure(row, division, election_day):
    if row['level'] == 'state':
        state = division
    else:
        state = geography.Division.objects.get(
            code=division.code_components.get('fips').get('state')
        )

    return election.BallotMeasure.objects.get_or_create(
        question=row['seatname'],
        name=row['seatname'],
        division=state,
        election_day=election_day
    )[0]


def _get_or_create_ballot_answer(row, ballot_measure):
    return election.BallotAnswer.objects.get_or_create(
        answer=row['last'],
        name=row['last'],
        ballot_measure=ballot_measure
    )


def _get_or_create_ap_election_meta(row, election=None, ballot_measure=None):
    kwargs = {
        'ap_election_id': row['raceid']
    }

    if election:
        kwargs['election'] = election

    if ballot_measure:
        kwargs['ballot_measure'] = ballot_measure

    return vote.APElectionMeta.objects.get_or_create(**kwargs)[0]


def _get_or_create_votes(
    row, division, candidate_election=None, ballot_answer=None
):
    kwargs = {
        'division': division,
        'count': row['votecount'],
        'pct': row['votepct'],
        'winning': row['winner']
    }

    if candidate_election:
        kwargs['candidate_election'] = candidate_election

    if ballot_answer:
        kwargs['ballot_answer'] = ballot_answer

    return vote.Votes.objects.get_or_create(**kwargs)[0]


def process_row(row):
    print('Processing {0} {1} {2} {3}'.format(
        row['statename'],
        row['level'],
        row['last'],
        row['officename']
    ))

    level = _get_division_level(row)
    division = _get_division(row, level)
    election_cycle = _get_or_create_election_cycle(row)
    election_day = _get_or_create_election_day(row, election_cycle)

    if row['is_ballot_measure'] == 'True':
        ballot_measure = _get_or_create_ballot_measure(
            row, division, election_day
        )
        ballot_answer = _get_or_create_ballot_answer(row, ballot_measure)
        meta = _get_or_create_ap_election_meta(
            row, ballot_measure=ballot_measure
        )
    else:
        jurisdiction = _get_or_create_jurisdiction(row)
        body = _get_or_create_body(row, jurisdiction)
        office = _get_or_create_office(
            row, body, division=division, jurisdiction=jurisdiction
        )
        party = _get_or_create_party(row)
        election_type = _get_or_create_election_type(row)
        race = _get_or_create_race(row, office, election_cycle)
        election = _get_or_create_election(
            row, election_day, division, election_type, race
        )
        person = _get_or_create_person(row)
        candidate = _get_or_create_candidate(
            row, person, party, race, election
        )
        candidate_election = _get_or_create_candidate_election(
            row, election, candidate, party
        )
        meta = _get_or_create_ap_election_meta(row, election=election)
        votes = _get_or_create_votes(
            row, division, candidate_election=candidate_election
        )


class Command(BaseCommand):
    help = (
        'Bootstraps election meta models for all elections on an election date.'
    )

    def add_arguments(self, parser):
        parser.add_argument('election_date', type=str)

    def handle(self, *args, **options):
        writefile = open('bootstrap.json', 'w')
        elex_args = ['elex', 'results', options['election_date']]
        elex_args.extend(server_config.ELEX_FLAGS)
        subprocess.run(elex_args, stdout=writefile)

        with open('bootstrap.json', 'r') as readfile:
            data = json.load(readfile)
            for row in data:
                if row['level'] == 'township':
                    continue
                process_row(row)
