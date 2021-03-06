#!/usr/bin/env python
import sys
import csv
import csp_make_teams
import pandas as pd
import numpy as np
our_teams_csv = 'teams_from_csp.csv'
their_teams_csv = 'teams_from_fsports.csv'

def main():
    #make_teams_for_all_days()
    their_scores = calculate_team_score(their_teams_csv)
    scores = pd.read_csv(our_teams_csv)
    our_scores =scores.TotalPoints.tolist()
    scores['FantasyPoints'] = their_scores
    print "our scores was: {}".format(our_scores)
    print "their scores was: {}".format(their_scores)
    scores['diffScore'] = scores['TotalPoints'].sub(scores['FantasyPoints'], axis = 0)
    diff_mean = np.mean(scores.diffScore.tolist())
    their_mean = np.mean(scores.FantasyPoints.tolist())
    our_mean = np.mean(scores.TotalPoints.tolist())
    print "Their mean was {}".format(their_mean)
    print "Our mean was {}".format(our_mean)
    print "Mean difference was {}".format(diff_mean)
    print scores.diffScore

#returns dict from date to scores
def calculate_team_score(teams_filename):
    #result = {}
    result = []
    with open(teams_filename) as teams_file:
        teams_reader = csv.reader(teams_file)
        header = teams_reader.next()
        for team in teams_reader:
    #        print "team was {}".format(team)
            date = team[0]
            if not date: continue
            total_score = 0
            with open('SalariesData/DKSalaries{}.csv'.format(date)) as dates:
                scores_reader = csv.DictReader(dates)
                for player in scores_reader:
                    if player["Name"] in team:
                        total_score += float(player["AvgPointsPerGame"].replace("'",""))
            result.append(total_score)
    return result

def make_teams_for_all_days():
    with open(our_teams_csv, 'w+') as f:
        wr = csv.writer(f)
        data_files = ['SalariesData/DKSalaries11.{}.2015.csv'.format(i) for i in range(11, 14) + range(16,21) + [30]]
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
