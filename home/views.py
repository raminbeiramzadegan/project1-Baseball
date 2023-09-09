from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views import View
import requests


class HomeView(View):
    template_name = 'home/home.html'
    def news_crawler(self):

        url = "https://www.mlb.com/news"
        response = requests.get(url)
        news_list = []
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all('article')[:4]

            for article in articles:
                article_link = article.find("a",class_ ="p-button__link")
                headline = article.find("h1", class_="article-item__headline")
                article_date = article.find('div', class_='article-item__contributor-date')
                body = article.find('div', class_='article-item__preview')
                image = article.find('img')
                
                if image:
                    srcset = image.get("data-srcset")

                if srcset:
                    sources = srcset.split(',')

                    first = sources[0].strip().split(' ')[0]
                
                   
                    news = {
                            # 'article_id':article_id.get['id'] if article_id else '',
                            'headline': headline.get_text() if headline else '',
                            'image': first if first else '',
                            'date': article_date.get_text() if article_date else '',
                            'body': body.get_text() if body else '',
                            'link':article_link.get('href') if article_link else '',
                        }
                    
                    news_list.append(news)
                    
                    
        return news_list
    

    def get_mlb_standings_data(self,url):
        try:
            response = requests.get(url)

            if response.status_code == 200:

                data = response.json()
                standings = data['records']
                result = []
                

                for record in standings:
                    division_id = record['division']['id']
                    team_standings = record['teamRecords']

                    for team_record in team_standings:

                        team_name = team_record['team']['name']
                        team_id = team_record['team']['id']
                        words = team_name.split()
                        first_letters = [word[0] for word in words]
                        letters = ''.join(first_letters)
                        wins = team_record['records']['splitRecords'][0]['wins']
                        losses = team_record['records']['splitRecords'][0]['losses']  
                        games_back = team_record['gamesBack']
                        pct = team_record['records']['splitRecords'][0]['pct']  
                        last_10 = team_record['records']['splitRecords'][8]['wins']  
                        run_diff = team_record['runDifferential']

                        team_data = {
                             
                            'team_name':team_name,
                            'id': division_id,
                            'team': letters,
                            'wins': wins,
                            'losses': losses,
                            'games_back': games_back,
                            'pct': pct,
                            'last_ten_wins': last_10,
                            'run_differential': run_diff,
                            'team_id':team_id,

                        }

                        result.append(team_data)

                return result

            else:
                print(f"Request failed with status code {response.status_code}")
                return []

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return []

    def logos_crawler(self):
            
            url = "https://www.mlb.com/news"
            response = requests.get(url)
            logos_list = []
            names_list = []
            team_info = {}
            get_list  = get_team_choices()
        
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                team_logo = soup.find_all('a',class_='header__subnav__item header__subnav--teams__team')[:30]
                for nav in team_logo:
                
                        img = nav.find('img',class_="header__subnav--teams__team--logo")
                        logo = "https:"+ img.get('src')
                        logos_list.append(logo)
                        i = 0
                        for i in range(len(logos_list)):
                            team_info[get_list[i][0]] = logos_list[i]

            return team_info
 



    def get(self,request):
        url = "https://statsapi.mlb.com//api/v1/standings?leagueId=103,104"
        standings = self.get_mlb_standings_data(url)

        news_list = self.news_crawler()
        team_info = self.logos_crawler()
     
        context={
            'news_list': news_list,
            'standings':standings,
            'team_info':team_info,
        }
        return render(request, self.template_name,context)
    














def get_team_choices():
        url = "https://www.mlb.com/news"
        team_choices = []

        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                team_names = soup.find_all('a', class_='header__subnav__item header__subnav--teams__team')[:30]

                for names in team_names:
                    name = names.find('span', class_="header__subnav--teams__team--name")
                    team_name = name.get_text()
                    team_choices.append((team_name, team_name))  # Append a tuple with the same value for both display and value

            return team_choices
        
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return [] 