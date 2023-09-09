from django.shortcuts import render,redirect
from django.views import View
import requests

from home.views import HomeView
import requests
import json

# Define the URL




class PitchersTeamView(View):
    template_name = 'teamview/team.html'
    def pitchingteams(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                roster = data.get('roster', []) 
                print("--------")
                for ros in roster:
                    print(ros['person']['stats'][0]['splits'][0]['player'])
                print("--------")
                player_data = []
                for player in data['roster']:
                    jerseyNumber = player['jerseyNumber']
                    parentTeamId = player['parentTeamId']
                    person = player['person']
                    stats = player['person']['stats'][0]['splits'][0]['stat']

                    player_name = person['fullName']
                    player_num = jerseyNumber
                    
                    position = person['primaryPosition']['abbreviation']
                    position_name = person['primaryPosition']['name']
                    current_age = person['currentAge']
                    ops = stats['ops']
                    player_id = person['id']
                    # era =stats['era']
                    home_runs = stats['homeRuns']
                    strike_outs = stats['strikeOuts']
                    current_age = person['currentAge']
                    obp =stats['obp']
                    triples = stats['triples']
                    base_on_balls = stats['baseOnBalls']
                    hits = stats['hits']
                    avg = stats['avg']
                    # babip = stats['babip']
                    sac_bunts = stats['sacBunts']


                    player_info = {
                        'player_name':player_name,
                        'player_num':player_num,

                        'player_id':player_id,
                        'position': position ,
                        'position_name':position_name,

                        # 'team_name': team_name,
                        'current_age': current_age,
                        'ops': ops,
                        'team_Id': parentTeamId,
                        # 'era': era,
                        'home_runs': home_runs,
                        'strike_outs': strike_outs,
                        'obp': obp,
                        'triples': triples,
                        'base_on_balls': base_on_balls,
                        'hits':hits,
                        'avg': avg,
                        # 'position_type': person['position']['type'],
                        # 'babip': babip,
                        'sac_bunts': sac_bunts,
        }
                    player_data.append(player_info)

                return player_data
                
            except ValueError as e:
                print(f"Error parsing JSON: {e}")
        else:
                print(f"Request failed with status code {response.status_code}")

       
    

    def get(self,request):
            url = "https://statsapi.mlb.com/api/v1/teams/141/roster/Active?hydrate=person(stats(type=season))"
            myclass = HomeView()
            logos = myclass.logos_crawler()
            pitchingteams_data = self.pitchingteams(url)
            

            context = {
                'pitch':pitchingteams_data,
                'request':request,
                'logos':logos,
            }

            return render(request,self.template_name,context)


class HittersTeamView(View):
    template_name = 'teamview/team.html'
    
    # def hittingteams(self, url):
    #     response = requests.get(url)
    #     hitting_data = []

    #     if response.status_code == 200:
    #         try:
    #             data = response.json()
    #             people = data['people'][0]['stats'][0]['splits']
                
    #             for player_data in people:
    #                 player_name = player_data['player']['fullName']
    #                 player_id = player_data['player']['id']
    #                 # position = player_data['position']['abbreviation']
    #                 team_name = player_data['team']['name']

    #                 hitting_teams = {
    #                     'player_name': player_name,
    #                     'id': player_id,
    #                     # 'position': position,
    #                     'team_name': team_name,
    #                 }
    #                 hitting_data.append(hitting_teams)
    #         except ValueError as e:
    #             print(f"Error parsing JSON: {e}")
    #     else:
    #         print(f"Request failed with status code {response.status_code}")

    #     return hitting_data

                    
        
        
    def get(self,request):
            url = "https://statsapi.mlb.com/api/v1/teams/141/roster/Active?hydrate=person(stats(type=season))"
            myclass = HomeView()
            logos = myclass.logos_crawler()
            pitch_class = PitchersTeamView()
            hittingteams_data = pitch_class.pitchingteams(url)
       
            context = {
                'hitting':hittingteams_data,
                'request':request,
                'logos':logos,
            }
            return render(request,self.template_name,context)
        



