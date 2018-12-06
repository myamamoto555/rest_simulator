# -*- coding: utf-8 -*-
# author: Tiancheng Zhao
from simdial.domain import Domain, DomainSpec
from simdial.generator import Generator
from simdial import complexity
import string


class RestSpec(DomainSpec):
    name = "restaurant"
    greet = "Welcome to restaurant recommendation system."
    nlg_spec = {"loc": {"inform": ["I am at %s.", "%s.", "I'm interested in food at %s.", "At %s.", "In %s."],
                        "request": ["Which city are you interested in?", "Which place?"]},

                "food_pref": {"inform": ["I like %s food.", "%s food.", "%s restaurant.", "%s."],
                              "request": ["What kind of food do you like?", "What type of restaurant?"]},

                "open": {"inform": ["The restaurant is %s.", "It is %s right now."],
                         "request": ["Tell me if the restaurant is open.", "What's the hours?"],
                         "yn_question": {'open': ["Is the restaurant open?"],
                                         'closed': ["Is it closed?"]
                                         }},

                "parking": {"inform": ["The restaurant has %s.", "This place has %s."],
                            "request": ["What kind of parking does it have?.", "How easy is it to park?"],
                            "yn_question": {'street parking': ["Does it have street parking?"],
                                            "valet parking": ["Does it have valet parking?"]
                                            }},

                "price": {"inform": ["The restaurant serves %s food.", "The price is %s."],
                          "request": ["What's the average price?", "How expensive it is?"],
                          "yn_question": {'expensive': ["Is it expensive?"],
                                          'moderate': ["Does it have moderate price?"],
                                          'cheap': ["Is it cheap?"]
                                          }},

                "default": {"inform": ["Restaurant %s is a good choice."],
                            "request": ["I need a restaurant.",
                                        "I am looking for a restaurant.",
                                        "Recommend me a place to eat."]}
                }

    usr_slots = [("loc", "location city", ["Pittsburgh", "New York", "Boston", "Seattle",
                                           "Los Angeles", "San Francisco", "San Jose",
                                           "Philadelphia", "Washington DC", "Austin"]),
                 ("food_pref", "food preference", ["Thai", "Chinese", "Korean", "Japanese",
                                                   "American", "Italian", "Indian", "French",
                                                   "Greek", "Mexican", "Russian", "Hawaiian"])]

    sys_slots = [("open", "if it's open now", ["open", "closed"]),
                 ("price", "average price per person", ["cheap", "moderate", "expensive"]),
                 ("parking", "if it has parking", ["street parking", "valet parking", "no parking"])]

    db_size = 100


if __name__ == "__main__":
    test_size = 500
    train_size = 2000
    gen_bot = Generator()

    rest_spec = RestSpec()

    # restaurant
    gen_bot.gen_corpus("test", rest_spec, complexity.PropSpec, test_size)


