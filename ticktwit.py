
# Requires pymongo and tweepy
# Coded by Amir Canto


from pymongo import *
from datetime import *
from time import *
import tweepy


print "Inicializando..."

#here comes the account keys, get it here:  developer.twitter.com
consumer_token = ''
consumer_secret = ''
key = ''
secret = ''

ticker = ['$AC','$ALFA','$ALPEK','$ALSEA',
		  '$AMX','$ASUR','$BIMBO','$BOLSA','$CEMEX',
		  '$CHDRAUI','$COMERCI','$COMPARC','$ELEKTRA',
		  '$FEMSA','$GAP','$GFINBUR','$GFNORTE',
		  '$GFREGIO','$GMEXICO','$GRUMA',
		  '$GSANBOR','$ICA','$ICH','$IENOVA',
		  '$KIMBER','$KOFL','$LAB','$LIVEPOL',
		  '$MEXCHEM','$OHLMEX','$PE&OLES','$PINFRA',
		  '$SANMEX','$TLEVISA','$WALMEX']



print "Conectando a twitter..."
auth = tweepy.OAuthHandler(consumer_token,consumer_secret)
auth.set_access_token(key,secret)
api = tweepy.API(auth)


print "Conectando al servidor local de base de datos"

conexion = Connection()
db = conexion['twit_ticker']
twitText = db['twit']

print "Extrayendo twits de cada emisora..."
fecha  = date.today()
fechaAgregado = fecha.strftime("%d-%m-%y")

for emisora in ticker:
	print "Emisora actual: %s" % (emisora)
	for twit in tweepy.Cursor(api.search,emisora).items(1000):
	
		if twit.text:
			print "Insertando los datos en Mongo"
			twitText.insert({'ticker':emisora,'twit': twit.text,'fecha':fechaAgregado})
