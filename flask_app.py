# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask import jsonify
from flask.ext.mail import Message, Mail
from decorators import async

mail = Mail()

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'password'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'youremailaddress'
app.config["MAIL_PASSWORD"] = 'yourpassword'

mail.init_app(app)

ADMINS = ['youremailaddress']
if not app.debug:
    import logging
    from logging import Formatter
    import logging.handlers

    class TlsSMTPHandler(logging.handlers.SMTPHandler):
        def emit(self, record):
            try:
                import smtplib
                import string
                try:
                    from email.utils import formatdate
                except ImportError:
                    formatdate = self.date_time
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                msg = self.format(record)
                msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                                self.fromaddr,
                                string.join(self.toaddrs, ","),
                                self.getSubject(record),
                                formatdate(), msg)
                if self.username:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(self.username, self.password)
                smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                smtp.quit()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)

    logger = logging.getLogger()

    gm = TlsSMTPHandler(("smtp.gmail.com", 587), 'Marvel_Reco_Engine@underminer.net', ADMINS, 'Error found!', ('youremailaddress', 'yourpassword'))
    gm.setLevel(logging.ERROR)
    gm.setFormatter(Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''))

    logger.addHandler(gm)

@app.route('/autofill', methods=['GET'])
def autofill():
    import json
    query = request.args['term']
    with app.open_resource('/home/balkey/marvel/static/autofill2.json') as f:
        contents = json.loads(f.read())

    matching = [s for s in contents if query.lower() in s.lower()]
    matching_first = []
    matching_last = []

    for i in matching:
        if i.lower().startswith(query.lower()):
		    matching_first.append(i)
        else:
		    matching_last.append(i)

    matching_first.extend(matching_last)

    return json.dumps(matching_first)

@app.route('/characters', methods=['GET'])
def chars_autofill():
    import json
    query = request.args['term']
    with app.open_resource('/home/balkey/marvel/static/characters.json') as f:
        contents = json.loads(f.read())

    matching = [s for s in contents if query.lower() in s.lower()]
    matching_first = []
    matching_last = []

    for i in matching:
        if i.lower().startswith(query.lower()):
		    matching_first.append(i)
        else:
		    matching_last.append(i)

    matching_first.extend(matching_last)

    return json.dumps(matching_first)

@app.route('/words', methods=['GET'])
def words_autofill():
    import json
    query = request.args['term']
    with app.open_resource('/home/balkey/marvel/static/d3/alice_count.json') as f:
        contents = json.loads(f.read())

    matching = [s['key'] for s in contents if query.lower() in s['key']]
    if len(matching) != 0:
        matching_first = []
        matching_last = []
        for i in matching:
            if i.lower().startswith(query.lower()):
		        matching_first.append(i)
            else:
		        matching_last.append(i)
        matching_first.extend(matching_last)
        return json.dumps(matching_first)
    else:
        return json.dumps(["No results found!"])

@app.route('/words_update', methods=['GET', 'POST'])
def words_update():
    import json
    a = request.args.get('a', 0, type=str)
    with app.open_resource('/home/balkey/marvel/static/d3/alice_count.json') as f:
        contents = json.loads(f.read())
    matching = [s for s in contents if a.lower() == s['key']]
    if len(matching) != 0:
        return json.dumps(matching[0])
    else:
        return json.dumps([])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_unhandled_exception(error):
    return render_template('500.html'), 500

@app.route('/')
def hello ():
    import requests
    from datetime import datetime
    import random
    import re
    year_start = random.choice(range(1940, 2012))
    month_start = random.choice(range(1, 12))
    day_start = random.choice(range(1, 28))
    yearstart2 = year_start + 1
    year_end = random.choice(range(yearstart2, 2014))
    month_end = random.choice(range(1, 12))
    day_end = random.choice(range(1, 28))

    startDate1 = datetime(year_start, month_start, day_start)
    endDate1 = datetime(year_end, month_end, day_end)

    startDate = datetime.date(startDate1)
    endDate = datetime.date(endDate1)

    comic_query = {'ts': '1',
	               'hash': 'yourhash',
		           'format': 'comic',
		           'formatType': 'comic',
		           'limit': '1',
		           'apikey': 'yourapikey',
		           'dateRange': str(startDate)+","+str(endDate)
		           }

    headers = {'Accept-Encoding': 'gzip'}

    r = requests.get('http://gateway.marvel.com/v1/public/comics', params=comic_query, headers=headers)

    z = r.json()

    if r.status_code == 429:
        return render_template('429.html')
    else:
        pass

    thumbnail = z.get("data").get("results")[0].get("thumbnail").get("path")+"/portrait_uncanny.jpg"
    link = z.get("data").get("results")[0].get("urls")[0].get("url")
    comic_series = z.get("data").get("results")[0].get("series").get("name")
    issue_number = z.get("data").get("results")[0].get("issueNumber")
    publication_date1 = z.get("data").get("results")[0].get("dates")[0].get("date")[:10].strip("-")
    if len(publication_date1) == 9:
        publication_date1 = "1940-01-01"
    publication_date = datetime.strptime(publication_date1, "%Y-%m-%d").strftime("%B %d, %Y")
    creators_count = z.get("data").get("results")[0].get("creators").get("returned")
    characters_count = z.get("data").get("results")[0].get("characters").get("returned")
    digital_id = z.get("data").get("results")[0].get("digitalId")
    character_list = []
    character_id = []
    creator_list = []
    creator_role = []
    creator_id = []
    creator_dictionary = {}

    def character_id_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    character_id.append(i.get("resourceURI").split("/")[-1])

    character_id_append(z.get("data").get("results")[0].get("characters").get("items")[:characters_count])

    def creator_id_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    creator_id.append(i.get("resourceURI").split("/")[-1])

    creator_id_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

    def creator_role_append(lista):
	if len(lista) != 0:
		for i in lista:
			creator_role.append(i.get("role"))
	else:
		creator_role.append("Unknown")

    creator_role_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

    def creator_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    creator_list.append(i.get("name"))
	    else:
		    creator_list.append("Unknown")

    creator_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

    creator_role = [word.replace("penciller (cover)", "cover") for word in creator_role]
    creator_role = [word.replace("penciler (cover)", "cover") for word in creator_role]
    creator_role = [word.replace("penciler", "penciller") for word in creator_role]
    creator_role = [word.replace(word[0], word[0].upper()) for word in creator_role]

    for q, a in zip(creator_role, creator_list):
        creator_dictionary.setdefault(q,[]).append(a)

    def character_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    character_list.append(i.get("name"))
	    else:
		    character_list.append("Unknown")

    character_append(z.get("data").get("results")[0].get("characters").get("items")[:characters_count])

    a = z.get("data").get("results")[0].get("textObjects")
    description_list = []


    def description_check():
        if not a:
            description_list.insert(0, "There is no description for this issue yet in the Marvel database.")
        else:
            description_list.insert(0, z.get("data").get("results")[0].get("textObjects")[0].get("text"))

    def replacer (rep, text):
	    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
	    pattern = re.compile("|".join(rep.keys()))
	    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
	    return text

    char_repl = {"<br>": "",
	       		 "&bull; ": "",
	    		 "<ul>": "",
	     		 "<li>": "",
	    	 	 "</ul>": "",
	    		 "</li>": "",
	    		 "</br": "",
	    		 "&rsquo;": "'",
	    		 "&hellip;": "...",
	    		 "&mdash;": "-",
	    		 "--": " - ",
	    		 "<br />": "",
	    		 "&ldquo;": '"',
	    		 "&rdquo;": '"',
	    		 "&#39;": "'",
                u"•": "\n",
                u"—": " - ",
                u"�": "",
                "&#133;": "...",
                u"ï¿½": "'"}

    description_check()
    description = replacer(char_repl, description_list[0])

    shared_collaborator = []
    shared_appearances_list = []

    true_artists = ["writer", "artist", "penciller", "penciler", "penciler (cover)", "penciller (cover)", "artist (cover", "inker", "colorist"]

    def creator_shared_append(lista):
	    for i in lista:
		    if len(lista) != 0 and any(substring in i.get("role") for substring in true_artists):
			    shared_collaborator.append(i.get("resourceURI").split("/")[-1])
		    else:
			    pass

    creator_shared_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])


    def shared_appearances():
	    if 2 <= len(character_list) <=10:
		    shared_appearances_list.append(character_id)

    shared_appearances()

    def decade_checker2(input_date2):
        x = int(input_date2[0:4])
        if x < 1950:
            return "1940-01-01,1950-12-31"
        elif x < 2004:
            return str(x-10)+"-01-01,"+str(x+10)+"-12-12"
        else:
            return "2004-01-01,2014-05-13"

    reco_range = decade_checker2(publication_date1)

    recommendation_query = {'ts': '1',
	                        'hash': 'yourhash',
		                    'format': 'comic',
		                    'formatType': 'comic',
		                    'limit': '9',
		                    'creators': creator_id[:10],
		                    'noVariants': "true",
		                    'orderBy': "-onsaleDate",
		                    'characters': character_id[:10],
		                    'sharedAppearances': shared_appearances_list[:10],
		                    'collaborators': shared_collaborator[:10],
		                    'dateRange': reco_range,
		                    'apikey': 'yourapikey',
		                    }

    headers_reco = {'Accept-Encoding': 'gzip'}

    recommendation = requests.get('http://gateway.marvel.com/v1/public/comics', params=recommendation_query, headers=headers_reco)

    reco = recommendation.json()

    reco_thumbnails = []
    reco_ids =[]
    reco_titles = []
    reco_issue_nr = []
    reco_dictionary = {}

    def reco_thumbnails_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_thumbnails.append(i.get("thumbnail").get("path"))

    def reco_ids_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_ids.append(i.get("id"))

    def reco_titles_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_titles.append(i.get("series").get("name"))

    def reco_issue_nr_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_issue_nr.append(i.get("issueNumber"))

    reco_count = reco["data"]["count"]

    if reco_count is None:
        reco_count == 0

    reco_thumbnails_append(reco.get("data").get("results")[:reco_count])
    reco_ids_append(reco.get("data").get("results")[:reco_count])
    reco_titles_append(reco.get("data").get("results")[:reco_count])
    reco_issue_nr_append(reco.get("data").get("results")[:reco_count])

    for q, a, v, s in zip(reco_ids, reco_titles, reco_thumbnails, reco_issue_nr):
        reco_dictionary[q] = [a, v, s]

    return render_template('about.html', thumbnail=thumbnail, link=link, comic_series=comic_series, issue_number=issue_number, publication_date=publication_date, character_list=character_list, description=description, digital_id=digital_id, creator_dictionary=creator_dictionary, reco_thumbnails=reco_thumbnails, reco_dictionary=reco_dictionary)

@app.route('/recommendation', methods=['GET'])
def recommendation():
    a = request.args['l']
    import requests
    from datetime import datetime
    import re

    comic_query = {'ts': '1',
	               'hash': 'yourhash',
		           'apikey': 'yourapikey'
		           }

    headers = {'Accept-Encoding': 'gzip'}

    r = requests.get('http://gateway.marvel.com/v1/public/comics/'+str(a), params=comic_query, headers=headers)

    z = r.json()

    thumbnail = z.get("data").get("results")[0].get("thumbnail").get("path")+"/portrait_uncanny.jpg"
    link = z.get("data").get("results")[0].get("urls")[0].get("url")
    comic_series = z.get("data").get("results")[0].get("series").get("name")
    issue_number = z.get("data").get("results")[0].get("issueNumber")
    publication_date1 = z.get("data").get("results")[0].get("dates")[0].get("date")[:10].strip("-")
    if len(publication_date1) == 9:
        publication_date1 = "1940-01-01"
    publication_date = datetime.strptime(publication_date1, "%Y-%m-%d").strftime("%B %d, %Y")
    creators_count = z.get("data").get("results")[0].get("creators").get("returned")
    characters_count = z.get("data").get("results")[0].get("characters").get("returned")
    digital_id = z.get("data").get("results")[0].get("digitalId")
    character_list = []
    character_id = []
    creator_list = []
    creator_id = []
    creator_role = []
    creator_dictionary = {}

    def character_id_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    character_id.append(i.get("resourceURI").split("/")[-1])

    character_id_append(z.get("data").get("results")[0].get("characters").get("items")[:characters_count])

    def creator_id_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    creator_id.append(i.get("resourceURI").split("/")[-1])

    creator_id_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

    def creator_role_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    creator_role.append(i.get("role"))
	    else:
		    creator_list.append("Unknown")

    creator_role_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

    def creator_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    creator_list.append(i.get("name"))
	    else:
		    creator_list.append("Unknown")

    creator_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

    creator_role = [word.replace("penciller (cover)", "cover") for word in creator_role]
    creator_role = [word.replace("penciler (cover)", "cover") for word in creator_role]
    creator_role = [word.replace("penciler", "penciller") for word in creator_role]
    creator_role = [word.replace(word[0], word[0].upper()) for word in creator_role]

    for q, a in zip(creator_role, creator_list):
        creator_dictionary.setdefault(q,[]).append(a)

    def character_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    character_list.append(i.get("name"))
	    else:
		    character_list.append("Unknown")

    character_append(z.get("data").get("results")[0].get("characters").get("items")[:characters_count])

    a = z.get("data").get("results")[0].get("textObjects")
    description_list = []


    def description_check():
        if not a:
            description_list.insert(0, "There is no description for this issue yet in the Marvel database.")
        else:
            description_list.insert(0, z.get("data").get("results")[0].get("textObjects")[0].get("text"))

    def replacer (rep, text):
	    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
	    pattern = re.compile("|".join(rep.keys()))
	    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
	    return text

    char_repl = {"<br>": "",
	       		 "&bull; ": "",
	    		 "<ul>": "",
	     		 "<li>": "",
	    	 	 "</ul>": "",
	    		 "</li>": "",
	    		 "</br": "",
	    		 "&rsquo;": "'",
	    		 "&hellip;": "...",
	    		 "&mdash;": "-",
	    		 "--": " - ",
	    		 "<br />": "",
	    		 "&ldquo;": '"',
	    		 "&rdquo;": '"',
	    		 "&#39;": "'",
	    		 u"•": "\n",
                u"—": " - ",
                u"�": "",
                "&#133;": "...",
                u"ï¿½": "'"}

    description_check()
    description = replacer(char_repl, description_list[0])

    shared_collaborator = []
    shared_appearances_list = []

    true_artists = ["writer", "artist", "penciller", "penciler", "penciler (cover)", "penciller (cover)", "artist (cover", "inker", "colorist"]

    def creator_shared_append(lista):
	    for i in lista:
		    if len(lista) != 0 and any(substring in i.get("role") for substring in true_artists):
			    shared_collaborator.append(i.get("resourceURI").split("/")[-1])
		    else:
			    pass

    creator_shared_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])


    def shared_appearances():
	    if 2 <= len(character_list) <=10:
		    shared_appearances_list.append(character_id)

    shared_appearances()

    recommendation_query = {'ts': '1',
	                        'hash': 'yourhash',
		                    'format': 'comic',
		                    'formatType': 'comic',
		                    'limit': '9',
		                    'creators': creator_id[:10],
		                    'noVariants': "true",
		                    'orderBy': "-onsaleDate",
		                    'characters': character_id[:10],
		                    'sharedAppearances': shared_appearances_list[:10],
		                    'collaborators': shared_collaborator[:10],
		                    'dateRange': "1940-01-01,2014-05-11",
		                    'apikey': 'yourapikey',
		                    }

    headers_reco = {'Accept-Encoding': 'gzip'}

    recommendation = requests.get('http://gateway.marvel.com/v1/public/comics', params=recommendation_query, headers=headers_reco)

    reco = recommendation.json()

    reco_thumbnails = []
    reco_ids =[]
    reco_titles = []
    reco_issue_nr = []
    reco_dictionary = {}

    def reco_thumbnails_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_thumbnails.append(i.get("thumbnail").get("path"))

    def reco_ids_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_ids.append(i.get("id"))

    def reco_titles_append(lista):
        if len(lista) != 0:
            for i in lista:
                reco_titles.append(i.get("series").get("name"))

    def reco_issue_nr_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_issue_nr.append(i.get("issueNumber"))

    reco_count = reco["data"]["count"]

    if reco_count is None:
        reco_count == 0

    reco_thumbnails_append(reco.get("data").get("results")[:reco_count])
    reco_ids_append(reco.get("data").get("results")[:reco_count])
    reco_titles_append(reco.get("data").get("results")[:reco_count])
    reco_issue_nr_append(reco.get("data").get("results")[:reco_count])

    for q, a, v, s in zip(reco_ids, reco_titles, reco_thumbnails, reco_issue_nr):
        reco_dictionary[q] = [a, v, s]

    return render_template('about.html', thumbnail=thumbnail, link=link, comic_series=comic_series, issue_number=issue_number, publication_date=publication_date, character_list=character_list, description=description, digital_id=digital_id, creator_dictionary=creator_dictionary, reco_thumbnails=reco_thumbnails, reco_dictionary=reco_dictionary)


@app.route('/uat', methods=['GET', 'POST'])

def uat ():
    import requests
    from datetime import datetime
    import random
    import re

    year_start = random.choice(range(1940, 2012))
    month_start = random.choice(range(1, 12))
    day_start = random.choice(range(1, 28))
    yearstart2 = year_start + 1
    year_end = random.choice(range(yearstart2, 2014))
    month_end = random.choice(range(1, 12))
    day_end = random.choice(range(1, 28))

    startDate1 = datetime(year_start, month_start, day_start)
    endDate1 = datetime(year_end, month_end, day_end)

    startDate = datetime.date(startDate1)
    endDate = datetime.date(endDate1)

    comic_query = {'ts': '1',
	               'hash': 'yourhash',
		           'format': 'comic',
		           'formatType': 'comic',
		           'noVariants': 'true',
		           'limit': '5',
		           'apikey': 'yourapikey',
		           'dateRange': str(startDate)+","+str(endDate)
		           }

    headers = {'Accept-Encoding': 'gzip'}

    r = requests.get('http://gateway.marvel.com/v1/public/comics', params=comic_query, headers=headers)

    z = r.json()

    if r.status_code == 429:
        return render_template('429.html')
    else:
        pass

    picture_counter = 0
    thumbnail_test = z.get("data").get("results")[0].get("thumbnail").get("path")+".jpg"

    while thumbnail_test == "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg":
        picture_counter = picture_counter + 1
        thumbnail_test = z.get("data").get("results")[picture_counter].get("thumbnail").get("path")+".jpg"
        if picture_counter == 4:
            break

    if thumbnail_test == "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg":
        thumbnail = "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available/portrait_uncanny.jpg"
    else:
        thumbnail = thumbnail_test
    link = z.get("data").get("results")[picture_counter].get("urls")[0].get("url")
    comic_series = z.get("data").get("results")[picture_counter].get("series").get("name")
    issue_number = z.get("data").get("results")[picture_counter].get("issueNumber")
    publication_date1 = z.get("data").get("results")[picture_counter].get("dates")[0].get("date")[:10].strip("-")
    if len(publication_date1) == 9:
        publication_date1 = "Unknown"
    if publication_date1 != "Unknown":
        publication_date = datetime.strptime(publication_date1, "%Y-%m-%d").strftime("%B %d, %Y")
    else:
        publication_date = publication_date1
    creators_count = z.get("data").get("results")[picture_counter].get("creators").get("returned")
    characters_count = z.get("data").get("results")[picture_counter].get("characters").get("returned")
    id_original = z.get("data").get("results")[picture_counter].get("id")
    digital_id = z.get("data").get("results")[picture_counter].get("digitalId")
    series = z.get("data").get("results")[picture_counter].get("series").get("resourceURI").split("/")[-1]
    character_list = []
    character_id = []
    creator_list = []
    creator_role = []
    creator_id = []
    creator_dictionary = {}

    def character_id_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    character_id.append(i.get("resourceURI").split("/")[-1])

    character_id_append(z.get("data").get("results")[picture_counter].get("characters").get("items")[:characters_count])

    def creator_id_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    creator_id.append(i.get("resourceURI").split("/")[-1])

    creator_id_append(z.get("data").get("results")[picture_counter].get("creators").get("items")[:creators_count])

    def creator_role_append(lista):
	if len(lista) != 0:
		for i in lista:
			creator_role.append(i.get("role"))
	else:
		creator_role.append("Unknown")

    creator_role_append(z.get("data").get("results")[picture_counter].get("creators").get("items")[:creators_count])

    def creator_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    creator_list.append(i.get("name"))
	    else:
		    creator_list.append("Unknown")

    creator_append(z.get("data").get("results")[picture_counter].get("creators").get("items")[:creators_count])

    creator_role = [word.replace("penciller (cover)", "cover") for word in creator_role]
    creator_role = [word.replace("penciler (cover)", "cover") for word in creator_role]
    creator_role = [word.replace("penciler", "penciller") for word in creator_role]
    creator_role = [word.replace(word[0], word[0].upper()) for word in creator_role]

    for q, a in zip(creator_role, creator_list):
        creator_dictionary.setdefault(q,[]).append(a)

    def character_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    character_list.append(i.get("name"))
	    else:
		    character_list.append("Unknown")

    character_append(z.get("data").get("results")[picture_counter].get("characters").get("items")[:characters_count])

    a = z.get("data").get("results")[picture_counter].get("textObjects")
    description_list = []


    def description_check():
        if not a:
            description_list.insert(0, "There is no description for this issue yet in the Marvel database.")
        else:
            description_list.insert(0, z.get("data").get("results")[picture_counter].get("textObjects")[0].get("text"))

    def replacer (rep, text):
	    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
	    pattern = re.compile("|".join(rep.keys()))
	    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
	    return text

    char_repl = {"<br>": "",
	       		 "&bull; ": "",
	    		 "<ul>": "",
	     		 "<li>": "",
	    	 	 "</ul>": "",
	    		 "</li>": "",
	    		 "</br": "",
	    		 "&rsquo;": "'",
	    		 "&hellip;": "...",
	    		 "&mdash;": "-",
	    		 "&ndash;": "-",
	    		 "--": " - ",
	    		 "<br />": "",
	    		 "&ldquo;": '"',
	    		 "&rdquo;": '"',
	    		 "&#39;": "'",
                u"•": "\n",
                u"—": " - ",
                u"�": "",
                "&#133;": "...",
                u"ï¿½": "'",
                u"â€¢ ": "",
                '&quot;': '"',
                u"â€™": "'",
                "%^$%^%$%^": ""}

    description_check()
    description = replacer(char_repl, description_list[0])

    shared_collaborator = []
    shared_appearances_list = []

    true_artists = ["writer", "artist", "penciller", "penciler", "penciler (cover)", "penciller (cover)", "artist (cover"]

    def creator_shared_append(lista):
	    for i in lista:
		    if len(lista) != 0 and any(substring in i.get("role") for substring in true_artists):
			    shared_collaborator.append(i.get("resourceURI").split("/")[-1])
		    else:
			    pass

    creator_shared_append(z.get("data").get("results")[picture_counter].get("creators").get("items")[:creators_count])

    def shared_appearances():
	    if 2 <= len(character_list) <=10:
		    shared_appearances_list.extend(character_id)

    shared_appearances()

    def decade_checker2(input_date2):
        if input_date2 == "Unknown":
            return "1940-01-01,2014-05-13"
        else:
            x = int(input_date2[0:4])
            if x < 1950:
                return "1940-01-01,1950-12-31"
            elif x < 2004:
                return str(x-8)+"-01-01,"+str(x+2)+"-12-12"
            else:
                return "2004-01-01,2014-05-13"

    reco_range = decade_checker2(publication_date1)

    if not character_id and not creator_id:
	    series_filter = series
    else:
	    series_filter = []

    x = len(shared_appearances_list)
    if x == 2 and len(creator_id) <= 1:
        character_id = []
        creator_id =[]
        reco_range = "1940-01-01,2014-05-13"

    recommendation_query = {'ts': '1',
	                        'hash': 'yourhash',
		                    'format': 'comic',
		                    'formatType': 'comic',
		                    'limit': '30',
		                    'creators': creator_id[:10],
		                    'noVariants': 'true',
		                    'orderBy': '-onsaleDate,title,issueNumber',
		                    'characters': character_id[:10],
		                    'sharedAppearances': shared_appearances_list[:10],
		                    'series': series_filter,
		                    'collaborators': shared_collaborator[:10],
		                    'dateRange': reco_range,
		                    'apikey': 'yourapikey',
		                    }

    headers_reco = {'Accept-Encoding': 'gzip'}

    recommendation = requests.get('http://gateway.marvel.com/v1/public/comics', params=recommendation_query, headers=headers_reco)

    reco = recommendation.json()

    reco_thumbnails = []
    reco_ids =[]
    reco_titles = []
    reco_issue_nr = []
    reco_dictionary = {}

    def reco_thumbnails_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_thumbnails.append(i.get("thumbnail").get("path"))

    def reco_ids_append(lista):
        if len(lista) != 0:
            for i in lista:
                if str(i.get("id")) != str(id_original):
                    reco_ids.append(i.get("id"))
                else:
                    reco_ids.append("myself")

    def reco_titles_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_titles.append(i.get("series").get("name"))

    def reco_issue_nr_append(lista):
	    if len(lista) != 0:
		    for i in lista:
			    reco_issue_nr.append(i.get("issueNumber"))

    reco_count = reco["data"]["count"]

    if reco_count is None:
        reco_count = 0

    reco_thumbnails_append(reco.get("data").get("results")[:reco_count])
    reco_ids_append(reco.get("data").get("results")[:reco_count])
    reco_titles_append(reco.get("data").get("results")[:reco_count])
    reco_issue_nr_append(reco.get("data").get("results")[:reco_count])

    for q, a, v, s in zip(reco_ids, reco_titles, reco_thumbnails, reco_issue_nr):
        reco_dictionary[q] = [a, v, s]

    if "myself" in reco_dictionary.keys():
        del reco_dictionary["myself"]
    else:
        pass

    try:
        reco_ids.remove("myself")
    except ValueError:
        pass

    return render_template('uat.html', thumbnail=thumbnail, link=link, comic_series=comic_series, issue_number=issue_number, publication_date=publication_date, character_list=character_list, description=description, id_original=id_original, digital_id=digital_id, creator_dictionary=creator_dictionary, reco_count=reco_count, reco_ids=reco_ids, reco_dictionary=reco_dictionary)

@app.route('/add_character', methods=['GET'])
def add_character():
    import urllib
    add_character_raw = request.args['new_char_input']
    character_list = urllib.unquote(add_character_raw).decode('utf8').replace('+', ' ')
    return character_list

@app.route('/search', methods=['GET'])
def search():
    import urllib
    series_search_raw = request.args['series']
    issue_search = request.args['issue']
    import requests
    from datetime import datetime
    import re

    series_search = urllib.unquote(series_search_raw).decode('utf8').replace('+', ' ')
    if not issue_search:
        issue_search = 1

    comic_query = {'ts': '1',
	               'hash': 'yourhash',
		           'apikey': 'yourapikey',
		           'noVariants': 'true',
		           'title': series_search,
		           'issueNumber': issue_search
		           }

    headers = {'Accept-Encoding': 'gzip'}

    r = requests.get('http://gateway.marvel.com/v1/public/comics', params=comic_query, headers=headers)

    z = r.json()

    decide = z.get("data").get("count")

    if decide == 0:
        return render_template('no_results.html')

    elif decide > 1:
        thumbnail_list = []
        comic_series_list = []
        issue_number_list = []
        id_original_list = []
        publication_date_list = []

        for i in range(decide):
            thumbnail_list.append(z.get("data").get("results")[i].get("thumbnail").get("path")+"/portrait_uncanny.jpg")
            comic_series_list.append(z.get("data").get("results")[i].get("series").get("name"))
            issue_number_list.append(z.get("data").get("results")[i].get("issueNumber"))
            id_original_list.append(z.get("data").get("results")[i].get("id"))
            publication_date1 = z.get("data").get("results")[i].get("dates")[0].get("date")[:10].strip("-")
            if len(publication_date1) == 9:
                publication_date1 = "Unknown"
            if publication_date1 != "Unknown":
                publication_date = datetime.strptime(publication_date1, "%Y-%m-%d").strftime("%B %d, %Y")
            else:
                publication_date = publication_date1
            publication_date_list.append(publication_date)
        return render_template('results.html', decide=decide, series_search=series_search, issue_search=issue_search, thumbnail_list=thumbnail_list, comic_series_list=comic_series_list, issue_number_list=issue_number_list, id_original_list=id_original_list, publication_date_list=publication_date_list)

    else:
        thumbnail = z.get("data").get("results")[0].get("thumbnail").get("path")+"/portrait_uncanny.jpg"
        link = z.get("data").get("results")[0].get("urls")[0].get("url")
        comic_series = z.get("data").get("results")[0].get("series").get("name")
        issue_number = z.get("data").get("results")[0].get("issueNumber")
        publication_date1 = z.get("data").get("results")[0].get("dates")[0].get("date")[:10].strip("-")
        if len(publication_date1) == 9:
            publication_date1 = "Unknown"
        if publication_date1 != "Unknown":
            publication_date = datetime.strptime(publication_date1, "%Y-%m-%d").strftime("%B %d, %Y")
        else:
            publication_date = publication_date1
        creators_count = z.get("data").get("results")[0].get("creators").get("returned")
        characters_count = z.get("data").get("results")[0].get("characters").get("returned")
        id_original = z.get("data").get("results")[0].get("id")
        digital_id = z.get("data").get("results")[0].get("digitalId")
        series = z.get("data").get("results")[0].get("series").get("resourceURI").split("/")[-1]
        character_list = []
        character_id = []
        creator_list = []
        creator_role = []
        creator_id = []
        creator_dictionary = {}

        def character_id_append(lista):
	        if len(lista) != 0:
		        for i in lista:
			        character_id.append(i.get("resourceURI").split("/")[-1])

        character_id_append(z.get("data").get("results")[0].get("characters").get("items")[:characters_count])

        def creator_id_append(lista):
	        if len(lista) != 0:
		        for i in lista:
			        creator_id.append(i.get("resourceURI").split("/")[-1])

        creator_id_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

        def creator_role_append(lista):
	        if len(lista) != 0:
		        for i in lista:
			        creator_role.append(i.get("role"))
	        else:
		        creator_role.append("Unknown")

        creator_role_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

        def creator_append(lista):
	        if len(lista) != 0:
		        for i in lista:
			        creator_list.append(i.get("name"))
	        else:
		        creator_list.append("Unknown")

        creator_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

        creator_role = [word.replace("penciller (cover)", "cover") for word in creator_role]
        creator_role = [word.replace("penciler (cover)", "cover") for word in creator_role]
        creator_role = [word.replace("penciler", "penciller") for word in creator_role]
        creator_role = [word.replace(word[0], word[0].upper()) for word in creator_role]

        for q, a in zip(creator_role, creator_list):
            creator_dictionary.setdefault(q,[]).append(a)

        def character_append(lista):
	        if len(lista) != 0:
		        for i in lista:
			        character_list.append(i.get("name"))
	        else:
		        character_list.append("Unknown")

        character_append(z.get("data").get("results")[0].get("characters").get("items")[:characters_count])

        a = z.get("data").get("results")[0].get("textObjects")
        description_list = []


        def description_check():
            if not a:
                description_list.insert(0, "There is no description for this issue yet in the Marvel database.")
            else:
                description_list.insert(0, z.get("data").get("results")[0].get("textObjects")[0].get("text"))

        def replacer (rep, text):
	        rep = dict((re.escape(k), v) for k, v in rep.iteritems())
	        pattern = re.compile("|".join(rep.keys()))
	        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
	        return text

        char_repl = {"<br>": "",
	       		 "&bull; ": "",
	    		 "<ul>": "",
	     		 "<li>": "",
	    	 	 "</ul>": "",
	    		 "</li>": "",
	    		 "</br": "",
	    		 "&rsquo;": "'",
	    		 "&hellip;": "...",
	    		 "&mdash;": "-",
	    		 "&ndash;": "-",
	    		 "--": " - ",
	    		 "<br />": "",
	    		 "&ldquo;": '"',
	    		 "&rdquo;": '"',
	    		 "&#39;": "'",
                u"•": "\n",
                u"—": " - ",
                u"�": "",
                "&#133;": "...",
                u"ï¿½": "'",
                u"â€¢ ": "",
                '&quot;': '"',
                u"â€™": "'",
                "%^$%^%$%^": ""}

        description_check()
        description = replacer(char_repl, description_list[0])

        shared_collaborator = []
        shared_appearances_list = []

        true_artists = ["writer", "artist", "penciller", "penciler", "penciler (cover)", "penciller (cover)", "artist (cover"]

        def creator_shared_append(lista):
	        for i in lista:
		        if len(lista) != 0 and any(substring in i.get("role") for substring in true_artists):
			        shared_collaborator.append(i.get("resourceURI").split("/")[-1])
		        else:
			        pass

        creator_shared_append(z.get("data").get("results")[0].get("creators").get("items")[:creators_count])

        def shared_appearances():
	        if 2 <= len(character_list) <=10:
		        shared_appearances_list.extend(character_id)

        shared_appearances()

        def decade_checker2(input_date2):
            if input_date2 == "Unknown":
                return "1940-01-01,2014-05-13"
            else:
                x = int(input_date2[0:4])
                if x < 1950:
                    return "1940-01-01,1950-12-31"
                elif x < 2004:
                    return str(x-8)+"-01-01,"+str(x+2)+"-12-12"
                else:
                    return "2004-01-01,2014-05-13"

        reco_range = decade_checker2(publication_date1)

        if not character_id and not creator_id:
	        series_filter = series
        else:
	        series_filter = []

        x = len(shared_appearances_list)
        if x == 2 and len(creator_id) <= 1:
            character_id = []
            creator_id =[]
            reco_range = "1940-01-01,2014-05-13"

        recommendation_query = {'ts': '1',
	                            'hash': 'yourhash',
		                        'format': 'comic',
		                        'formatType': 'comic',
		                        'limit': '30',
		                        'creators': creator_id[:10],
		                        'noVariants': 'true',
		                        'orderBy': '-onsaleDate,title,issueNumber',
		                        'characters': character_id[:10],
		                        'sharedAppearances': shared_appearances_list[:10],
		                        'series': series_filter,
		                        'collaborators': shared_collaborator[:10],
		                        'dateRange': reco_range,
		                        'apikey': 'yourapikey',
		                        }

        headers_reco = {'Accept-Encoding': 'gzip'}

        recommendation = requests.get('http://gateway.marvel.com/v1/public/comics', params=recommendation_query, headers=headers_reco)

        reco = recommendation.json()

        reco_thumbnails = []
        reco_ids =[]
        reco_titles = []
        reco_issue_nr = []
        reco_dictionary = {}

        def reco_thumbnails_append(lista):
	        if len(lista) != 0:
		        for i in lista:
			        reco_thumbnails.append(i.get("thumbnail").get("path"))

        def reco_ids_append(lista):
            if len(lista) != 0:
                for i in lista:
                    if str(i.get("id")) != str(id_original):
                        reco_ids.append(i.get("id"))
                    else:
                        reco_ids.append("myself")

        def reco_titles_append(lista):
	        if len(lista) != 0:
		        for i in lista:
			        reco_titles.append(i.get("series").get("name"))

        def reco_issue_nr_append(lista):
	        if len(lista) != 0:
		        for i in lista:
			        reco_issue_nr.append(i.get("issueNumber"))

        reco_count = reco["data"]["count"]

        if reco_count is None:
            reco_count = 0

        reco_thumbnails_append(reco.get("data").get("results")[:reco_count])
        reco_ids_append(reco.get("data").get("results")[:reco_count])
        reco_titles_append(reco.get("data").get("results")[:reco_count])
        reco_issue_nr_append(reco.get("data").get("results")[:reco_count])

        for q, a, v, s in zip(reco_ids, reco_titles, reco_thumbnails, reco_issue_nr):
            reco_dictionary[q] = [a, v, s]

        if "myself" in reco_dictionary.keys():
            del reco_dictionary["myself"]
        else:
            pass

        try:
            reco_ids.remove("myself")
        except ValueError:
            pass

        return render_template('uat.html', thumbnail=thumbnail, link=link, comic_series=comic_series, issue_number=issue_number, publication_date=publication_date, character_list=character_list, description=description, id_original=id_original, digital_id=digital_id, creator_dictionary=creator_dictionary, reco_count=reco_count, reco_ids=reco_ids, reco_dictionary=reco_dictionary)


@app.route('/svg', methods=['GET', 'POST'])
def svg():
    return render_template('svg.html')

@app.route('/d3', methods=['GET', 'POST'])
def d3():
    return render_template('d3.html')

@app.route('/d3_stacked', methods=['GET', 'POST'])
def d3_stacked():
    return render_template('d3_stacked.html')

@app.route('/sendmail', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        @async
        def send_async_email(msg):
            with app.app_context():
                mail.send(msg)

        def send_email(subject, sender, recipients, text_body):
            msg = Message(subject, sender = sender, recipients = recipients)
            msg.body = text_body
            send_async_email(msg)

        text = """
From: %s <%s>

%s
    """ % (request.json["name"], request.json["email"], request.json["message"])
        send_email(request.json["subject"], "youremail", ["youremail"], text)
        return jsonify(result={"status": 200})
    else:
        return render_template('404.html')

@app.route('/sendcharacter', methods=['GET', 'POST'])
def sendcharacter():
    if request.method == 'POST':
        @async
        def send_async_email(msg):
            with app.app_context():
                mail.send(msg)

        def send_email(subject, sender, recipients, text_body):
            msg = Message(subject, sender = sender, recipients = recipients)
            msg.body = text_body
            send_async_email(msg)

        text = """
Hi There,

The following characters have been added to %s [Marvel Database ID = %s]:

%s

Characters already present in this issue:

%s
    """ % (request.json["issue"], request.json["comic_id"], request.json["message"], request.json["character_list"])
        send_email(request.json["subject"], "youremail", ["youremail"], text)
        return jsonify(result={"status": 200})
    else:
        return render_template('404.html')

if __name__ == '__main__':
    app.run()
