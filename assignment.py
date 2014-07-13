import sys
import random

SUITS = ['CLUB', 'SPADE', 'HEART', 'DIAMOND']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

SCORE = 0
CHIPS_MAX = 100
MESSAGE = ""
RESULT = ""
KEYS = {'HIT':'A','STAND':'B','DEAL':'C','DOUBLE_DOWN':'D','BET':'E'}
GAME_IN_PROGRESS = False


class Card(object):
	def __init__(self, suit, rank):
		if (suit in SUITS) and (rank in RANKS):
			self._suit = suit
			self._rank = rank
		else:
			self._suit = None
			self._rank = None

	def __str__(self):
		return "{%s-%s}"%(self._suit,self._rank)

	def __repr__(self):
		return "{%s-%s}"%(self._suit,self._rank)

	def get_suit(self):
		return self._suit

	def get_rank(self):
		return self._rank

class Deck:
    def __init__(self):
        popped = []
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffle()
        
    def __str__(self):
        s = ''
        for c in self.cards:
            s = s + str(c) + ' '
        return s

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        popped = self.cards.pop(0)
        return popped

deck = Deck()

class Hand:
    def __init__(self):
        self.player_hand = []

    def __str__(self):
        s = ''
        for c in self.player_hand:
            s = s + str(c) + ' '
        return s

    def add_card(self, card):
        self.player_hand.append(card)
        return self.player_hand

    def show_hand(self):
    	as_string = ""
    	for c in  self.player_hand:
    		as_string = as_string+str(c)+"  "
    	return as_string

    def get_value(self):
        value = 0
        for card in self.player_hand:
            rank = card.get_rank()
            value = value + VALUES[rank]
        for card in self.player_hand:
            rank = card.get_rank()    
            if rank == 'A' and value <= 11:
                value += 10
        return value

# PLAYER_CARDS = Hand()
# DEALER_CARDS = Hand()

class Game(object):
	_chips = CHIPS_MAX
	_current_bet = 1
	_deal_in_progress = False

	def deal(self):
    # deal function deals initial hands and adjusts MESSAGE
		global GAME_IN_PROGRESS, PLAYER_CARDS, DEALER_CARDS, deck, MESSAGE, SCORE, RESULT
		SCORE = 0
		self._deal_in_progress = True
		if GAME_IN_PROGRESS:
			MESSAGE = "Do you want to Hit or Stand?"
			SCORE -= 1
			deck = Deck()
			PLAYER_CARDS = Hand()
			DEALER_CARDS = Hand()
			PLAYER_CARDS.add_card(deck.deal_card())
			DEALER_CARDS.add_card(deck.deal_card())
			PLAYER_CARDS.add_card(deck.deal_card())
			DEALER_CARDS.add_card(deck.deal_card())
		else:
			deck = Deck()
			PLAYER_CARDS = Hand()
			DEALER_CARDS = Hand()
			PLAYER_CARDS.add_card(deck.deal_card())
			DEALER_CARDS.add_card(deck.deal_card())
			PLAYER_CARDS.add_card(deck.deal_card())
			DEALER_CARDS.add_card(deck.deal_card())
			MESSAGE = "Do you want to Hit or Stand?"
		GAME_IN_PROGRESS = True
		RESULT = ""

	def get_current_chips(self):
		return self._chips

	def bet_change_menu(self):
		true_value = False
		print 'Please enter an integer value for the current bet, must be between 1-100'
		while not true_value:
			inp = raw_input()
			if str(inp).isdigit():
				if int(inp) < 1 or int(inp) > 99:
					print 'Value not in range, please enter an integer between 1-100'
					true_value = False
				self._current_bet = int(inp)
				true_value = True
			else:
				print 'Should be integer, please try again'
				true_value = False


	def hit(self):
	    # deals PLAYER_CARDS a new hand and ends hand if it causes a bust.
	    global GAME_IN_PROGRESS, SCORE, MESSAGE
	    if GAME_IN_PROGRESS == True and self._deal_in_progress:
	        PLAYER_CARDS.add_card(deck.deal_card())
	        MESSAGE = "Would you like to Hit or Stand?"
	        if PLAYER_CARDS.get_value() > 21:
	            # GAME_IN_PROGRESS = False
	            self._deal_in_progress = False
	            MESSAGE = "You are busted! You Lose! Deal again?"
	            self._chips = int(self._chips) - int(self._current_bet)
	            SCORE -= 1
	            RESULT = "Dealer : " + str(DEALER_CARDS.get_value()) + "  You: " + str(PLAYER_CARDS.get_value())

	def stand(self):
	    global GAME_IN_PROGRESS, SCORE, MESSAGE, RESULT
	    if not self._deal_in_progress:
	        MESSAGE = "The hand is already over. Deal again?."
	    else:
	        while DEALER_CARDS.get_value() < 17:
	            DEALER_CARDS.add_card(deck.deal_card())
	        if DEALER_CARDS.get_value() > 21:
				self._chips = self._chips + self._current_bet
				MESSAGE = "Congratulations! The Dealer is busted. You win! Deal again?"
				SCORE += 1
				self._deal_in_progress = False
				# GAME_IN_PROGRESS = False
	            
	        elif DEALER_CARDS.get_value() > PLAYER_CARDS.get_value():
				self._chips = self._chips - self._current_bet
				MESSAGE = "Dealer wins! Play again?"
				SCORE -= 1
				self._deal_in_progress = False
				# GAME_IN_PROGRESS = False
	        
	        elif DEALER_CARDS.get_value() == PLAYER_CARDS.get_value():
	            MESSAGE = "Tied! The Dealer is given the game in case of tie. Deal again?"
	            self._chips = self._chips - self._current_bet
	            SCORE -= 1
	            self._deal_in_progress = False
	            # GAME_IN_PROGRESS = False
	        
	        elif DEALER_CARDS.get_value() < PLAYER_CARDS.get_value():
				self._chips = self._chips + self._current_bet
				MESSAGE = "Congratulations! You win! Deal again?"
				SCORE += 1
				self._deal_in_progress = False
				# GAME_IN_PROGRESS = False
	            
	        RESULT = "DEALER_CARDS: " + str(DEALER_CARDS.get_value()) + "  PLAYER_CARDS: " + str(PLAYER_CARDS.get_value())
        
	def is_game_end(self):
		global GAME_IN_PROGRESS
		if self._chips <= 0:
			GAME_IN_PROGRESS = False	

	def instructions(self):
		return "Press %s for Hit, %s for Stand, %s for Deal and to change Bet press %s"%(KEYS['HIT'],KEYS['STAND'],KEYS['DEAL'],KEYS['BET'])

	def table_draw(self):
		global GAME_IN_PROGRESS, SCORE, MESSAGE, RESULT,PLAYER_CARDS,DEALER_CARDS
		print """
**************************************************************
  %s
**************************************************************
CHIPS : $ %s
CURRENT BET : $ %s
--------------

PLAYER_CARDS :  %s
		
DEALER_CARDS :  %s


SCORE : %s        RESULT : %s
**************************************************************
  %s 
**************************************************************
	"""%(MESSAGE,self.get_current_chips(),self._current_bet,PLAYER_CARDS.show_hand(),DEALER_CARDS.show_hand(),SCORE,RESULT,self.instructions())


def main_function():
	global GAME_IN_PROGRESS,KEYS,RESULT
	c = Game()
	c.deal()
	c.table_draw()
	while GAME_IN_PROGRESS:
		inp = raw_input()
		if inp == KEYS['HIT'] or inp == KEYS['HIT'].lower():
			c.hit()
		elif inp == KEYS['STAND'] or inp == KEYS['STAND'].lower():
			c.stand()
		elif inp == KEYS['DEAL'] or inp == KEYS['DEAL'].lower():
			c.deal()
		elif inp == KEYS['BET'] or inp == KEYS['BET'].lower():
			c.bet_change_menu()
		RESULT = "PLAYER_CARDS = %s , DEALER_CARDS = %s"%(PLAYER_CARDS.get_value(),DEALER_CARDS.get_value())
		c.table_draw()
		c.is_game_end()
	print "The game ended. If you want to play again press P, Press any other key for exit"
	inp = raw_input()
	if inp == 'p' or inp == 'P':
		main_function()
	else:
		exit()


if __name__ == '__main__':
	main_function()
