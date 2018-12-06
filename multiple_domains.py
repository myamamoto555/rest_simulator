# -*- coding: utf-8 -*-
# author: Tiancheng Zhao
from simdial.domain import Domain, DomainSpec
from simdial.generator import Generator
from simdial import complexity
import string


class RestSpec(DomainSpec):
    name = "restaurant"
    greet = "レストラン検索システムです。"
    nlg_spec = {"loc": {"inform": ["%s。", "%sで食べたいです。", "%sでお願いします。"],
                        "request": ["どこで食べたいですか。", "場所はどこがいいですか。"]},

                "food_pref": {"inform": ["%sがいいです。", "%sが食べたい。", "%s"],
                              "request": ["何を食べたいですか。", "食べたいものはありますか。"]},

                "price": {"inform": ["このお店は%sです。", "値段は%s。"],
                          "request": ["値段はどれくらいですか。", "平均価格を教えて下さい。"],
                          "yn_question": {'expensive': ["高いですか。"],
                                          'moderate': ["妥当な値段ですか。"],
                                          'cheap': ["安いですか。"]
                                          }},

                "default": {"inform": ["%sはいかがでしょうか。"],
                            "request": ["お勧めはありますか。",
                                        "レストランを探しています。"]}
                }

    usr_slots = [("loc", "location city", ["Pittsburgh", "New York", "Boston", "Seattle",
                                           "Los Angeles", "San Francisco", "San Jose",
                                           "Philadelphia", "Washington DC", "Austin"]),
                 ("food_pref", "food preference", ["Thai", "Chinese", "Korean", "Japanese",
                                                   "American", "Italian", "Indian", "French",
                                                   "Greek", "Mexican", "Russian", "Hawaiian"])]

    sys_slots = [("price", "average price per person", ["cheap", "moderate", "expensive"])]

    db_size = 100


if __name__ == "__main__":
    test_size = 500
    train_size = 2000
    gen_bot = Generator()

    rest_spec = RestSpec()

    # restaurant
    gen_bot.gen_corpus("test", rest_spec, complexity.PropSpec, test_size)


