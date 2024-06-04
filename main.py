import flet as ft
from flet_core import Container, Row, Column, Image, Text
from flet_core.alignment import center
from flet_core.types import AppView

from game.logic.core import get_total_value
from game.page.solitaire import Solitaire, Role


def main(page: ft.Page):
    solitaire = Solitaire()

    def alert_dialog(title):
        dlg.title = Text(title)
        dlg.content = Text("Dealer Score:" + str(get_total_value(solitaire.dealer_scores)) + " vs " + "User Score:" + str(
            get_total_value(solitaire.user_scores)))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def reset_game(e):
        solitaire.reset()
        deal_card_button.disabled = False
        user_hit_button.disabled = True
        user_stand_button.disabled = True
        user_table_row.controls = []
        dealer_table_row.controls = []
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        modal=True,
        title=Text("result"),
        actions=[
            ft.TextButton("Yes", on_click=reset_game),
        ],
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    remain_area = Container(
        # bgcolor=ft.colors.ORANGE_300,
        content=Column(
            wrap=False,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[]
        )
    )

    def start_game(e):
        start_game_button.disabled = True
        solitaire.create_card_deck()
        remain_area.content = solitaire
        control_area_col.controls.append(deal_card_button)
        deck_view.update()

    start_game_button = ft.ElevatedButton(
        text="开始", on_click=start_game, icon=ft.icons.CATCHING_POKEMON
    )

    def deal_card(e):
        deal_card_button.disabled = True
        user_table_row.controls.append(Image(src=solitaire.deal_cards(Role.USER), width=70, height=100))
        dealer_table_row.controls.append(Image(src=solitaire.deal_cards(Role.DEALER), width=70, height=100))
        user_table_row.controls.append(Image(src=solitaire.deal_cards(Role.USER), width=70, height=100))
        user_hit_button.disabled = False
        user_stand_button.disabled = False
        control_area_col.controls.extend([user_hit_button, user_stand_button])
        deck_view.update()

    deal_card_button = ft.ElevatedButton(
        text="发牌", on_click=deal_card, icon=ft.icons.SPOKE_OUTLINED
    )

    def hit_card(e):
        user_table_row.controls.append(Image(src=solitaire.deal_cards(Role.USER), width=70, height=100))
        user_table_row.update()
        total_user_scores = get_total_value(solitaire.user_scores)
        if total_user_scores > 21:
            alert_dialog("Dealer Win!!!")
        elif total_user_scores == 21:
            stand_card(e)

    user_hit_button = ft.ElevatedButton(
        text="要牌", on_click=hit_card, icon=ft.icons.SQUARE_SHARP
    )

    def stand_card(e):
        while True:
            dealer_table_row.controls.append(Image(src=solitaire.deal_cards(Role.DEALER), width=70, height=100))
            if get_total_value(solitaire.dealer_scores) >= 17:
                break
        total_dealer_scores = get_total_value(solitaire.dealer_scores)
        total_user_scores = get_total_value(solitaire.user_scores)
        if total_dealer_scores > 21:
            alert_dialog("User Win!!!")
        elif total_user_scores > total_dealer_scores:
            alert_dialog("User Win!!!")
        elif total_user_scores == total_dealer_scores:
            alert_dialog("Draw!!!")
        else:
            alert_dialog("Dealer Win!!!")

    user_stand_button = ft.ElevatedButton(
        text="不要", on_click=stand_card, icon=ft.icons.CROP_SQUARE_SHARP
    )

    control_area_col = Column(
        wrap=False,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[start_game_button],
    )

    dealer_table_row = Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=2,
        wrap=True,
    )

    user_table_row = Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=2,
        wrap=True,
    )

    deck_view = Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            Column(
                width=150,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=False,
                controls=[
                    remain_area,
                    Container(control_area_col)
                ]),
            Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=False,
                controls=[
                    Container(
                        alignment=center,
                        bgcolor=ft.colors.BLUE_300,
                        width=600,
                        height=250,
                        content=dealer_table_row
                    ),
                    Container(
                        alignment=center,
                        bgcolor=ft.colors.GREEN_100,
                        width=600,
                        height=250,
                        content=user_table_row
                    )
                ])
        ])

    page.adaptive = True

    page.appbar = ft.AppBar(
        leading=ft.Image(src=f"/images/card.png"),
        leading_width=30,
        title=ft.Text("1v1 Black Jack 21"),
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    page.add(deck_view)


ft.app(target=main, assets_dir="assets", view=AppView.WEB_BROWSER)
