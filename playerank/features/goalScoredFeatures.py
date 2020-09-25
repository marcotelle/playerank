from .abstract import Feature
from .wyscoutEventsDefinition import *
import json
from collections import defaultdict
import glob


class goalScoredFeatures(Feature):
    """
    goals scored by each team in each match
    """
    def createFeature(self,matches_path,select = None):
        """
        stores qualityFeatures on database
        parameters:
        -matches_path: file path of matches file
        -select: function  for filtering matches collection. Default: aggregate over all matches

        Output:
        list of documents in the format: match: matchId, entity: team, feature: feature, value: value
        """

        result =[]

        for id,match in matches_path.items():
            for team in [match.home_team, match.away_team]:
                document = {}
                document['match'] = id
                document['entity'] = team.team_id
                document['feature'] = 'goal-scored'
                document['value'] = team.score
                result.append(document)


        return result
