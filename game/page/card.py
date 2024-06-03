import flet as ft

CARD_WIDTH = 70
CARD_HEIGHT = 100
DROP_PROXIMITY = 20


class Card(ft.Card):
    def __init__(self, suite, rank):
        super().__init__()
        self.suite = suite
        self.rank = rank
        self.slot = None
        self.content = ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            border_radius=ft.border_radius.all(4),
            content=ft.Image(src="/images/card_back.png"),
        )

