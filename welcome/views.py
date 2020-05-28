import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import random
import pymysql
import socket

# Create your views here.

def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    return HttpResponse(PageView.objects.count())

app = Flask(__name__)
api = Api(app)

ai_quotes = [
    {
        "id": 0,
        "author": "Kevin Kelly",
        "quote": "The business plans of the next 10,000 startups are easy to forecast: " +
                 "Take X and add AI."
    },
    {
        "id": 1,
        "author": "Stephen Hawking",
        "quote": "The development of full artificial intelligence could " +
                 "spell the end of the human race " +
                 "It would take off on its own, and re-design " +
                 "itself at an ever increasing rate. " +
                 "Humans, who are limited by slow biological evolution, " +
                 "couldn't compete, and would be superseded."
    },
    {
        "id": 2,
        "author": "Claude Shannon",
        "quote": "I visualize a time when we will be to robots what " +
                 "dogs are to humans, " +
                 "and Im rooting for the machines."
    },
    {
        "id": 3,
        "author": "Elon Musk",
        "quote": "The pace of progress in artificial intelligence " +
                 "(Im not referring to narrow AI) " +
                 "is incredibly fast. Unless you have direct " +
                 "exposure to groups like Deepmind, " +
                 "you have no idea how fast it is growing " +
                 "at a pace close to exponential. " +
                 "The risk of something seriously dangerous " +
                 "happening is in the five-year timeframe." +
                 "10 years at most."
    },
    {
        "id": 4,
        "author": "Geoffrey Hinton",
        "quote": "I have always been convinced that the only way " +
                 "to get artificial intelligence to work " +
                 "is to do the computation in a way similar to the human brain. " +
                 "That is the goal I have been pursuing. We are making progress, " +
                 "though we still have lots to learn about " +
                 "how the brain actually works."
    },
    {
        "id": 5,
        "author": "Pedro Domingos",
        "quote": "People worry that computers will " +
                 "get too smart and take over the world, " +
                 "but the real problem is that they're too stupid " +
                 "and they've already taken over the world."
    },
    {
        "id": 6,
        "author": "Alan Turing",
        "quote": "It seems probable that once the machine thinking " +
                 "method had started, it would not take long " +
                 "to outstrip our feeble powers " +
                 "They would be able to converse " +
                 "with each other to sharpen their wits. " +
                 "At some stage therefore, we should " +
                 "have to expect the machines to take control."
    },
    {
        "id": 7,
        "author": "Ray Kurzweil",
        "quote": "Artificial intelligence will reach " +
                 "human levels by around 2029. " +
                 "Follow that out further to, say, 2045, " +
                 "we will have multiplied the intelligence, " +
                 "the human biological machine intelligence " +
                 "of our civilization a billion-fold."
    },
    {
        "id": 8,
        "author": "Sebastian Thrun",
        "quote": "Nobody phrases it this way, but I think " +
                 "that artificial intelligence " +
                 "is almost a humanities discipline. It's really an attempt " +
                 "to understand human intelligence and human cognition."
    },
    {
        "id": 9,
        "author": "Andrew Ng",
        "quote": "We're making this analogy that AI is the new electricity." +
                 "Electricity transformed industries: agriculture, " +
                 "transportation, communication, manufacturing."
    }
]

class Apigeo(Resource):
    def get(self):
        #return socket.gethostname(), 200
        #465e4889-402d-49aa-92b0-d2270c1bc33e
        if socket.gethostname() == "Victors-Mac-mini.local":
            con = pymysql.connect('localhost', 'root', 'qwerty123', 'geo')
        else:
            con = pymysql.connect('us-cdbr-east-06.cleardb.net', 'bb9a790fad175e', '52b62723', 'heroku_f93829613caaa23')
        cur = con.cursor()
        with con:
            country_id = 0
            if request.headers.get('country_id'):
                country_id = request.headers.get('country_id')
            cur.execute(f"call getdata({country_id})")
            #if request.headers.get('name'):
            #    name = request.headers.get('name')
            #    cur.execute(f"SELECT * FROM `countries` WHERE name LIKE '%{name}%' LIMIT 10")
            #else:
            #    cur.execute("SELECT * FROM `countries` LIMIT 10")
            rows = cur.fetchall()
            return rows, 200
        return "Apigeo not found", 404

class Quote(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(ai_quotes), 200
        for quote in ai_quotes:
            if(quote["id"] == id):
                return quote, 200
        return "Quote not found", 404

def post(self, id):
      parser = reqparse.RequestParser()
      parser.add_argument("author")
      parser.add_argument("quote")
      params = parser.parse_args()
      for quote in ai_quotes:
          if(id == quote["id"]):
              return "Quote with id {id} already exists", 400
      quote = {
          "id": int(id),
          "author": params["author"],
          "quote": params["quote"]
      }
      ai_quotes.append(quote)
      return quote, 201

def put(self, id):
      parser = reqparse.RequestParser()
      parser.add_argument("author")
      parser.add_argument("quote")
      params = parser.parse_args()
      for quote in ai_quotes:
          if(id == quote["id"]):
              quote["author"] = params["author"]
              quote["quote"] = params["quote"]
              return quote, 200
      
      quote = {
          "id": id,
          "author": params["author"],
          "quote": params["quote"]
      }
      
      ai_quotes.append(quote)
      return quote, 201

def delete(self, id):
      global ai_quotes
      ai_quotes = [qoute for qoute in ai_quotes if qoute["id"] != id]
      return "Quote with id {id} is deleted.", 200

api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")
api.add_resource(Apigeo, "/api", "/api/")
if __name__ == '__main__':
    app.run(debug=True)
