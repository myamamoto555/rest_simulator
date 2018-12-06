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

                "rating": {"inform": ["このお店の評価値は%sです。", "%sです"],
                            "request": ["評価値はどれくらいですか。", "お店の評判を教えて"]},

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

    usr_slots = [("loc", "location city", ["大崎", "東京", "品川", "町田",
                                           "国分寺", "三鷹", "新宿",
                                           "渋谷", "立川", "八王子"]),
                 ("food_pref", "food preference", ["タイ料理", "中華", "韓国料理", "和食",
                                                   "ロシア料理", "洋食", "イタリアン", "フレンチ",
                                                   "カフェ", "メキシコ料理", "ハワイ料理", "お寿司"])]

    sys_slots = [("price", "average price per person", ["cheap", "moderate", "expensive"]),
                 ("rating", "customer rating", ["1", "2", "3", "4", "5"])]

    db_size = 100


if __name__ == "__main__":
    test_size = 500
    train_size = 2000
    gen_bot = Generator()

    rest_spec = RestSpec()

    # restaurant
    gen_bot.gen_corpus("test", rest_spec, complexity.PropSpec, test_size)


