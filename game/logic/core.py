import random as rd

basic_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def create_all_cards(num_decks=1):
    """Creates a list of cards for playing, optionally specifying the number of decks."""
    return basic_cards * num_decks


def get_card_value(card):
    """Returns the point value of a given card."""
    if card in [11, 12, 13]:
        return 10
    elif card == 1:
        return 11  # Ace can be 1 or 11
    else:
        return card


def get_total_value(cards):
    """Calculates the total point value of a list of cards."""
    print("get_total_value")
    print(cards)
    total_value = sum(get_card_value(card) for card in cards)
    # Adjust for Ace value if necessary
    if 1 in cards and total_value > 21:
        total_value -= 10  # Count Ace as 1 instead of 11
    print(total_value)
    return total_value


def deal_card(cards):
    """Deals a random card from the given card list and removes it."""
    card = rd.choice(cards)
    cards.remove(card)
    return card


def deal_cards(cards, num_cards):
    """Deals a specified number of cards from the given card list and returns them as a list."""
    dealt_cards = []
    for _ in range(num_cards):
        dealt_cards.append(deal_card(cards))
    return dealt_cards


def show_cards(cards, hide_first_card=True):
    """Prints the cards in a given list, optionally hiding the first card."""
    if hide_first_card:
        print("Dealer cards: [?", *[get_card_value(card) for card in cards[1:]])
    else:
        print("Dealer cards:", [get_card_value(card) for card in cards])
    print("User cards:", [get_card_value(card) for card in cards])


def check_bust(cards):
    """Checks if the given list of cards exceeds the 21-point limit."""
    return get_total_value(cards) > 21


def play_user_turn(user_cards, all_cards):
    """Handles the user's turn, allowing them to hit or stand."""
    while True:
        action = input("Hit (h) or Stand (s)? ").lower()
        if action in ["h", "s"]:
            break
        else:
            print("Invalid action. Please enter 'h' to hit or 's' to stand.")

    if action == "h":
        user_cards.append(deal_card(all_cards))
        print("User draws a", get_card_value(user_cards[-1]))
        show_cards(user_cards)

        if check_bust(user_cards):
            print("User busts!")
            return False  # User loses

    return True  # User continues


def play_dealer_turn(dealer_cards, all_cards):
    """Handles the dealer's turn, following the dealer's rules."""
    while get_total_value(dealer_cards) < 17:
        dealer_cards.append(deal_card(all_cards))
        print("Dealer draws a", get_card_value(dealer_cards[-1]))
        show_cards(dealer_cards)

    if check_bust(dealer_cards):
        print("Dealer busts!")
        return True  # Dealer loses

    return False  # Dealer continues


def determine_winner(user_value, dealer_value):
    """Determines the winner based on the final card values."""
    if user_value > 21:
        return "Dealer"  # User busts
    elif dealer_value > 21:
        return "User"  # Dealer busts
    elif user_value == dealer_value:
        return "Tie"
    elif user_value > dealer_value:
        return "User"
    else:
        return "Dealer"


def play_blackjack():
    """Plays a single round of Blackjack."""
    num_decks = int(input("Enter the number of decks to use (1-8): "))
    # Check for valid number of decks
    while num_decks < 1 or num_decks > 8:
        num_decks = int(input("Invalid number of decks. Please enter a number between 1 and 8: "))

    # Create the deck of cards
    all_cards = create_all_cards(num_decks)
    rd.shuffle(all_cards)

    # Deal initial cards to the user and dealer
    user_cards = deal_cards(all_cards, 2)
    dealer_cards = deal_cards(all_cards, 2)

    # Show the cards to the player
    show_cards(user_cards, hide_first_card=False)
    show_cards(dealer_cards, hide_first_card=True)

    # Play the user's turn
    user_bust = not play_user_turn(user_cards, all_cards)

    # End game if user busts
    if user_bust:
        print("Dealer wins!")
        return

    # Dealer's turn
    dealer_bust = play_dealer_turn(dealer_cards, all_cards)

    # Show the final cards
    show_cards(user_cards)
    show_cards(dealer_cards)

    # Determine the winner
    user_value = get_total_value(user_cards)
    dealer_value = get_total_value(dealer_cards)
    winner = determine_winner(user_value, dealer_value)

    if winner == "User":
        print("User wins!")
    elif winner == "Dealer":
        print("Dealer wins!")
    else:
        print("It's a tie!")


# # Play the game
# while True:
#     play_blackjack()
#     play_again = input("Play again? (y/n): ").lower()
#     if play_again != "y":
#         break
