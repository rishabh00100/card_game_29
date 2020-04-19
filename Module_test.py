from Module import *

deckofCard = DeckOfCards()
#name, bid, hand, score, bidpass = False
Player1 = player("Player_1", 0, None, 0, False)
Player2 = player("Player_2", 0, None, 0, False)
Player3 = player("Player_3", 0, None, 0, False)
Player4 = player("Player_4", 0, None, 0, False)

PlayerSet = (Player1, Player2, Player3, Player4)
Team1 = (Player1.name, Player3.name)
Team2 = (Player2.name, Player4.name)


deckofCard.shuffleDeck()
print("DISTRIBUTING 4 CARDS PER PLAYER")
PlayerSet = deckofCard.dealCards(PlayerSet)

FirstBidRound = BiddingRound(PlayerSet)
FirstBidRound.startBiddingRound()
HigherBidder = FirstBidRound.DeclareBidWinner(Team1)
# HigherBid, HigherBidder = startBiddingRound(PlayerSet)
# DeclareBidWinner(HigherBid, HigherBidder, Team1)

FirstRound = PlayRound()
TrumpSuite = FirstRound.SetTrump(HigherBidder)

print("DEALING REMAINING CARDS")
PlayerSet = deckofCard.dealCards(PlayerSet)

print("LETS START THE GAME")

cardsInATurn = {}
isTrumpOpen = False
FirstPlayerofRound = Player1.name
for player in PlayerSet:
    CardPlayed = 999
    print("")
    print("{PlayerName}, your turn to play".format(PlayerName = player.name))
    player.showHandToPlay()
    ValidCards = getValidCards(player, cardsInATurn, isTrumpOpen, FirstPlayerofRound, TrumpSuite)
    for card in ValidCards:
        if card.validity == 1:
            print(card.cardName())
    valid_moves = getValidIndex(ValidCards)
    print(valid_moves)
    while CardPlayed not in valid_moves:
        try:
            CardPlayed = int(input("Play:"))
        except ValueError:
            print("Please provide integer input")
    cardsInATurn[player.name] = player.hand[CardPlayed]
CalcHandWinner(cardsInATurn)

print(cardsInATurn)
print(cardsInATurn['Player_1'].score)