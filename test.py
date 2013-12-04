from flask import Flask, render_template, request
from wtforms import Form, TextField, SubmitField
from twitter import *
import collections
import json
import re
from nltk.corpus import stopwords
import urllib2
from BeautifulSoup import BeautifulSoup
import pprint

app = Flask(__name__)

class BuildListForm(Form):
	user1 = TextField('Twitter User:')
	user2 = TextField('Twitter User:')
	user3 = TextField('Twitter User:')
	user4 = TextField('Twitter User:')
	user5 = TextField('Twitter User:')
	submit = SubmitField("Build Network")

@app.route('/')
def home():
	return render_template('input.html')

@app.route('/postTest', methods=['POST'])
def postTest():
	if request.method == 'POST':
		hello = request.form['user1']
		return render_template('postTest.html', input=hello)

@app.route('/search-test', methods=['POST'])
def searchTest():
	if request.method == 'POST':
		t = Twitter(auth=OAuth('931458319-2k9OMXCCIZeM7K5FuT6UfVarIUAIfJ1mYYMul99B', 'bJrLuGOzPozdYdFTw4NLq1YzUJ4zglyrNNgyxO10ljWO0', 'eEj5KPQdDK1LtxGX6fZKw', 'oKjbj9Y4LQjv2mkJ7UO24JMhLj20lhawcNZFxeh4s'))
		
		user1 = request.form['user1']
		user2 = request.form['user2']
		user3 = request.form['user3']
		user4 = request.form['user4']
		user5 = request.form['user5']

		user1_friends = t.friends.ids(screen_name=user1)['ids']
		user2_friends = t.friends.ids(screen_name=user2)['ids']
		user3_friends = t.friends.ids(screen_name=user3)['ids']
		user4_friends = t.friends.ids(screen_name=user4)['ids']
		user5_friends = t.friends.ids(screen_name=user5)['ids']

		masterList = user1_friends + user2_friends + user3_friends + user4_friends + user5_friends
		x = collections.Counter(masterList)
		x.most_common()
		new = [elt for elt,count in x.most_common(50)]

		allTweets = []
		for count in range(len(new)):
			allTweets = allTweets + t.statuses.user_timeline(user_id=new[count], count=20)

		parsedTweets = json.dumps(allTweets)
		arrayTweets = json.loads(parsedTweets)
		hashtags = []

		for count in range(len(arrayTweets)):
			hashtags = hashtags + re.findall(r"#(\w+)", arrayTweets[count]['text'])

		hashtagCount = collections.Counter(hashtags)
		hashtagTuples = hashtagCount.items()
		sortedHashtagTuples = sorted(hashtagTuples, key=lambda x: x[1])
		sortedHashtagTuples = sortedHashtagTuples[::-1]

		allHashtags = []
		mostUsed = sortedHashtagTuples[0][1]
		for count in range(len(sortedHashtagTuples)):
			temp = [sortedHashtagTuples[count][0], sortedHashtagTuples[count][1], sortedHashtagTuples[count][1]/float(mostUsed)*100]
			allHashtags.append(temp)

		x = collections.Counter(masterList)
		y = x.most_common(5)

		top = t.users.lookup(user_id=','.join(str(x) for x,z in y), _timeout=1)
		names = []
		for count in range(5):
			names.append(top[count]['name'])

		finalTop = []
		for count in range(5):
			temp = [names[count], y[count][1]/float(5)*100, top[count]['profile_image_url_https'], 'http://twitter.com/' + top[count]['screen_name']]
			finalTop.append(temp) 
		
		#keywords
		allWords = ''
		for count in range(len(arrayTweets)):
			allWords = allWords + " " + arrayTweets[count]['text']

		splitWords = allWords.split()
		manualStopList = ['RT', '21', '-', '&amp;', 'I', 'MT', 'The', 'It\'s']
		filteredWords = [w for w in splitWords if not w in stopwords.words('english')]
		filteredWords2 = [w for w in filteredWords if not w in manualStopList]
		noHashtags = [s.strip('#') for s in filteredWords2]
		ranked = collections.Counter(noHashtags).most_common(100)

		maxUse = ranked[0][1]
		allKeywords = []
		for count in range(len(ranked)):
			temp = [ranked[count][0], ranked[count][1], ranked[count][1]/float(maxUse)*100]
			allKeywords.append(temp)

		#links 
		allLinks = []
		for count in range(len(arrayTweets)):
			try:
	  			arrayTweets[count]['entities']['urls'][0]['expanded_url']
			except IndexError:
				pass
			else:
				allLinks.append(arrayTweets[count]['entities']['urls'][0]['expanded_url'])


		#links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', allLinks)
		#rankedLinks = collections.Counter(links).most_common()
		rankedLinks = collections.Counter(allLinks).most_common(20)

		linkTitles = []
		for count in range(len(rankedLinks)):
			source = urllib2.urlopen(rankedLinks[count][0])
			BS = BeautifulSoup(source)
			linkTitles.append([rankedLinks[count][0], BS.find('title').text, rankedLinks[count][1]])


		return render_template('networkResults.html', hashtags=allHashtags, topusers=finalTop, keywords=allKeywords, links=linkTitles)

@app.route('/search', methods=['GET', 'POST'])
def search():
	t = Twitter(auth=OAuth('931458319-2k9OMXCCIZeM7K5FuT6UfVarIUAIfJ1mYYMul99B', 'bJrLuGOzPozdYdFTw4NLq1YzUJ4zglyrNNgyxO10ljWO0', 'eEj5KPQdDK1LtxGX6fZKw', 'oKjbj9Y4LQjv2mkJ7UO24JMhLj20lhawcNZFxeh4s'))
	testListId = t.lists.show(slug='tweetbeattestingdemo', owner_screen_name='PhilipHouse2')['id']

	tweets = t.lists.statuses(list_id=testListId, count=200)
	parsedTweets = json.dumps(tweets)
	arrayTweets = json.loads(parsedTweets)
	hashtags = []

	for count in range(len(arrayTweets)):
		hashtags = hashtags + re.findall(r"#(\w+)", arrayTweets[count]['text'])

	hashtagCount = collections.Counter(hashtags)
	hashtagTuples = hashtagCount.items()
	sortedHashtagTuples = sorted(hashtagTuples, key=lambda x: x[1])
	sortedHashtagTuples = sortedHashtagTuples[::-1]

	allHashtags = []
	mostUsed = sortedHashtagTuples[0][1]
	for count in range(len(sortedHashtagTuples)):
		temp = [sortedHashtagTuples[count][0], sortedHashtagTuples[count][1], sortedHashtagTuples[count][1]/float(mostUsed)*100]
		allHashtags.append(temp)

	user1_friends = t.friends.ids(screen_name='NASA')['ids']
	user2_friends = t.friends.ids(screen_name='SPACEdotcom')['ids']
	user3_friends = t.friends.ids(screen_name='Csa_asc')['ids']

	masterList = user1_friends + user2_friends + user3_friends
	x = collections.Counter(masterList)
	y = x.most_common(5)

	top = t.users.lookup(user_id=','.join(str(x) for x,z in y), _timeout=1)
	names = []
	for count in range(5):
		names.append(top[count]['name'])

	finalTop = []
	for count in range(5):
		temp = [names[count], y[count][1]/float(3)*100, top[count]['profile_image_url_https']]
		finalTop.append(temp) 
	
	#keywords
	allWords = ''
	for count in range(len(arrayTweets)):
		allWords = allWords + " " + arrayTweets[count]['text']

	splitWords = allWords.split()
	manualStopList = ['RT', '21', '-', '&amp;', 'I', 'MT', 'The', 'It\'s']
	filteredWords = [w for w in splitWords if not w in stopwords.words('english')]
	filteredWords2 = [w for w in filteredWords if not w in manualStopList]
	noHashtags = [s.strip('#') for s in filteredWords2]
	ranked = collections.Counter(noHashtags).most_common(100)

	maxUse = ranked[0][1]
	allKeywords = []
	for count in range(len(ranked)):
		temp = [ranked[count][0], ranked[count][1], ranked[count][1]/float(maxUse)*100]
		allKeywords.append(temp)

	#links 
	allLinks = []
	for count in range(len(arrayTweets)):
		try:
  			arrayTweets[count]['entities']['urls'][0]['expanded_url']
		except IndexError:
			pass
		else:
			allLinks.append(arrayTweets[count]['entities']['urls'][0]['expanded_url'])


	#links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', allLinks)
	#rankedLinks = collections.Counter(links).most_common()
	rankedLinks = collections.Counter(allLinks).most_common()


	return render_template('networkResults.html', hashtags=allHashtags, topusers=finalTop, keywords=allKeywords, links=rankedLinks)


@app.route('/index', methods=['GET', 'POST'])
def index():
	form = BuildListForm(request.form)

	if request.method == 'POST':
		t = Twitter(auth=OAuth('931458319-2k9OMXCCIZeM7K5FuT6UfVarIUAIfJ1mYYMul99B', 'bJrLuGOzPozdYdFTw4NLq1YzUJ4zglyrNNgyxO10ljWO0', 'eEj5KPQdDK1LtxGX6fZKw', 'oKjbj9Y4LQjv2mkJ7UO24JMhLj20lhawcNZFxeh4s'));

		user1_friends = t.friends.ids(screen_name=form.user1.data)['ids']
		user2_friends = t.friends.ids(screen_name=form.user2.data)['ids']
		user3_friends = t.friends.ids(screen_name=form.user3.data)['ids']

		if (len(user1_friends) < 50):
			topLimit1 = len(user1_friends)
		else:
			topLimit1 = 50

		if (len(user2_friends) < 50):
			topLimit2 = len(user2_friends)
		else:
			topLimit2 = 50
			
		if (len(user3_friends) < 50):
			topLimit3 = len(user3_friends)
		else:
			topLimit3 = 50

		masterList = user1_friends + user2_friends + user3_friends
		x = collections.Counter(masterList)
		x.most_common()
		new = [elt for elt,count in x.most_common(40)]

		#testListId = t.lists.show(slug='tweetbeat', owner_screen_name='PhilipHouse2')['id']
		#deleted = t.lists.destroy(list_id=testListId)

		newId = t.lists.create(name='TweetbeatBrooklyn')['id']

		newAdded = t.lists.members.create_all(list_id=newId, user_id=','.join(str(x) for x in new), _timeout=100)
			
		user1_limitFriends = []
		user2_limitFriends = []
		user3_limitFriends = []
		
		for i in range(topLimit1):
			user1_limitFriends.append(user1_friends[i])
		for i in range(topLimit2):
			user2_limitFriends.append(user2_friends[i])
		for i in range(topLimit3):
			user3_limitFriends.append(user3_friends[i])

		user1_nameList = t.users.lookup(user_id=','.join(str(x) for x in user1_limitFriends), _timeout=1)
		user2_nameList = t.users.lookup(user_id=','.join(str(x) for x in user2_limitFriends), _timeout=1)
		user3_nameList = t.users.lookup(user_id=','.join(str(x) for x in user3_limitFriends), _timeout=1)

		return render_template('results.html', form=form,users1=user1_nameList, users2=user2_nameList, users3=user3_nameList)
		
	elif request.method == 'GET':
		return render_template('search.html', form=form)

@app.route('/search2', methods=['GET', 'POST'])
def search2():
	t = Twitter(auth=OAuth('931458319-2k9OMXCCIZeM7K5FuT6UfVarIUAIfJ1mYYMul99B', 'bJrLuGOzPozdYdFTw4NLq1YzUJ4zglyrNNgyxO10ljWO0', 'eEj5KPQdDK1LtxGX6fZKw', 'oKjbj9Y4LQjv2mkJ7UO24JMhLj20lhawcNZFxeh4s'))
	testListId = t.lists.show(slug='tweetbeatbrooklyn', owner_screen_name='PhilipHouse2')['id']

	tweets = t.lists.statuses(list_id=testListId, count=200)
	parsedTweets = json.dumps(tweets)
	arrayTweets = json.loads(parsedTweets)
	hashtags = []

	for count in range(len(arrayTweets)):
		hashtags = hashtags + re.findall(r"#(\w+)", arrayTweets[count]['text'])

	hashtagCount = collections.Counter(hashtags)
	hashtagTuples = hashtagCount.items()
	sortedHashtagTuples = sorted(hashtagTuples, key=lambda x: x[1])
	sortedHashtagTuples = sortedHashtagTuples[::-1]

	allHashtags = []
	mostUsed = sortedHashtagTuples[0][1]
	for count in range(len(sortedHashtagTuples)):
		temp = [sortedHashtagTuples[count][0], sortedHashtagTuples[count][1], sortedHashtagTuples[count][1]/float(mostUsed)*100]
		allHashtags.append(temp)

	user1_friends = t.friends.ids(screen_name='Brokelyn')['ids']
	user2_friends = t.friends.ids(screen_name='thebklynkitchen')['ids']
	user3_friends = t.friends.ids(screen_name='BrooklynBrewery')['ids']

	masterList = user1_friends + user2_friends + user3_friends
	x = collections.Counter(masterList)
	y = x.most_common(5)

	top = t.users.lookup(user_id=','.join(str(x) for x,z in y), _timeout=1)
	names = []
	for count in range(5):
		names.append(top[count]['name'])

	finalTop = []
	for count in range(5):
		temp = [names[count], y[count][1]/float(3)*100, top[count]['profile_image_url_https']]
		finalTop.append(temp) 
	
	#keywords
	allWords = ''
	for count in range(len(arrayTweets)):
		allWords = allWords + " " + arrayTweets[count]['text']

	splitWords = allWords.split()
	filteredWords = [w for w in splitWords if not w in stopwords.words('english')]
	noHashtags = [s.strip('#') for s in filteredWords]
	ranked = collections.Counter(noHashtags).most_common(100)

	maxUse = ranked[0][1]
	allKeywords = []
	for count in range(len(ranked)):
		temp = [ranked[count][0], ranked[count][1], ranked[count][1]/float(maxUse)*100]
		allKeywords.append(temp)

	#links 
	allLinks = ''
	for count in range(len(arrayTweets)):
		allLinks = allLinks + " " + arrayTweets[count]['text']

	links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', allLinks)
	rankedLinks = collections.Counter(links).most_common()

	return render_template('networkResults.html', hashtags=allHashtags, topusers=finalTop, keywords=allKeywords, links=rankedLinks)



if __name__ == '__main__':
	app.run(debug = True)