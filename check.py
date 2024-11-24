import requests

url = "https://reddit-scraper2.p.rapidapi.com/sub_posts"

querystring = {"sub":"indiehackers","sort":"NEW","time":"ALL"}

headers = {
	"x-rapidapi-key": "e8795eab86msh32bbf8663b8eac0p1df737jsn48e46471bb33",
	"x-rapidapi-host": "reddit-scraper2.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

for post in data['data']:
    print(post['title'])