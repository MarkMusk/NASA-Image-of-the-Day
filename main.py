from flask import Flask, render_template, request, redirect
from time import gmtime, strftime
from random import randrange
from datetime import timedelta, datetime
from datetime import date, datetime, timedelta
import requests
from secret import access_secret_version
import pandas as pd

#TOKEN = "FmptTtOk1l6AyRVaryN0hg9nPOabgkZcy0SPLowo"
TOKEN = access_secret_version(project_id="websites-378423", secret_id="NASA-Gallery-APOD-API-Key", version_id="1")

def crop_text(text: str, limit: int) -> str:
    if len(text) > limit:
        return text[:limit - 3] + '...'
    else:
        return text

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return str(start + timedelta(seconds=random_second)).split()[0]

app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={TOKEN}')
    response_json = response.json()
    today = str(datetime.strptime(strftime("%Y-%m-%d", gmtime()), '%Y-%m-%d')).split(' ')[0]
    if str(response) != '<Response [200]>':
        return render_template('nasagalleryerror.html')
    response_json = response.json()
    if 'hdurl' in response_json:
        img = response_json['hdurl']
    elif 'url' in response_json:
        img = response_json['url']
    else:
        return render_template('nasagalleryerror.html', image=img, date=randomDate)
    desc = ''
    if 'explanation' in response_json:
        desc += response_json['explanation']
    return render_template('nasagallery.html', image=img, description=desc, date=today)

@app.route('/about')
def about():
    while True:
        d1 = datetime.strptime('1995/6/16', '%Y/%m/%d')
        d2 = datetime.strptime(strftime("%Y/%m/%d", gmtime()), '%Y/%m/%d')
        randomDate = random_date(d1, d2)
        response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={TOKEN}&date={randomDate}')
        if str(response) == '<Response [200]>' or 'hdurl' not in response:    
            response_json = response.json()
            if 'hdurl' in response_json:
                img = response_json['hdurl']
                return render_template('nasagalleryabout.html', image=img, date=randomDate)
            elif 'url' in response_json:
                img = response_json['url']
                return render_template('nasagalleryabout.html', image=img, date=randomDate)

@app.route('/q&a')
def QandA():
    d1 = datetime.strptime('1995/6/16', '%Y/%m/%d')
    d2 = datetime.strptime(strftime("%Y/%m/%d", gmtime()), '%Y/%m/%d')
    randomDate = random_date(d1, d2)
    response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={TOKEN}&date={randomDate}')
    if str(response) == '<Response [200]>' or 'hdurl' not in response:    
        response_json = response.json()
        if 'hdurl' in response_json:
            img = response_json['hdurl']
            return render_template('nasagalleryQandA.html', image=img, date=randomDate)
        elif 'url' in response_json:
            img = response_json['url']
            return render_template('nasagalleryQandA.html', image=img, date=randomDate)

@app.route('/contact')
def contact():
    d1 = datetime.strptime('1995/6/16', '%Y/%m/%d')
    d2 = datetime.strptime(strftime("%Y/%m/%d", gmtime()), '%Y/%m/%d')
    randomDate = random_date(d1, d2)
    response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={TOKEN}&date={randomDate}')
    while True:
        if str(response) == '<Response [200]>' or 'hdurl' not in response:    
            response_json = response.json()
        if 'hdurl' in response_json:
            img = response_json['hdurl']
            return render_template('nasagallerycontact.html', image=img, date=randomDate)
        elif 'url' in response_json:
            img = response_json['url']
            return render_template('nasagallerycontact.html', image=img, date=randomDate)

@app.route('/random')
def random():
    d1 = datetime.strptime('1995/6/16', '%Y/%m/%d')
    d2 = datetime.strptime(strftime("%Y/%m/%d", gmtime()), '%Y/%m/%d')
    date = random_date(d1, d2)
    response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={TOKEN}&date={date}')
    if str(response) != '<Response [200]>':
        return render_template('nasagalleryerror.html')
    response_json = response.json()
    if 'hdurl' in response_json:
        img = response_json['hdurl']
    elif 'url' in response_json:
        img = response_json['url']
    else:
        return render_template('nasagalleryerror.html')
    desc = ''
    if 'explanation' in response_json:
        desc += response_json['explanation']
    return render_template('nasagallery.html', image=img, description=desc, date=date)

@app.route('/gallery')
def gallery():
    s = request.args.get('start')
    e = query = request.args.get('end')
    images = []
    if s and e:
        d0 = datetime.strptime(s,"%Y-%m-%d")
        d1 = datetime.strptime(e, "%Y-%m-%d")
        l = []
        for days in range((d1 - d0).days):
            date = str((d0 + timedelta(days)).date())
            response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={TOKEN}&date={date}')
            if str(response) == '<Response [200]>':
                response_json = response.json()
                if 'hdurl' in response_json:
                    desc = ''
                    if 'explanation' in response_json:
                        desc += response_json['explanation']
                    img = response_json['hdurl']
                    desc = crop_text(text=desc, limit=100)
                    images.append([img, desc, desc, f"/search?q={str(date)}"])
                elif 'url' in response_json:
                    desc = ''
                    if 'explanation' in response_json:
                        desc += response_json['explanation']
                    img = response_json['url']
                    desc = crop_text(text=desc, limit=100)
                    images.append([img, desc, desc, f"/search?q={str(date)}", date])
    return render_template('nasagallerygallery.html', images=images)

@app.route("/search")
def search():
    query = request.args.get('q')
    if query != '':
        date = datetime.strptime(query, '%Y-%m-%d')
        today = datetime.strptime(strftime("%Y-%m-%d", gmtime()), '%Y-%m-%d')
        if date < datetime.strptime("1995-6-16", "%Y-%m-%d") or date > today:
            return render_template('nasagallerydatenotfound.html')
        response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={TOKEN}&date={query}')
        if str(response) != '<Response [200]>':
            return render_template('nasagalleryerror.html')
        response_json = response.json()
        if 'hdurl' in response_json:
            img = response_json['hdurl']
        elif 'url' in response_json:
            img = response_json['url']
        else:
            return render_template('nasagalleryerror.html')
        desc = ''
        if 'explanation' in response_json:
            desc += response_json['explanation']
        return render_template('nasagallery.html', image=img, description=desc, date=str(date).split()[0])
    else:
        return render_template('nasagallerydatenotfound.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)