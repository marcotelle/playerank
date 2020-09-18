from .abstract import Feature
from .wyscoutEventsDefinition import *
import json
from collections import defaultdict
import glob

TOUCH_TAGS = [1401, 1302, 201, 1901, 1301, 2001, 301]
EVENTS = ['Duel', 'Foul', 'Free Kick', 'Goalkeeper leaving line', 'Offside', 'Others on the ball', 'Pass', 'Shot']

class qualityFeatures(Feature):
    """
    Quality features are the count of events with outcomes.
    E.g.
    - number of accurate passes
    - number of wrong passes
    ...
    """
    def createFeature(self,events_path,players_file,entity = 'team',select = None):
        """
        compute qualityFeatures
        parameters:
        -events_path: file path of events file
        -select: function  for filtering events collection. Default: aggregate over all events
        -entity: it could either 'team' or 'player'. It selects the aggregation for qualityFeatures among teams or players qualityfeatures

        Output:
        list of dictionaries in the format: matchId -> entity -> feature -> value
        """

        aggregated_features = defaultdict(lambda : defaultdict(lambda: defaultdict(int)))

        players =  json.load(open(players_file))
        #  filtering out all the events from goalkeepers
        goalkeepers_ids = [player['wyId'] for player in players
                                if player['role']['name']=='Goalkeeper']

        events = []
        for event in events_path:
            if event.period in ['1H','2H'] and event.player_id not in goalkeepers_ids:
                events.append(event)
        print ("[qualityFeatures] added %s events"%len(events))

        for evt in events:
            labelSplit = evt.label.split("-")
            if labelSplit[0] in EVENTS: 
                ent = evt.team_id
                if entity == 'player':
                    ent = evt.player_id
                

                aggregated_features[evt.match_id][ent]["%s"%evt.label]+=1

                '''
                # eventi OTHERS ON THE BALL 
                if labelSplit[0] == 'Others on the ball':
                    evtName = evt.label
                    tags = []
                    if labelSplit[1] == 'Touch':
                        for tag in evt.tags:
                            if tag in TOUCH_TAGS:
                                tags.append(tag)
                    elif labelSplit[1] in ['Acceleration', 'Clearance']:
                        for tag in evt.tags:
                            if tag == 101:
                                tags.append(tag)

                    if len(tags)>0:
                        for tag in tags:
                            aggregated_features[evt.match_id][ent]["%s-%s"%(evtName, tag2name[tag])]+=1
                    else:
                        aggregated_features[evt.match_id][ent]["%s"%(evtName)]+=1
                
                # eventi PASS
                elif labelSplit[0] == 'Pass':
                    evtName = evt.label
                    if evt.is_assist:
                        aggregated_features[evt.match_id][ent]["%s-assist"%evtName]+=1
                    if evt.is_keypass:
                        aggregated_features[evt.match_id][ent]["%s-key pass"%evtName]+=1

                # eventi FOUL
                elif labelSplit[0] == 'Foul':
                    evtName = labelSplit[0]

                    if evt.penalty_card != None:
                        aggregated_features[evt.match_id][ent]["%s-%s"%(evtName, evt.penalty_card)]+=1

                # eventi OFFSIDE
                elif labelSplit[0] == 'Offside':
                    evtName = evt.label
                    aggregated_features[evt.match_id][ent]["%s"%(evtName)]+=1

                # eventi DUEL, SHOT; FREE KICK
                else:
                    evtName = evt.label

                # tutti gli eventi con tag accurate, not accurate (tranne touch)
                if labelSplit[1] != 'Touch':
                    if evt.outcome == 'SUCCESS':
                        aggregated_features[evt.match_id][ent]["%s-accurate"%evtName]+=1
                    elif evt.outcome == 'FAILURE':
                        aggregated_features[evt.match_id][ent]["%s-not accurate"%evtName]+=1
                '''


        result =[]
        for match in aggregated_features:
            for entity in aggregated_features[match]:
                for feature in aggregated_features[match][entity]:
                    document = {}
                    document['match'] = match
                    document['entity'] = entity
                    document['feature'] = feature
                    document['value'] = aggregated_features[match][entity][feature]
                    result.append(document)

        return result