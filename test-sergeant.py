#Sergeant Major Quick Check to see if solvable easily with perfect information
# 0## clubs, 1## diamonds, 2## hearts, 3## spades
# #02 2, #03 3, #10 10, #11 J, #12 Q, #13 K, #14 A

import random
import copy

# Set seed for reproducibility at program level
random.seed(23)

# Game state class
class GameState:
    def __init__(self):
        self.hands = [[[] for _ in range(4)] for _ in range(3)]  # 3 players, each with 4 suits
        self.kitty = [[] for _ in range(4)]  # Kitty with 4 suits
        self.lead_player = 0
        self.current_player = 0
        self.current_trick = []
        self.previous_trick = []
        self.previous_trick_leader = None
        self.scores = [0, 0, 0]  # Scores for each player
        self.trick_number = 0
        self.trump_suit = 0
        
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
        state = f"LP:{self.lead_player} | CP:{self.current_player} | CT:{self.current_trick} | Trump:{self.trump_suit} | "
        for i in range(3):  # 3 players
            state += f"P{i}:{str(self.hands[i])} | "
        state += f"Kitty:{self.kitty}"
        return state
    
    def copy(self):
        """Create a deep copy of the game state"""
        new_state = GameState.__new__(GameState)  # Create instance without calling __init__
        new_state.hands = copy.deepcopy(self.hands)
        new_state.kitty = copy.deepcopy(self.kitty)
        new_state.lead_player = self.lead_player
        new_state.current_player = self.current_player
        new_state.current_trick = self.current_trick.copy()
        new_state.previous_trick = self.previous_trick.copy()
        new_state.previous_trick_leader = self.previous_trick_leader
        new_state.scores = self.scores.copy()
        new_state.trick_number = self.trick_number
        new_state.trump_suit = self.trump_suit
        return new_state
    
    def __repr__(self):
        return self.serialize() + f" | Scores: {self.scores}"
    
    def formatted_string(self):
        result = f"Lead Player: {self.lead_player}, Current Player: {self.current_player}, Trump Suit: {self.trump_suit}, Kitty: {self.kitty}, Previous Trick: {self.previous_trick} led by Player {self.previous_trick_leader}\n"
        result += f"Current Trick: {self.current_trick}, "
        result += f"Scores: {self.scores}\n"
        result += f"              0{"T" if self.trump_suit == 0 else " "}            1{"T" if self.trump_suit == 1 else " "}            2{"T" if self.trump_suit == 2 else " "}            3{"T" if self.trump_suit == 3 else " "}\n"
        # result += f"Player 0: 23456789TJQKA 23456789TJQKA 23456789TJQKA 23456789TJQKA##\n"
        for player in range(3):
            result += f"    Player {player}: "
            for suit in range(4):
                for card, letter in zip(range(2, 15), "23456789TJQKA"):
                    result += letter if (100 * suit + card) in self.hands[player][suit] else "."
                result += " "
            # Add played cards, tick leader, and W for winner of trick if relevant
            if len(self.current_trick) > 0:
                reference_trick = self.current_trick
                lead_player = self.lead_player
            else:
                reference_trick = self.previous_trick
                lead_player = self.previous_trick_leader
            if self.current_player == player:
                result += " L"
            result += "\n"
        return result
    
    def generate_legal_moves(self):
        #Returns a list of legal moves for the current player
        if self.lead_player == self.current_player:
            # Lead player can play any card
            legal_moves = []
            for suit in range(4):
                legal_moves.extend(self.hands[self.current_player][suit])
            return legal_moves
        else:
            # Non-lead players must follow suit if possible
            lead_suit = self.current_trick[0] // 100
            if self.hands[self.current_player][lead_suit]:
                return self.hands[self.current_player][lead_suit]
            else:
                legal_moves = []
                for suit in range(4):
                    legal_moves.extend(self.hands[self.current_player][suit])
                return legal_moves
    
    def play_card(self, card):
        #Plays a card for the current player and updates the game state
        suit = card // 100
        self.hands[self.current_player][suit].remove(card)
        self.current_trick.append(card)
        self.current_player = (self.current_player + 1) % 3  # Move to next player
        if len(self.current_trick) == 3:
            # Trick is complete, determine winner and reset trick
            lead_suit = self.current_trick[0] // 100
            # Determine winning card considering trump suit
            trump_cards = [c for c in self.current_trick if c // 100 == self.trump_suit]
            if trump_cards:
                # If trump cards were played, highest trump wins
                winning_card = max(trump_cards)
            else:
                # Otherwise, highest card in lead suit wins
                winning_card = max((c for c in self.current_trick if c // 100 == lead_suit), default=None)
            winning_player = (self.lead_player + self.current_trick.index(winning_card)) % 3
            self.scores[winning_player] += 1 #Increase score for winning player
            # print("Trick won by player", winning_player, "with card", winning_card)
            self.previous_trick = self.current_trick.copy()
            self.previous_trick_leader = self.lead_player
            self.lead_player = winning_player
            self.current_player = winning_player
            self.current_trick = []
            self.trick_number += 1
            delta_score = [0, 0, 0]
            delta_score[winning_player] = 1
            return delta_score
        return [0, 0, 0]
    
    def is_card_better_than_current_trick(self, card):
        #Check if the given card is better than the current highest card in the trick
        if not self.current_trick:
            return True  # No cards played yet
        lead_suit = self.current_trick[0] // 100
        trump_cards = [c for c in self.current_trick if c // 100 == self.trump_suit]
        if trump_cards:
            highest_trump = max(trump_cards)
            if card // 100 == self.trump_suit:
                return card > highest_trump
            else:
                return False
        else:
            highest_lead = max((c for c in self.current_trick if c // 100 == lead_suit), default=None)
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

#Dictionary of previously evaluated game states, only stores states between tricks
# serialized : (score, best_move)
# game_state_lookup = {}

def min_max_game_state(game_state):
    #Lookup check for previously evaluated states at trick boundary
    if game_state.lead_player == game_state.current_player:
        serialized = game_state.serialize()
        if serialized in game_state_lookup:
            return game_state_lookup[serialized]
    #Alternative min-max algorithm implementation:
    legal_moves = game_state.generate_legal_moves()
    best_tail_score = [0,0,0]
    best_move = None
    for move in legal_moves:
        new_state = game_state.copy()
        delta_score = new_state.play_card(move)
        #Recursively evaluate new_state
        new_score, _ = min_max_game_state(new_state)
        #Calculate tail score
        tail_score = [new_score[i] + delta_score[i] for i in range(3)]
        if is_better_score(tail_score, best_tail_score, game_state.current_player):
            best_tail_score = tail_score
            best_move = move
    #Store in lookup if at trick boundary
    if game_state.lead_player == game_state.current_player:
        serialized = game_state.serialize()
        game_state_lookup[serialized] = (best_tail_score, best_move)
    return best_tail_score, best_move

# game_state_lookup_hypothesis_1 = {}

def min_max_game_state_hypothesis_1(game_state):
    #Lookup check for previously evaluated states at trick boundary
    if game_state.lead_player == game_state.current_player:
        serialized = game_state.serialize()
        if serialized in game_state_lookup_hypothesis_1:
            return game_state_lookup_hypothesis_1[serialized]
    #Alternative min-max algorithm implementation:
    legal_moves = game_state.generate_legal_moves()
    best_tail_score = [0,0,0]
    best_move = None
    for move_index, move in enumerate(legal_moves):
        #Check to see if the move is the lowest losging card or the lowest winning card
        suit = move // 100
        #First check if the card is the lowest in a suit
        if game_state.hands[game_state.current_player][suit][0] != move:
            #Now check if the card is the lowest winning card
            if len(game_state.current_trick) == 0: #Lead player is playing a card
                #Check if the card is winning against both opponents
                if game_state.can_player_beat_card((game_state.current_player + 1) % 3, move) or \
                        game_state.can_player_beat_card((game_state.current_player + 2) % 3, move):
                    continue #Not winning card, skip
                #Check if card is lowest winning card
                if move_index - 1 >= 0 and legal_moves[move_index - 1] // 100 == suit:
                    if (not game_state.can_player_beat_card((game_state.current_player + 1) % 3, legal_moves[move_index - 1])) and \
                            (not game_state.can_player_beat_card((game_state.current_player + 2) % 3, legal_moves[move_index - 1])):
                        continue #Not lowest winning card, skip
            elif len(game_state.current_trick) == 1: #Second player is playing a card
                #Check if the card is winning aganist the played card and the next player
                if (not game_state.is_card_better_than_current_trick(move)) or \
                        game_state.can_player_beat_card((game_state.current_player + 1) % 3, move):
                    continue #Not lowest winning card, skip
                #Check if card is lowest winning card
                if move_index - 1 >= 0 and legal_moves[move_index - 1] // 100 == suit:
                    if game_state.is_card_better_than_current_trick(legal_moves[move_index - 1]) and \
                            (not game_state.can_player_beat_card((game_state.current_player + 1) % 3, legal_moves[move_index - 1])):
                        continue #Not lowest winning card, skip
            else: #Third player is playing a card
                #Check if the card is winning against both played cards
                if (not game_state.is_card_better_than_current_trick(move)):
                    continue #Not winning card, skip
                #Check if card is lowest winning card
                if move_index - 1 >= 0 and legal_moves[move_index - 1] // 100 == suit:
                    if game_state.is_card_better_than_current_trick(legal_moves[move_index - 1]):
                        continue #Not lowest winning card, skip
        #Make a copy of the game state
        new_state = game_state.copy()
        delta_score = new_state.play_card(move)
        #Recursively evaluate new_state
        new_score, _ = min_max_game_state_hypothesis_1(new_state)
        #Calculate tail score
        tail_score = [new_score[i] + delta_score[i] for i in range(3)]
        if is_better_score(tail_score, best_tail_score, game_state.current_player):
            best_tail_score = tail_score
            best_move = move
    #Store in lookup if at trick boundary
    if game_state.lead_player == game_state.current_player:
        serialized = game_state.serialize()
        game_state_lookup_hypothesis_1[serialized] = (best_tail_score, best_move)
    return best_tail_score, best_move
    
def run_test(seed):
    random.seed(seed)
    # Clear lookup dictionaries
    global game_state_lookup
    game_state_lookup = {}  
    global game_state_lookup_hypothesis_1
    game_state_lookup_hypothesis_1 = {}
    # Create initial game state
    game_state = GameState()
    # print(game_state)
    # Play random cards
    for i in range(3*10):
        legal_moves = game_state.generate_legal_moves()
        # print("Legal moves for current player:", legal_moves)
        #choose a random legal move to play
        chosen_card = random.choice(legal_moves)
        # print("Playing card:", chosen_card)
        game_state.play_card(chosen_card)
        # print("Game state after playing a card:")
        # print(game_state)
    game_state_save = game_state.copy()
    game_state_2 = game_state.copy()
    print(game_state.formatted_string())

    while game_state.trick_number < 16:
        best_score, best_move = min_max_game_state(game_state)
        # print(f"  Player {game_state.current_player} best score from min-max evaluation: {best_score}")
        # print(f"  Player {game_state.current_player} best move from min-max evaluation: {best_move}")
        game_state.play_card(best_move)
        # print(game_state)
    while game_state_2.trick_number < 16:
        best_score, best_move = min_max_game_state_hypothesis_1(game_state_2)
        # print(f"  Player {game_state_2.current_player} best score from min-max evaluation: {best_score}")
        # print(f"  Player {game_state_2.current_player} best move from min-max evaluation: {best_move}")
        game_state_2.play_card(best_move)
        # print(game_state_2)
    # Compare final scores to see if they were the same
    if game_state.scores != game_state_2.scores:
        print(f"Discrepancy found for seed {seed}! Game state 1: {game_state.scores}, Game state 2: {game_state_2.scores}, Player {game_state_save.current_player} leads.")
        return False
    else:
        print(f"Final scores match for seed {seed}:", game_state.scores)
        return True

#71 yields an interesting case where hypothesis 1 fails: Discrepancy found for seed 71! Game state 1: [9, 6, 1], Game state 2: [10, 5, 1], Player 0 leads.
for i in range(71,71+1):
    seed = i
    run_test(seed)

'''
NOTES
What options might I play from my hand?
  - Smallest losing card
  - Highest losing card
  - Smallest winning card
  - Highest winning card (I don't think this would ever be best?)
QUESTION:
  - Is winning a trick always better than losing it? - HYPOTHESIS 1: Likely yes
Given Hypothesis 1, cards that it would make sense to play:
  - smallest losing card (suited or unsuited)
  - smallest winning card


Player 0: ............A ........T...A 2..........KA ............. 1A L W
Player 1: ............. ....67....Q.. .34.......Q.. ............. 16
Player 2: ............. ..4.......... ....67...J... ...5....T.... 14

Player 0: ............A ........T.... 2..........KA ............. 2A L W
Player 1: ............. .....7....Q.. .34.......Q.. ............. 23
Player 2: ............. ............. ....67...J... ...5....T.... 26

Player 0: ............A ........T.... 2..........K. ............. 2K L W
Player 1: ............. .....7....Q.. ..4.......Q.. ............. 24
Player 2: ............. ............. .....7...J... ...5....T.... 27

Player 0: ............A ........T.... 2............ ............. 2K L W
Player 1: ............. .....7....Q.. ..........Q.. ............. 24
Player 2: ............. ............. .........J... ...5....T.... 27
'''