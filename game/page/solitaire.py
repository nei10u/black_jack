import random

import flet as ft

from game.page.card import Card
from enum import Enum, auto

SOLITAIRE_WIDTH = 200
SOLITAIRE_HEIGHT = 200


class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value


# 定义枚举类
class Role(Enum):
    DEALER = auto()
    USER = auto()


class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.controls = []
        self.cards = []
        self.dealer_scores = []
        self.user_scores = []

    def reset(self):
        self.dealer_scores = []
        self.user_scores = []

    def deal_cards(self, role):
        remaining_cards = self.cards
        top_card = remaining_cards[0]
        remaining_cards.remove(top_card)
        if role == Role.DEALER:
            self.dealer_scores.append(top_card.rank.value)
        elif role == Role.USER:
            self.user_scores.append(top_card.rank.value)
        return f"/images/{top_card.rank.name}_{top_card.suite.name}.svg"

    def create_card_deck(self):
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                file_name = f"{rank.name}_{suite.name}.svg"
                print(file_name)
                self.cards.append(Card(suite=suite, rank=rank))
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
