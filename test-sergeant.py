#Sergeant Major Quick Check to see if solvable easily with perfect information
# 0## clubs, 1## diamonds, 2## hearts, 3## spades
# #02 2, #03 3, #10 10, #11 J, #12 Q, #13 K, #14 A
# Hands targets are: [5, 3, 8] for players 0, 1, 2 respectively also known as eldest, middle, youngest/dealer respectively.
DEALER, ELDEST, MIDDLE = 2, 0, 1
EIGHT, FIVE, THREE = 2, 0, 1

import random
import copy

# Game state class
class GameState:
    def __init__(self, starting_exchanges = [0, 0, 0]):
        #Start with exchanges (if any), or start with player 2 exchange to kitty
        self.current_player = max((count >= 0) * player for count,player in zip(starting_exchanges, [0, 1, 2]))
        #Data for initial exchanges
        self.starting_exchanges = starting_exchanges
        self.starting_exchanges_remaining = starting_exchanges.copy()
        self.starting_exchanges_complete = [] #list of tuples (high_player, card_given, low_player, card_given)
        self.starting_exchanges_complete_flag = sum([x for x in starting_exchanges if x > 0]) == 0 
        #Trump suit
        self.trump_suit = None
        #Kitty Echange data
        self.dealer_exchanged_into_kitty = [] #Cards exchanged into kitty by dealer, if less than 4, exchange not complete
        self.dealer_removed_from_kitty = [] #Cards removed from kitty by dealer
        self.dealer_revealed_kitty_cards = [] #list of tuples (player_seeing_card, card_shown); When dealer gives away a card lower than drawn from Kitty, must show it
        self.kitty_exchange_complete_flag = False
        self.hands = [[[] for _ in range(4)] for _ in range(3)]  # 3 players, each with 4 suits
        self.kitty = [[] for _ in range(4)]  # Kitty with 4 suits
        #Normal Playing data
        self.trick_history = [[]]
        self.lead_history = [0] #Already know the first lead player
        self.scores = [0, 0, 0]  # Scores for each player
        #Start at negative trick number based on number of starting exchanges
        #Trump suit set is trick -5, kitty exchange is trick -4 -3 -2 -1, so that the first trick after exchanges is trick 0
        self.trick_number = -5 + -1*sum([x for x in starting_exchanges if x > 0])
        # Shuffle and deal the deck
        self._shuffle_and_deal()
    
    def _shuffle_and_deal(self):
        """Create, shuffle, and deal the deck to players and kitty"""
        # Create deck
        deck = []
        for suit in range(4):
            for rank in range(2, 15):
                card = 100 * suit + rank
                deck.append(card)
        
        # Shuffle deck
        random.shuffle(deck)
        
        # Deal 16 cards to each player, remaining to kitty
        for i in range(52):
            suit = deck[i] // 100
            if i < 48:
                player = i % 3
                self.hands[player][suit].append(deck[i])
            else:
                self.kitty[suit].append(deck[i])
        
        # Sort each hand and kitty within each suit
        for i in range(3):
            for suit in range(4):
                self.hands[i][suit].sort()
        for suit in range(4):
            self.kitty[suit].sort()
    
    def serialize(self):
        """Serialize game state for dictionary search"""
        #For simplicity at the moment, use the formatted string
        return self.formatted_string()
    
    def copy(self):
        """Create a deep copy of the game state"""
        new_state = GameState.__new__(GameState)  # Create instance without calling __init__
        new_state.hands = copy.deepcopy(self.hands)
        new_state.kitty = copy.deepcopy(self.kitty)
        new_state.current_player = self.current_player
        new_state.scores = self.scores.copy()
        new_state.trick_number = self.trick_number
        new_state.trump_suit = self.trump_suit
        new_state.starting_exchanges = self.starting_exchanges.copy()
        new_state.trick_history = copy.deepcopy(self.trick_history)
        new_state.lead_history = copy.deepcopy(self.lead_history)
        new_state.starting_exchanges_remaining = self.starting_exchanges_remaining.copy()
        new_state.starting_exchanges_complete_flag = self.starting_exchanges_complete_flag
        new_state.kitty_exchange_complete_flag = self.kitty_exchange_complete_flag
        new_state.dealer_exchanged_into_kitty = self.dealer_exchanged_into_kitty.copy()
        new_state.dealer_removed_from_kitty = copy.deepcopy(self.dealer_removed_from_kitty)
        new_state.starting_exchanges_complete = copy.deepcopy(self.starting_exchanges_complete)
        new_state.dealer_revealed_kitty_cards = copy.deepcopy(self.dealer_revealed_kitty_cards)
        return new_state
    
    def __repr__(self):
        return self.formatted_string_2()
    
    def card_to_string(self, card):
        if card is None:
            return "??"
        return str(card//100) + "0023456789TJQKA"[(card % 100)]
    
    def formatted_string_2(self, color_flag=False):
        #Format setter, operated on each symbol to properly format the symbol and coloring
        def format_set(text:str, highlight, header_flag = False):
            # text: string to format
            # highlight: 0 for no highlight, 1 for highlight in lowercase, 2 for highlight in uppercase
            if highlight == 0:
                return text
            elif not header_flag:
                return text
            elif highlight == 1:
                if text == "#":
                    return "+"
                else:
                    return text.lower()
            elif highlight == 2:
                return text
        first_trick = -5 + -1*sum([x for x in self.starting_exchanges if x > 0])
        current_trick = self.trick_history[-1]
        lead_player = self.lead_history[-1]
        previous_trick = self.trick_history[-2] if len(self.trick_history) > 1 else []
        previous_trick_leader = self.lead_history[-2] if len(self.lead_history) > 1 else lead_player
        #Setup a matrix structure for the data
        s = {"intro": {"header":"", 0:"", 1:"", 2:"", "info":""},
             "state": [[{"header":" ", 0:".", 1:".", 2:".", "info":" "} for card in range(15)] for suit in range(4)],
             "history": [{"header":"   ", 0:"   ", 1:"   ", 2:"   ", "info":"   "} for trick in range(first_trick, 17)]
            }
        #Start by setting up the intros
        s["intro"]["header"] = f"Round: {self.trick_number}"
        player_names =["Eldest", "Middle", "Dealer"]
        for player in range(3):
            turn_marker = "*" if player == self.current_player else " "
            s["intro"][player] = f"  {turn_marker}{player_names[player]} {self.starting_exchanges[player]:+d} ({self.scores[player]}/{[5, 3, 8][player]}):"
        #Setup what is shown for each card in the state as a baseline, take into account known information about what has been played
        #Start by assuming we don't know where anything is
        for suit in range(4):
            for card in range(2, 15):
                for player in range(3):
                    if player == self.current_player:
                        s["state"][suit][card][player] = "."
                    else:
                        s["state"][suit][card][player] = "?"
        #Handle cards with unknown positions
        def filter_unknown(card):
            if card is None:
                return True
            for player in range(3):
                s["state"][card // 100][card % 100][player] = "." #Card position known, override the "?"
        #Mark player exchanges
        def mark_player_exhange(exchange_complete, highlight):
            high_player, card_given, low_player, card_returned = exchange_complete
            if filter_unknown(card_given) or filter_unknown(card_returned): #Returns or marks with "."
                return
            elif card_given == card_returned:
                if highlight != 0: s["state"][card_given // 100][card_given % 100]["header"] = format_set("E", highlight, True)
                s["state"][card_given // 100][card_given % 100][high_player] = format_set(self.card_to_string(card_given)[1], highlight)
                if highlight != 0: s["state"][card_given // 100][card_given % 100][low_player] = format_set("#", highlight)
            else:
                if highlight != 0: s["state"][card_given // 100][card_given % 100]["header"] = format_set("G", highlight, True)
                if highlight != 0: s["state"][card_given // 100][card_given % 100][high_player] = format_set("#", highlight)
                s["state"][card_given // 100][card_given % 100][low_player] = format_set(self.card_to_string(card_given)[1], highlight)
                if highlight != 0: s["state"][card_returned // 100][card_returned % 100]["header"] = format_set("T", highlight, True)
                s["state"][card_returned // 100][card_returned % 100][high_player] = format_set(self.card_to_string(card_returned)[1], highlight)
                if highlight != 0: s["state"][card_returned // 100][card_returned % 100][low_player] = format_set("#", highlight)
        def mark_into_kitty(card, highlight):
            if filter_unknown(card):#Returns or marks with "."
                return
            if highlight != 0: s["state"][card // 100][card % 100]["header"] = format_set("K", highlight, True)
            if highlight != 0: s["state"][card // 100][card % 100]["header"] = format_set("K", highlight, True)
            if highlight != 0: s["state"][card // 100][card % 100][DEALER] = format_set("#", highlight)
        def mark_removed_from_kitty(card, highlight):
            if filter_unknown(card): #Returns or marks with "."
                return
            if highlight != 0: s["state"][card // 100][card % 100]["header"] = format_set("R", highlight, True)
            s["state"][card // 100][card % 100][DEALER] = format_set(self.card_to_string(card)[1], highlight)
            #See if the card was revealed
            for player_seeing_card, card_shown in self.dealer_revealed_kitty_cards:
                if card_shown == card:
                    if highlight != 0: s["state"] [card // 100][card % 100]["header"] = format_set("S", highlight, True) #S for shown
                if highlight != 0: s["state"][card // 100][card % 100][player_seeing_card] = format_set("o", highlight)
                break #Skips further checks since the card only needs to be revealed once
        def mark_trick(leader, winner, trick, highlight):
            for card in trick:
                if filter_unknown(card): #Returns or marks with "."
                    return
            trick_player_order = [(leader + i) % 3 for i in range(3)]
            for player, card in zip(trick_player_order, trick):
                if player == leader and player == winner:
                    char = "M"
                elif player == leader:
                    char = "L"
                elif player == winner:
                    char = "W"
                else:
                    char = "F"
                if highlight != 0: s["state"][card // 100][card % 100]["header"] = format_set(char, highlight, True)
                if highlight != 0: s["state"][card // 100][card % 100][player] = format_set("#", highlight)
        #GO THROUGH THE FULL HISTORY
        #Mark all exchanged cards
        for exchange_complete in self.starting_exchanges_complete:
            mark_player_exhange(exchange_complete, highlight = 0)
        #Mark all kitty exchanged cards
        for card in self.dealer_exchanged_into_kitty:
            mark_into_kitty(card, highlight = 0)
        for card in [item for sublist in self.dealer_removed_from_kitty for item in sublist]:
            mark_removed_from_kitty(card, highlight = 0)
        #Mark all hands
        for player in range(3):
            for suit in range(4):
                for card in self.hands[player][suit]:
                    filter_unknown(card) #Returns or marks with "."
                    s["state"][card // 100][card % 100][player] = format_set(self.card_to_string(card)[1], 0)
        #Mark all played tricks
        for i, trick in enumerate(self.trick_history):
            leader = self.lead_history[i]
            if i < len(self.trick_history) - 1:
                #For all but the current trick, we know the winner
                winner = self.lead_history[i + 1]
            else:
                winner = None
            mark_trick(leader, winner, trick, highlight = 0)
        #NOW ACTUALLY HIGHLIGHT
        #Mark locations based on the current state of the game
        if self.trick_number < -4:
            #Show the exchanges between players
            for exchange_complete in self.starting_exchanges_complete:
                mark_player_exhange(exchange_complete, highlight = 1 + (exchange_complete == self.starting_exchanges_complete[-1]))
        elif self.trick_number <= 0 and len(current_trick) == 0:
            #Show the exchanges with the kitty by the dealer
            for card in self.dealer_exchanged_into_kitty:
                mark_into_kitty(card, highlight = 1 + (card == self.dealer_exchanged_into_kitty[-1]))
            #Show cards that the dealer gets back
            for card in [item for sublist in self.dealer_removed_from_kitty for item in sublist]:
                mark_removed_from_kitty(card, highlight = 1 + (card == self.dealer_removed_from_kitty[-1]))
        elif self.trick_number == 0:
            #Show the exchanges with the kitty by the dealer
            for card in self.dealer_exchanged_into_kitty:
                mark_into_kitty(card, highlight = 1)
            #Show cards that the dealer gets back
            for card in [item for sublist in self.dealer_removed_from_kitty for item in sublist]:
                mark_removed_from_kitty(card, highlight = 1)
            #Show the current trick if any cards have been played
            mark_trick(lead_player, None, current_trick, highlight = 2)
        elif len(current_trick) == 0:
            #Show the previous trick in upper
            mark_trick(previous_trick_leader, lead_player, previous_trick, highlight = 2)
        else:
            #Show the previous trick in lower and the current trick in upper
            mark_trick(previous_trick_leader, lead_player, previous_trick, highlight = 1)
            mark_trick(lead_player, None, current_trick, highlight = 2)
        #Show turn marker in history
        if self.trick_number < 16:
            s["history"][self.trick_number]["header"] = str(self.trick_number).rjust(3)
            s["history"][self.trick_number][self.current_player] = "  *" #Show turn marker in history
        #Setup the history of exchanges
        round_from_neg = first_trick
        for high_player, card_given, low_player, card_returned in self.starting_exchanges_complete:
            s["history"][round_from_neg]["header"] = str(round_from_neg).rjust(3)
            s["history"][round_from_neg][high_player] = f"^{self.card_to_string(card_given)}"
            s["history"][round_from_neg][low_player] = f"v{self.card_to_string(card_returned)}"
            round_from_neg += 1
        #History of trump suit selection
        if self.trump_suit is not None:
            s["history"][round_from_neg]["header"] = str(round_from_neg).rjust(3)
            s["history"][round_from_neg][DEALER] = f"T{self.trump_suit}0"
            round_from_neg += 1
        #History of dealer exchanges with kitty
        for i, card in enumerate(self.dealer_exchanged_into_kitty):
            s["history"][round_from_neg]["header"] = str(round_from_neg).rjust(3)
            s["history"][round_from_neg][DEALER] = f"^{self.card_to_string(card)}"
            dealer_removed_from_kitty_flat = [item for sublist in self.dealer_removed_from_kitty for item in sublist]
            #See if the player picking up cards should be shown
            if len(dealer_removed_from_kitty_flat) > i:
                s["history"][round_from_neg]["header"] = f"v{self.card_to_string(dealer_removed_from_kitty_flat[i])}"
                #See if a card was revealed
                for player_seeing_card, card_shown in self.dealer_revealed_kitty_cards:
                    if card_shown == dealer_removed_from_kitty_flat[i]:
                        s["history"][round_from_neg][player_seeing_card] = f"R{self.card_to_string(card_shown)}"
            round_from_neg += 1
        #History of played tricks
        for trick_number, trick in enumerate(self.trick_history[:-1]):
            s["history"][round_from_neg]["header"] = str(trick_number).rjust(3)
            trick_player_order = [(self.lead_history[trick_number] + i) % 3 for i in range(3)]
            for player, card in zip(trick_player_order, trick):
                #Mark the lead and the winning card, use char as we did above
                if player == self.lead_history[trick_number]:
                    if trick_number + 1 < len(self.lead_history) and player == self.lead_history[trick_number + 1]:
                        char = "M"
                    else:
                        char = "L"
                else:
                    if trick_number + 1 < len(self.lead_history) and player == self.lead_history[trick_number + 1]:
                        char = "W"
                    else:
                        char = "^"
                s["history"][round_from_neg][player] = f"{char}{self.card_to_string(card)}"
            round_from_neg += 1
        #Trick being currently played
        if len(current_trick) > 0:
            s["history"][round_from_neg]["header"] = str(round_from_neg).rjust(3)
            trick_player_order = [(lead_player + i) % 3 for i in range(len(current_trick))]
            for player, card in zip(trick_player_order, current_trick):
                if player == lead_player:
                    char = "L"
                else:
                    char = "^"
                s["history"][round_from_neg][player] = f"{char}{self.card_to_string(card)}"
            round_from_neg += 1
        #Format the string output
        condensed_matrix = {row_name:{"intro":"", "state": "", "history":""} for row_name in ["header", 0, 1, 2, "info"]}
        for line_name in ["header", 0, 1, 2, "info"]:
            condensed_matrix[line_name]["intro"] = s["intro"][line_name]
            state = ""
            for suit in range(4):
                state += " "
                state += "*" if suit == self.trump_suit and line_name in [0, 1, 2] else " "
                for card in range(2, 15):
                    state += s["state"][suit][card][line_name]
            condensed_matrix[line_name]["state"] = state
            history = ""
            for trick in range(first_trick, 17):
                history += " " + s["history"][trick][line_name]
            condensed_matrix[line_name]["history"] = history
        #Justify by each column, not printing the info column, seems unnecessary with full history shown
        as_matrix = [[condensed_matrix[line_name][column_name] for line_name in ["header", 0, 1, 2]] for column_name in ["intro", "state", "history"]]
        column_widths = [max(len(cell) for cell in column) for column in as_matrix]
        justified_matrix = []
        for line in range(4):
            justified_line = []
            for column in range(3):
                justified_line.append(as_matrix[column][line].ljust(column_widths[column]))
            justified_matrix.append(justified_line)
        lines = ["".join(justified_matrix[line]) for line in range(4)]
        return "\n".join(lines)
    
    def generate_legal_moves(self):
        #Returns a list of legal moves for the current player
        #Before the game starts, cards are exchanged between players and the kitty
        if self.starting_exchanges_complete_flag == False:
            #Order of exchanges should be target 8, 5, 3 for positive then negative 3, 5, 8
            for high_player, low_player in [(EIGHT, THREE), (EIGHT, FIVE), (FIVE, THREE), (FIVE, EIGHT), (THREE, FIVE), (THREE, EIGHT)]:
                if self.starting_exchanges_remaining[high_player] > 0 and self.starting_exchanges_remaining[low_player] < 0:
                    #High player can give a card to low player
                    self.current_player = high_player
                    legal_moves = []
                    for suit in range(4):
                        legal_moves.extend(self.hands[high_player][suit])
                    return legal_moves
            #We should never get here, thow an error
            raise Exception("Error in generate_legal_moves: No valid exchanges found during starting exchanges phase.")
        #Now the dealer sets the tump suit
        if self.trump_suit is None:
            legal_moves = [0, 100, 200, 300] #Select a suit without a card number defined
            return legal_moves
        #Now the dealer exhanges cards with the kitty
        if self.kitty_exchange_complete_flag == False:
            #Dealer places 4 cards into the kitty exchange
            if len(self.dealer_exchanged_into_kitty) < 4:
                self.current_player = 2
                legal_moves = []
                for suit in range(4):
                    legal_moves.extend(self.hands[2][suit])
                return legal_moves
            #We should never get here, thow an error
            raise Exception("Error in generate_legal_moves: Dealer has not placed 4 cards into the kitty exchange, but no valid moves found.")
        #In the main game playing a normal card
        lead_player = self.lead_history[-1]
        current_trick = self.trick_history[-1]
        if lead_player == self.current_player:
            # Lead player can play any card
            legal_moves = []
            for suit in range(4):
                legal_moves.extend(self.hands[self.current_player][suit])
            return legal_moves
        else:
            # Non-lead players must follow suit if possible
            lead_suit = current_trick[0] // 100
            if self.hands[self.current_player][lead_suit]:
                return self.hands[self.current_player][lead_suit]
            else:
                legal_moves = []
                for suit in range(4):
                    legal_moves.extend(self.hands[self.current_player][suit])
                return legal_moves
    
    def play_card(self, card):
        suit = card // 100
        #If at the begining of the game, process exchanges
        if self.starting_exchanges_complete_flag == False:
            #Order of exchanges should be target 8, 5, 3 for positive then negative 3, 5, 8
            low_player = max(((count < 0) * player for count,player in zip(self.starting_exchanges_remaining, [0, 1, 2])))
            self.hands[self.current_player][suit].remove(card) #Remove card from high player's hand
            self.hands[low_player][suit].append(card) #Add card to low player's hand
            self.hands[low_player][suit].sort() #Sort low player's hand
            returned_card = self.hands[low_player][suit].pop(-1) #Give the lowest card in the suit to the high player
            self.hands[self.current_player][suit].append(returned_card) #Add the returned card to the high player's hand
            self.hands[self.current_player][suit].sort() #Sort high player's hand
            #Record the exchange
            self.starting_exchanges_complete.append((self.current_player, card, low_player, returned_card))
            #Update the remaining exchanges
            self.starting_exchanges_remaining[self.current_player] -= 1
            self.starting_exchanges_remaining[low_player] += 1
            #Set the current player 
            self.current_player = max((count >= 0) * player for count,player in zip(self.starting_exchanges_remaining, [0, 1, 2]))
            #Check if exchanges are complete
            if sum([x for x in self.starting_exchanges_remaining if x > 0]) == 0:
                self.starting_exchanges_complete_flag = True
                self.current_player = 2 #Move to dealer exchange to kitty
            #Increase trick number after each exchange, so that the first trick after exchanges is trick -1
            self.trick_number += 1
            #Return
            return [0, 0, 0] #Return the change in each players score, which is 0 during exchanges
        #Set trump suit if not set
        if self.trump_suit is None:
            self.trump_suit = card // 100
            self.current_player = DEALER #Move to dealer exchange to kitty
            self.trick_number += 1 #Increase trick number after setting trump, so that the first trick after exchanges is trick -1
            return [0, 0, 0] #Return the change in each players score, which is 0 during trump selection
        #If at the dealer exchange to kitty phase, process dealer exchange
        if self.kitty_exchange_complete_flag == False:
            self.hands[DEALER][suit].remove(card) #Remove card from dealer's hand
            #Add card to kitty exchange
            self.dealer_exchanged_into_kitty.append(card)
            #Check if dealer has placed 4 cards into the kitty exchange
            if len(self.dealer_exchanged_into_kitty) == 4:
                self.dealer_removed_from_kitty = copy.deepcopy(self.kitty) #Dealer takes all (4) cards from kitty
                #Move the cards from the kitty exchange to the kitty
                self.kitty = [[] for _ in range(4)] #Reset kitty
                for exchanged_card in self.dealer_exchanged_into_kitty:
                    suit = exchanged_card // 100
                    self.kitty[suit].append(exchanged_card)
                    self.kitty[suit].sort()
                #Reset the dealer's hand to include the cards removed from the kitty
                for suit in range(4):
                    for card in self.dealer_removed_from_kitty[suit]:
                        self.hands[DEALER][suit].append(card)
                    self.hands[DEALER][suit].sort()
                #Check if any of the cards taken from the kitty by the dealer are lower than cards exchanged to other players as the low_player
                for suit in range(4):
                    for card_from_kitty in self.dealer_removed_from_kitty[suit]:
                        card_from_kitty_suit = card_from_kitty // 100
                        for high_player, _, low_player, card_given in self.starting_exchanges_complete:
                            card_given_suit = card_given // 100
                            if low_player == DEALER and card_from_kitty_suit == card_given_suit and card_from_kitty > card_given:
                                self.dealer_revealed_kitty_cards.append((high_player, card_from_kitty))
                                break #Skips further checks since the card only needs to be revealed once
                #Set the current player to the lead player for the first trick, which is the dealer (player 2)
                self.current_player = ELDEST
                #Set the flag to indicate that the kitty exchange is complete
                self.kitty_exchange_complete_flag = True
            self.trick_number += 1
            return [0, 0, 0]
        # Normal gameplay loop, assumes exchanges are already complete
        self.hands[self.current_player][suit].remove(card)
        current_trick = self.trick_history[-1]
        lead_player = self.lead_history[-1]
        current_trick.append(card)
        self.current_player = (self.current_player + 1) % 3  # Move to next player
        if len(current_trick) == 3:
            # Trick is complete, determine winner and reset trick
            lead_suit = current_trick[0] // 100
            # Determine winning card considering trump suit
            trump_cards = [c for c in current_trick if c // 100 == self.trump_suit]
            if trump_cards:
                # If trump cards were played, highest trump wins
                winning_card = max(trump_cards)
            else:
                # Otherwise, highest card in lead suit wins
                winning_card = max((c for c in current_trick if c // 100 == lead_suit), default=None)
            winning_player = (lead_player + current_trick.index(winning_card)) % 3
            self.scores[winning_player] += 1 #Increase score for winning player
            # print("Trick won by player", winning_player, "with card", winning_card)
            self.current_player = winning_player
            self.lead_history.append(winning_player)
            self.trick_history.append([])
            self.trick_number += 1
            delta_score = [0, 0, 0]
            delta_score[winning_player] = 1
            return delta_score
        return [0, 0, 0] #Return the change in each players score
    
    def is_card_better_than_current_trick(self, card):
        #Check if the given card is better than the current highest card in the trick
        current_trick = self.trick_history[-1]
        if not current_trick:
            return True  # No cards played yet
        lead_suit = current_trick[0] // 100
        trump_cards = [c for c in current_trick if c // 100 == self.trump_suit]
        if trump_cards:
            highest_trump = max(trump_cards)
            if card // 100 == self.trump_suit:
                return card > highest_trump
            else:
                return False
        else:
            highest_lead = max((c for c in current_trick if c // 100 == lead_suit), default=None)
            if card // 100 == lead_suit:
                return card > highest_lead
            else:
                return False

    def can_player_beat_card(self, player_index, card):
        #Check if the specified player can beat the given card
        suit = card // 100
        #If player has cards in the suit, check if any can beat the card
        if self.hands[player_index][suit]:
            if self.hands[player_index][suit][-1] > card:
                return True
        else:
            #Player has no cards in the suit, can play any card, check if they have trump cards
            if self.hands[player_index][self.trump_suit]:
                return True
        return False

class GameStateTextDisplay:
    #Class for abstracting how the game state is displayed as text
    #Easier to use different formatting or more advanced display strategies in the future
    def __init__(self):
        pass
    def print_game_state(self, game_state: GameState, probability_distribtion):
        print(game_state.formatted_string_2())

def is_better_score(score1, score2, player_index):
    #Compares two scores for a specific player index
    #If score1 is better than score2 for that player, return True, else False
    if score1[player_index] > score2[player_index]:
        return True
    elif score1[player_index] == score2[player_index]:
        if score1[1] > score2[1]: #Youngest player has highest prefrence
            return True
        elif score1[1] == score2[1]:
            if score1[0] > score2[0]: #Then eldest player
                return True
            elif score1[2] > score2[2]:
                return True
    return False

'''
We will create a framework of how to combine simulation and evaluation strategies to solve Sergeant Major.
'''


''' MANAGER'''

class Manager:
    #Manages the playing of a single game
    #Classifies and saves the results of simulations and evaluations
    def __init__(self):
        players = [
            RandomMoveAgent("RandomMoveAgent_A"),
            RandomMoveAgent("RandomMoveAgent_B"),
            HumanAgent("HumanAgent_C")
        ]
        self.players = players
    
    def play_match(self, seed = None):
        #TODO implement match play, for now just look at single games
        pass

    def strip_game_state_for_player(self, game_state: GameState, player_index: int) -> GameState:
        #Returns a copy of the game state with information not known to the specified player removed or obfuscated
        stripped_state = game_state.copy()
        #Remove information about exchanges; unknown cards replaced with None
        for i in range(len(stripped_state.starting_exchanges_complete)):
            high_player, card_given, low_player, card_returned = stripped_state.starting_exchanges_complete[i]
            if player_index not in [high_player, low_player]:
                stripped_state.starting_exchanges_complete[i] = (high_player, None, low_player, None)
        #Remove information about dealer exchanges with kitty; unknown cards replaced with None
        if player_index != DEALER:
            for i in range(len(stripped_state.dealer_exchanged_into_kitty)):
                stripped_state.dealer_exchanged_into_kitty[i] = None
            for i in range(len(stripped_state.dealer_removed_from_kitty)):
                for j in range(len(stripped_state.dealer_removed_from_kitty[i])):
                    stripped_state.dealer_removed_from_kitty[i][j] = None
        #Remove information about revealed kitty cards; unknown cards replaced with None
        if player_index != DEALER:
            for i in range(len(stripped_state.dealer_revealed_kitty_cards)):
                player_seeing_card, card_shown = stripped_state.dealer_revealed_kitty_cards[i]
                if player_seeing_card != player_index:
                    stripped_state.dealer_revealed_kitty_cards[i] = (player_seeing_card, None)
        #Remove information about other players hands
        for player in range(3):
            if player != player_index:
                stripped_state.hands[player] = [[] for _ in range(4)]
        #Remove information about the kitty unless the player is dealer and they have already exchanged cards with the kitty
        if player_index != DEALER or stripped_state.kitty_exchange_complete_flag == False:
            stripped_state.kitty = [[] for _ in range(4)]
        return stripped_state

    def play_game(self, eldest: int, starting_exchanges: list[int], seed = None):
        print_every_move = True
        ordered_players = [self.players[(eldest + i) % 3] for i in range(3)]
        ordered_starting_exchanges = [starting_exchanges[(eldest + i) % 3] for i in range(3)]
        print(f"Ordered players: {[player.name for player in ordered_players]}, Starting exchanges: {ordered_starting_exchanges}")
        #Set the seed if provided
        if seed is not None:
            random.seed(seed)
        #Generate a random deal for the game
        game_state = GameState(ordered_starting_exchanges)
        #Iterate through the moves of the game until
        if print_every_move: 
            print(game_state.formatted_string_2())
        while game_state.trick_number < 16:
            legal_moves = game_state.generate_legal_moves()
            current_player = game_state.current_player
            #Create a copy of the game state for the player to use, obsfucating information that they should not know
            player_game_state = self.strip_game_state_for_player(game_state, current_player)
            if print_every_move:
                print(player_game_state.formatted_string_2())
                print(f"{['Eldest', 'Middle', 'Dealer'][current_player]}: {ordered_players[current_player].name}, Legal moves: {', '.join([game_state.card_to_string(move) for move in legal_moves])}")
                # input("Press Enter to continue to the next move...")
            #Feed the known information to the player agent to choose a move
            chosen_move = ordered_players[current_player].choose_move(player_game_state, legal_moves)
            if print_every_move:
                print(f"{['Eldest', 'Middle', 'Dealer'][current_player]}: {ordered_players[current_player].name} plays {game_state.card_to_string(chosen_move)}")
            game_state.play_card(chosen_move)
        print(game_state.formatted_string_2())
            


class ScoreEvaluator:
    #Assume that a score evaluator always returns a float value, so that can be easily used by the game engine
    #Can increase this complexity later if needed
    def __init__(self, protagonist_rise: float = 100.0, three_rise: float = -8.0, five_rise: float = -9.0, eight_rise: float = -7.0, win_bonus: float = 1000.0):
        self.protagonist_rise = protagonist_rise
        self.rise = [three_rise, five_rise, eight_rise]
        self.win_bonus = win_bonus
        self.trick_goals = [3, 5, 8]
    def evaluate(self, tricks_won: list[int], protagonist_index: int) -> float:
        #Evaluate the score from the perspective of the protagonist player
        value = (tricks_won[protagonist_index] - self.trick_goals[protagonist_index]) * self.protagonist_rise
        if tricks_won[protagonist_index] >= 12: #Win condition
            value += self.win_bonus
        for i in range(3):
            if i != protagonist_index:
                value += (tricks_won[i] - self.trick_goals[i]) * self.rise[i]
                if tricks_won[i] >= 12:
                    value -= self.win_bonus #Penalty for opponents winning
        return value
    
class FullInformationEvaluator:
    #Accepts a game state with complete information and returns an evaluation score for the current player using a ScoreEvaluator
    def __init__(self, score_evaluator: ScoreEvaluator):
        self.score_evaluator = score_evaluator
    def evaluate(self, game_state: GameState) -> float:
        raise NotImplementedError("FullInformationEvaluator.evaluate() must be implemented in subclass.")

class ImmediateEvaluator(FullInformationEvaluator):
    #A simple evaluator that uses the ScoreEvaluator to evaluate the current game state
    def evaluate(self, game_state: GameState) -> float:
        return self.score_evaluator.evaluate(tricks_won=game_state.scores, protagonist_index=game_state.current_player)


'''AGENTS'''

class Agent:
    #An agent is a superclass that knows know to take in a game state (with incomplete information) from the supervisor and return a move
    def __init__(self, name: str):
        self.name = name
        #Probability that each of the 52 cards is in each location, tracked by the Agent

        self.distribution = {
            0:[]
        }

    def choose_move(self, game_state: GameState, legal_moves: list[int]) -> int:
        #We always assume that we are the current player when choosing a move
        raise NotImplementedError("Agent.choose_move() must be implemented in subclass.")

class RandomMoveAgent(Agent):
    #An agent that chooses a random legal move
    def choose_move(self, game_state: GameState, legal_moves: list[int]) -> int:
        return random.choice(legal_moves)

class HumanAgent(Agent):
    #An agent that prompts the user to choose a move
    def choose_move(self, game_state: GameState, legal_moves: list[int]) -> int:
        legal_moves_str = [game_state.card_to_string(move) for move in legal_moves]
        while True:
            user_input = input(f"{self.name}, enter a move: {', '.join(legal_moves_str)}... ")
            if user_input.upper() in legal_moves_str:
                return legal_moves[legal_moves_str.index(user_input.upper())]
            print("Invalid move, please try again.")

'''START OF TESTING'''
        
# for i in range(256):
#     print(f"\033[48;5;{i}m {i:3} \033[0m", end=" ")
#     if (i + 1) % 16 == 0:
#         print()

# manager = Manager()
# for seed in range(1001, 1400):
#     #set random seed for reproducibility
#     manager.play_game(eldest=0, starting_exchanges=[3, -1, -2], seed=seed)


import numpy as np
from scipy.special import logsumexp

import numpy as np
from scipy.special import logsumexp

def sinkhorn_log_sor_custom(A, r, c, omega=1.2, tol=1e-4, max_iter=500):
    """
    Normalizes A such that row sums = r and column sums = c.
    r: array of shape (M,)
    c: array of shape (N,)
    """
    M, N = A.shape
    C = -np.log(np.maximum(A, 1e-100))
    
    # Pre-compute log-targets
    log_r = np.log(r)
    log_c = np.log(c)
    
    # Dual variables
    f = np.zeros(M)
    g = np.zeros(N)
    
    for i in range(max_iter):
        # 1. Update Rows
        # Ideal f: log_r - log(sum(exp(g - C)))
        f_target = log_r - logsumexp(g[None, :] - C, axis=1)
        f = (1 - omega) * f + omega * f_target
        
        # 2. Update Columns
        # Ideal g: log_c - log(sum(exp(f - C)))
        g_target = log_c - logsumexp(f[:, None] - C, axis=0)
        g = (1 - omega) * g + omega * g_target
        
        # 3. Convergence check
        # Compute current row sums to check error
        log_row_sums = logsumexp(f[:, None] + g[None, :] - C, axis=1)
        error = np.linalg.norm(np.exp(log_row_sums) - r, ord=1)
        
        if error < tol:
            print(f"Converged in {i+1} iterations with error {error:.4e}")
            break
            
    return np.exp(f[:, None] + g[None, :] - C)

print(sinkhorn_log_sor_custom(np.array([[0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5]]), r=np.array([3, 1]), c=np.array([1, 1, 1, 1]), omega=1.3))