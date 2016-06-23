from alchemyapi import AlchemyAPI
from flask import Flask, request, render_template
import jinja2, json, random, nltk
from nltk import tokenize
from unidecode import unidecode

nltk.data.path.append("./nltk_data/")

TOPIC_ENTITIES_THRESHOLD = 0.6
TOPIC_KEYWORDS_THRESHOLD = 0.75

ENTITY_SENTIMENT_THRESHOLD = 0.4
KEYWORD_SENTIMENT_THRESHOLD = 0.4

defaultDocs = [
"U.S. stocks finished little changed on Friday, but the Dow and the S&P 500 managed to log their best weekly gains since November, closing the curtain on a bumpy stretch of trading on Wall Street. A rally in the technology and consumer discretionary sectors eased a sharp selloff in the materials sector fueled by the drop in oil prices, while a reading on U.S. consumer inflation came in above economists' expectations. The S&P 500 SPX, +0.00% trimmed early losses to finish less than a point lower at 1,917.78. The materials sector fell the most, down 1.1%, while the consumer-discretionary sector led gainers, up 0.3%, followed by tech, up 0.2%. The index booked a 2.8% weekly gain, the largest weekly advance since Nov. 20.", 
"U.S. stocks finished little changed on Friday, but the Dow and the S&P 500 managed to log their best weekly gains since November, closing the curtain on a bumpy stretch of trading on Wall Street. A rally in the technology and consumer discretionary sectors eased a sharp selloff in the materials sector fueled by the drop in oil prices, while a reading on U.S. consumer inflation came in above economists' expectations. The S&P 500 SPX, +0.00% trimmed early losses to finish less than a point lower at 1,917.78. The materials sector fell the most, down 1.1%, while the consumer-discretionary sector led gainers, up 0.3%, followed by tech, up 0.2%. The index booked a 2.8% weekly gain, the largest weekly advance since Nov. 20.", 
"Apple's iPhone 5 received the biggest customer backlash following its launch in 2012, according to new research. One in five posts on social networks were critical of Apple's most recent handset, with the majority of people complaining about the introduction of a new power socket, the inaccuracy of Apple Maps and how similar the phone was to previous models. Samsung's Galaxy S4 received the least complaints - just 11 per cent - according to figures from analysts We Are Social.",
"Florida plans to file a U.S. Supreme Court lawsuit against Georgia, saying the state is consuming too much water that would otherwise flow to Florida, the latest battle nationally over an increasingly scarce resource. The dispute is fueled by the rapid growth of the metropolitan area surrounding Atlanta, which is demanding more water and hurting the oyster industry in Northwest Florida, Florida Governor Rick Scott, 60, said yesterday. Scott, a Republican, said he would file suit next month after the two states couldn't reach an agreement. \"That's our water,\" Scott told reporters while standing next to the Apalachicola Bay in the Florida Panhandle. \"They've impacted our families. They've impacted the livelihood of people down here.",
"Credit cards offer many advantages. There is the convenience of being able to buy needed items now and the security of not having to carry cash. You also receive fraud protection and in some cases rewards for making purchases. With these advantages also come responsibilities. You need to manage credit cards wisely by understanding all of the card's terms and conditions; stay on top of payments; and realize the true cost of purchases made with credit. Using a credit card is like taking out a loan. If you don't pay your card balance in full each month, you'll pay interest on that loan."
]

alchemyapi = AlchemyAPI()

def annotate(s, entities, keywords):
        a = []
        for dic in [entities, keywords]:
                for key, value in dic.iteritems():
                        if(s.lower().find(key.lower()) != -1):
                                a.append("Possible " + value + " bias towards \"" + key + "\"")
                                
        if(len(a) == 0):
                a = None
                
        return (s, a)

app = Flask(__name__)

@app.route("/")
def get_index():
	defaultDoc = random.choice(defaultDocs)
	return render_template('index.html', defaultDoc = defaultDoc)

@app.route("/result", methods=["POST"])
def get_result():
	reqDoc = request.form["doc"]

	try:
		doc = str(reqDoc)
	except UnicodeEncodeError:
		doc = unidecode(reqDoc)

	combined = alchemyapi.combined("text", doc, options = {"extract":"entity,keyword", "sentiment":1})

	if(combined["status"] == "OK"):
		entities = combined["entities"]
		keywords = combined["keywords"]

		topicEntities = filter(lambda e: float(e["relevance"]) > TOPIC_ENTITIES_THRESHOLD, entities)
		topicKeywords = filter(lambda k: float(k["relevance"]) > TOPIC_KEYWORDS_THRESHOLD, keywords)

		biasedEntities = {}

		for e in topicEntities:
			if("score" in e["sentiment"].keys()):
				if((abs(float(e["sentiment"]["score"])) > ENTITY_SENTIMENT_THRESHOLD)):
					biasedEntities[e["text"]] = e["sentiment"]["type"]

		biasedKeywords = {}

		for k in topicKeywords:
			if("score" in k["sentiment"].keys()):
				if((abs(float(k["sentiment"]["score"])) > KEYWORD_SENTIMENT_THRESHOLD)):
					biasedKeywords[k["text"]] = k["sentiment"]["type"]

		docSentences = tokenize.sent_tokenize(doc)

		sentencesAnnotated = [annotate(s, biasedEntities, biasedKeywords) for s in docSentences]

		return json.dumps({'status':'OK','doc':doc, 'sentences':sentencesAnnotated})
	else:
		return "There was an error!" + pprint("COMBINED", combined)

if(__name__ == '__main__'):
        app.run(threaded = True, debug = True)
