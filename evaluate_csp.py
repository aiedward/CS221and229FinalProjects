#!/usr/bin/env python
import sys
import csv
import csp_make_teams
our_teams_csv = 'teams_from_csp.csv'
their_teams_csv = 'teams_from_fsports.csv'
def main():
    #Make csv with teams from the thing for each day
    #make_teams_for_all_days()
    #make function to score from csv
    #our_scores = calculate_team_score(our_teams_csv)
    their_scores = calculate_team_score(their_teams_csv)
    our_scores = []
    #score both

    #do analysis about what the difference is!

#returns dict from date to scores
def calculate_team_score(teams_filename):
    result = {}
    with open(teams_filename) as teams_file:
        teams_reader = csv.reader(teams_file)
        for team in teams_reader:
            print "team was {}".format(team)
            date = team[0]
            total_score = 0
            with open('SalariesData/DKSalaries{}.csv'.format(date)) as dates:
                scores_reader = csv.DictReader(dates)
                for player in scores_reader:
                    if player["Name"] in team:
                        total_score += player["AvgPointsPerGame"]
            result[date] = total_score
    return result

def make_teams_for_all_days():
    with open(our_teams_csv, 'w+') as f:
        wr = csv.writer(f)
        data_files = ['SalariesData/DKSalaries11.{}.2015.csv'.format(i) for i in range(11, 14) + range(16,20) + [30]]
        data_files += ['SalariesData/DKSalaries12.{}.2015.csv'.format(i) for i in range(1,7)]
        print "number of successful files was {}".format(len(data_files))
        for data_file in data_files:
            output = csp_make_teams.make_teams(data_file)
            print "output was {}".format(output)

            team = output[0]
            print "team for {} was {}".format(data_file, team)
            row = team.values() + [output[1]]
            print "row was {}".format(row)
            wr.writerow(row)

if __name__ == "__main__":
    main()
