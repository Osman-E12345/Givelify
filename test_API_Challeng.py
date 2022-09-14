
from email.headerregistry import ContentTypeHeader
from http.client import responses
from socket import timeout
from wsgiref import headers
from xmlrpc.client import Boolean
from jsonschema import validate
import pytest
import requests
import json

from urllib3 import Timeout

@pytest.fixture()
def test_setup():
    global resp
    global json_response
    global schema
    resp = requests.get("http://www.omdbapi.com/?i=tt1517451&apikey=375a3264")
    json_response = resp.json()
    schema = {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "$ref": "#/definitions/Welcome6",
        "definitions": {
            "Welcome6": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "Title": {
                        "type": "string"
                    },
                    "Year": {
                        "type": "string",
                        "format": "integer"
                    },
                    "Rated": {
                        "type": "string"
                    },
                    "Released": {
                        "type": "string"
                    },
                    "Runtime": {
                        "type": "string"
                    },
                    "Genre": {
                        "type": "string"
                    },
                    "Director": {
                        "type": "string"
                    },
                    "Writer": {
                        "type": "string"
                    },
                    "Actors": {
                        "type": "string"
                    },
                    "Plot": {
                        "type": "string"
                    },
                    "Language": {
                        "type": "string"
                    },
                    "Country": {
                        "type": "string"
                    },
                    "Awards": {
                        "type": "string"
                    },
                    "Poster": {
                        "type": "string",
                        "format": "uri",
                        "qt-uri-protocols": [
                            "https"
                        ],
                        "qt-uri-extensions": [
                            ".jpg"
                        ]
                    },
                    "Ratings": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/Rating"
                        }
                    },
                    "Metascore": {
                        "type": "string",
                        "format": "integer"
                    },
                    "imdbRating": {
                        "type": "string"
                    },
                    "imdbVotes": {
                        "type": "string"
                    },
                    "imdbID": {
                        "type": "string"
                    },
                    "Type": {
                        "type": "string"
                    },
                    "DVD": {
                        "type": "string"
                    },
                    "BoxOffice": {
                        "type": "string"
                    },
                    "Production": {
                        "type": "string"
                    },
                    "Website": {
                        "type": "string"
                    },
                    "Response": {
                        "type": "string"
                    }
                },
                "required": [
                    "Actors",
                    "Awards",
                    "BoxOffice",
                    "Country",
                    "DVD",
                    "Director",
                    "Genre",
                    "Language",
                    "Metascore",
                    "Plot",
                    "Poster",
                    "Production",
                    "Rated",
                    "Ratings",
                    "Released",
                    "Response",
                    "Runtime",
                    "Title",
                    "Type",
                    "Website",
                    "Writer",
                    "Year",
                    "imdbID",
                    "imdbRating",
                    "imdbVotes"
                ],
                "title": "Welcome6"
            },
            "Rating": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "Source": {
                        "type": "string"
                    },
                    "Value": {
                        "type": "string"
                    }
                },
                "required": [
                    "Source",
                    "Value"
                ],
                "title": "Rating"
            }
        }
    }


def validate_JSON_DATA (jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def test_codeResponse200_Validattion (test_setup):
    code = resp.status_code
    print(code)
    assert code==200 , "Code doesn't match with the response 200"

def test_response_not_error (test_setup):
    response = json_response["Response"]
    code = resp.status_code
    assert response!= "False" ,"Response is False which means is a error"
    assert code==200 , "Code doesn't match with the response 200"

def test_verify_year_is_2018 (test_setup):
    year = json_response["Year"]
    assert year == "2018", "Year is not 2018"

def test_very_response_contains_Bradley(test_setup):
    substring = "Bradley"
    director = json_response["Director"]
    writer = json_response["Writer"]
    actors = json_response["Actors"]
    if substring in director or substring in writer or substring in actors:
        return True
    else:    
        return False

def test_validation_timeout(test_setup):
    try:
        requests.get("http://www.omdbapi.com/?i=tt1517451&apikey=375a3264", timeout=0.3)
    except :
        print('Timeout has been raised.')

def test_validate_JSON_Data(test_setup):
    validJsonData = """{"Title":"A Star Is Born","Year":"2018","Rated":"R","Released":"05 Oct 2018","Runtime":"136 min","Genre":"Drama, Music, Romance","Director":"Bradley Cooper","Writer":"Eric Roth, Bradley Cooper, Will Fetters","Actors":"Lady Gaga, Bradley Cooper, Sam Elliott","Plot":"A musician helps a young singer find fame as age and alcoholism send his own career into a downward spiral.","Language":"English, French","Country":"United States","Awards":"Won 1 Oscar. 95 wins & 280 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BNmE5ZmE3OGItNTdlNC00YmMxLWEzNjctYzAwOGQ5ODg0OTI0XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.6/10"},{"Source":"Rotten Tomatoes","Value":"90%"},{"Source":"Metacritic","Value":"88/100"}],"Metascore":"88","imdbRating":"7.6","imdbVotes":"378,998","imdbID":"tt1517451","Type":"movie","DVD":"19 Feb 2019","BoxOffice":"$215,333,122","Production":"N/A","Website":"N/A","Response":"True"}"""
    isValid = validate_JSON_DATA (validJsonData)
    print(isValid)

def test_validation_schema (test_setup):
    validate(instance={
        "Title": "A Star Is Born",
        "Year": "2018",
        "Rated": "R",
        "Released": "05 Oct 2018",
        "Runtime": "136 min",
        "Genre": "Drama, Music, Romance",
        "Director": "Bradley Cooper",
        "Writer": "Eric Roth, Bradley Cooper, Will Fetters",
        "Actors": "Lady Gaga, Bradley Cooper, Sam Elliott",
        "Plot": "A musician helps a young singer find fame as age and alcoholism send his own career into a downward spiral.",
        "Language": "English, French",
        "Country": "United States",
        "Awards": "Won 1 Oscar. 95 wins & 280 nominations total",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNmE5ZmE3OGItNTdlNC00YmMxLWEzNjctYzAwOGQ5ODg0OTI0XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
        "Ratings": [
            {
                "Source": "Internet Movie Database",
                "Value": "7.6/10"
            },
            {
                "Source": "Rotten Tomatoes",
                "Value": "90%"
            },
            {
                "Source": "Metacritic",
                "Value": "88/100"
            }
        ],
        "Metascore": "88",
        "imdbRating": "7.6",
        "imdbVotes": "378,998",
        "imdbID": "tt1517451",
        "Type": "movie",
        "DVD": "19 Feb 2019",
        "BoxOffice": "$215,333,122",
        "Production": "N/A",
        "Website": "N/A",
        "Response": "True"
    }, schema=schema,)

