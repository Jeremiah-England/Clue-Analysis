from math import factorial

players = []
weapons = []
people = []
rooms = []


def nCr(n, r):
    return (factorial(n) / (factorial(r) * factorial(n - r)))


def contains(lst, item):
    for i in lst:
        if item == i:
            return True


def all_sublists_have_item(lst, item):
    number_of_sublists_to_contain = 0
    for sublist in lst:
        if contains(sublist, item):
            number_of_sublists_to_contain += 1
    if number_of_sublists_to_contain == len(lst):
        return True
    else:
        return False


def check_for_duplicates(list1, list2):
    ''' A function which analysis two lists for duplicates and outputs a list of those duplicates without deleting the duplicates in the process'''
    dups = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                dups.append(item1)
    return dups


def has_duplicates(lst):  # Assume sortibility
    lst.sort()
    for i in range(len(lst) - 1):
        if lst[i] == lst[i + 1]:
            return True


def remove_duplicates(lst):
    lst.sort()
    removed = 0
    for i in range(len(lst) - 1):
        if lst[i - removed] == lst[i + 1 - removed]:
            del lst[i - removed]
            removed += 1


def are_mutually_exclusive(list_of_lists):
    total_combination = []
    for lst in list_of_lists:
        for item in lst:
            total_combination.append(item)
    if not has_duplicates(total_combination):
        return True
    else:
        return False


def combos_of_list_elements(lst, n):
    ''' Returns a sorted exhastive list of n-size combinations of the elements of a list'''
    lst.sort()
    combos = []
    length_list = len(lst)
    if n == 0:
        pass
    elif n == 1:
        for e in lst:
            combos.append([e])
    elif n == 2:
        for e in lst:
            e_index = lst.index(e)
            for i in range(e_index + 1, length_list):
                combos.append([e, lst[i]])
    elif n == 3:
        for e in lst:
            e_index = lst.index(e)
            for i in range(e_index + 1, length_list):
                for j in range(i + 1, length_list):
                    combos.append([e, lst[i], lst[j]])
    elif n == 4:
        for e in lst:
            e_index = lst.index(e)
            for i in range(e_index + 1, length_list):
                for j in range(i + 1, length_list):
                    for k in range(j + 1, length_list):
                        combos.append([e, lst[i], lst[j], lst[k]])
    elif n == 5:
        for e in lst:
            e_index = lst.index(e)
            for i in range(e_index + 1, length_list):
                for j in range(i + 1, length_list):
                    for k in range(j + 1, length_list):
                        for m in range(k + 1, length_list):
                            combos.append([e, lst[i], lst[j], lst[k], lst[m]])
    elif n > 5:
        print("Because of the computational burden, combinations of list elements are not calculated past combinations of 5")
    print(len(combos))
    return combos


def game_board_pre():
    """This function sets up the game board with the initial values of number of players and how many cards
    each of them has using prompts and such"""
    n_players = int(input("How many players are there?"))
    global players
    global weapons
    global people
    global rooms
    for i in range(n_players):
        player = input('What is player%i\'s name?' % (i + 1))
        players.append(player)
    default_board = input('would you like to use the default number of murderes, weapons, and rooms? \n Enter "yes" or "no": ')
    if default_board == "yes":
        weapons = ['dagger', 'pipe', 'wrench', 'pistol', 'candlestick', 'rope']
        people = ['scarlet', 'white', 'mustard', 'peacock', 'plum', 'green']
        rooms = ['office', 'courtyard', 'garage', 'gameroom', 'diningroom', 'livingroom', 'bedroom', 'bathroom', 'kitchen']
    print(players)


def re_organize_list(lst, item):
    """Reorganizes a list of players such the the first player on the list is the one which is the first to check his cards."""
    new_lst_start = lst.index(item) + 1
    new_lst = lst[new_lst_start:len(lst)] + lst[0:new_lst_start]
    del new_lst[new_lst.index(item)]
    return new_lst


class Player(object):
    """This is a class for the clue player which keepds record of all the data we have on the player
    such as which cards he has guessed, which ones we know he doesn't have, and which ones we know he does have."""

    def __init__(self, name, n_cards):
        self.n_cards = n_cards
        self.name = name
        self.cards = []
        self.impossible_cards = []
        self.tri_sets = []
        self.possible_cards = weapons + people + rooms
        self.possible_combinations = []

    def has_card(self, card):
        dups = check_for_duplicates(self.cards, [card])
        if len(dups) == 0:
            self.cards.append(card)
            print(self.name, '-->', self.cards)

    def impossible_cards(self, impossible_card):
        self.impossible_cards.append(impossible_card)
        print(self.impossible_cards)

    def tri_set(self, tri_set):
        self.tri_sets.append(tri_set)
        print(self.tri_sets)

    def not_has_cards(self, card_set):
        for i in range(len(card_set)):
            self.impossible_cards.append(card_set[i])
            if contains(self.possible_cards, card_set[i]):
                self.possible_cards.remove(card_set[i])
            remove_duplicates(self.impossible_cards)

    def turn(self, murderer, weapon, room):
        turn_order = re_organize_list(players, self)
        if not(contains(people, murderer) and contains(weapons, weapon) and contains(rooms, room)):
            print('One of your card choices was not amoung the possible cards or your combinations did not include all three card types. Please check your spelling and combination, then retry the turn. ')
            return None
        while True:

            for player in turn_order:
                while True:
                    cards_or_not = input("Does %s have any of the cards? (please respond 'yes' or 'no') " % player.name)
                    if cards_or_not == 'no' or cards_or_not == 'yes':
                        break
                    else:
                        print()
                        print('????????   WARNING: you entered an invalid response. please re-enter.    ???????')
                        print()
                if cards_or_not == "yes":
                    player.tri_set([murderer, weapon, room])
                    break
                elif cards_or_not == "no":
                    player.not_has_cards([murderer, weapon, room])
                else:
                    print("Please make sure that you respond with a 'yes or a 'no'.")
            break

    def check_for_valid_player_combinations(self):
        '''Returns a list of all the valid combinations for a given player assuming access to only individual information, not group information'''
        for card in self.cards:
            if contains(self.possible_cards, card):
                self.possible_cards.remove(card)
        possible_cards = [] + self.possible_cards  # the filter_card_options function has already removed the known_cards from the possible_cards
        known_cards = [] + self.cards
        tri_sets = [] + self.tri_sets
        combs_possible_at_begining_of_the_function = [] + self.possible_combinations
        n_cards = self.n_cards
        combos_possible_cards = combos_of_list_elements(possible_cards, n_cards - len(known_cards))  # assumes that possible cards does not contian known
        print('Length of initial possible combinations for', self.name, len(combos_possible_cards))
        total_valid_combinations = []
        if n_cards == len(known_cards):
            known_cards.sort()
            total_valid_combinations = [] + [known_cards]
            print(len(total_valid_combinations), 'length of valid combos', self.name)
            print('First ten total_valid_combinations for', self.name, total_valid_combinations[:10])
        else:
            for item in known_cards:
                removed = 0
                for i in range(len(tri_sets)):
                    for card in tri_sets[i - removed]:
                        if card == item:
                            del tri_sets[i - removed]
                            removed += 1
                            break
            print(tri_sets)  # This is something in there just for the testing stage
            if len(tri_sets) == 0:
                for i in range(len(combos_possible_cards)):
                    particular_combo = []
                    for card in combos_possible_cards[i]:
                        particular_combo.append(card)
                    full_combo = known_cards + particular_combo
                    full_combo.sort()
                    total_valid_combinations.append(full_combo)
                total_valid_combinations.sort()
                print(len(total_valid_combinations), 'length of valid combos', self.name)
                print('total_valid_combinations (first 10) for', self.name, total_valid_combinations[:10])
            else:
                for combo in combos_possible_cards:
                    tri_sets_new = [] + tri_sets  # assumes that the tri_sets have been filtered and known cards taken out (OK)
                    for card1 in combo:
                        removed = 0
                        for i in range(len(tri_sets_new)):
                            for card2 in tri_sets_new[i - removed]:
                                if card2 == card1:
                                    del tri_sets_new[i - removed]
                                    removed += 1
                                    break
                    if len(tri_sets_new) == 0:
                        full_combo = known_cards + combo
                        full_combo.sort()
                        total_valid_combinations.append(full_combo)
                total_valid_combinations.sort()

                print(len(total_valid_combinations), 'length of valid combos', self.name)
                print('total_valid_combinations (first 10) for', self.name, total_valid_combinations[:10])
        if len(combs_possible_at_begining_of_the_function) > 0:
            intersection_of_original_and_calculated_combs = check_for_duplicates(combs_possible_at_begining_of_the_function, total_valid_combinations)
            total_valid_combinations = intersection_of_original_and_calculated_combs
            total_valid_combinations.sort()
        self.possible_combinations = total_valid_combinations
        return total_valid_combinations

    def check_for_missing_cards_in_possible_combinations_and_update_possible_cards(self):
        possible_combos = [] + self.possible_combinations
        possible_cards = [] + self.possible_cards
        new_possible_cards = []
        for card in possible_cards:
            for comb in possible_combos:
                if contains(comb, card):
                    new_possible_cards.append(card)
                    break
        new_possible_cards.sort()
        self.possible_cards = new_possible_cards
        print(new_possible_cards)
        # then you would update the player.possible_cards to match that
        return new_possible_cards

    def combination_denominators(self):
        '''This algorithm should come after an algorithm which throughs out the invalid possible cards which are not in the combinations,
        since it looks through the possible cards to find a denominator'''
        for card in self.possible_cards:
            if all_sublists_have_item(self.possible_combinations, card):
                self.has_card(card)


class Player_you(Player):
    def turn(self, murderer, weapon, room):
        turn_order = re_organize_list(players, self)
        if not(contains(people, murderer) and contains(weapons, weapon) and contains(rooms, room)):
            print('One of your card choices was not amoung the possible cards or your combinations did not include all three card types. Please check your spelling and combination, then retry the turn. ')
            return None
        while True:
            for player in turn_order:
                while True:
                    cards_or_not = input("Does %s have any of the cards? (please respond 'yes' or 'no') " % player.name)
                    if cards_or_not == 'no' or cards_or_not == 'yes':
                        break
                    else:
                        print('???????????      WARNING: you entered an invalid response. please re-enter.      ???????????')
                        print()
                if cards_or_not == "yes":
                    while True:
                        card = input("What is the card? ")
                        if contains(weapons + people + rooms, card):
                            player.has_card(card)
                            break
                        else:
                            print()
                            print('-----    WARNING: You entered an invalid card. Check your spelling and re-enter.   -----')
                            print()
                    break
                elif cards_or_not == "no":
                    player.not_has_cards([murderer, weapon, room])
                else:
                    print("Please make sure that you respond with a 'yes or a 'no'.")
            break


class GameStack(Player):
    def remove_invalid_combos_for_gamestack(self):
        removed = 0
        for i in range(len(self.possible_combinations)):
            if len(check_for_duplicates(self.possible_combinations[i - removed], weapons)) == 0:
                self.possible_combinations.remove(self.possible_combinations[i - removed])
                removed += 1
            elif len(check_for_duplicates(self.possible_combinations[i - removed], rooms)) == 0:
                self.possible_combinations.remove(self.possible_combinations[i - removed])
                removed += 1
            elif len(check_for_duplicates(self.possible_combinations[i - removed], people)) == 0:
                self.possible_combinations.remove(self.possible_combinations[i - removed])
                removed += 1
        return self.possible_combinations


game_board_pre()
players2 = []

for player in players:
    ''' Getting all the players initialized into their respective classes'''
    if player == 'you':
        n_cards = input("How many cards do you have? ")
        exec("%s = Player_you('%s', %s)" % (player, player, n_cards))
        exec('print(%s.name)' % (player))
        exec('players2.append(%s)' % player)
        for i in range(int(n_cards)):
            card = input("Name one of your cards without capital letters.")
            you.has_card(card)
    else:
        n_cards = input("How many cards does %s have?" % str(player))
        exec("%s = Player('%s', %s)" % (player, player, n_cards))
        exec('print(%s.name)' % (player))
        exec('players2.append(%s)' % player)

players = players2

gamestack = GameStack('gamestack', 3)


class Game(object):
    def __init__(self):
        self.players = players
        self.p_g = players + [gamestack]
        self.mutually_impossibles = []
        self.total_combinations = []

    def filter_for_impossible_cards(self):
        ''' A function which takes all the cards which some other player has out of the all the other player's possible cards list'''
        for player in self.p_g:
            players_wo_player = self.p_g[:self.p_g.index(player)] + self.p_g[self.p_g.index(player) + 1:]
            for somebody in players_wo_player:
                dups = check_for_duplicates(player.cards, somebody.possible_cards)  # somebody.possible_cards does not contain the somebody's known_cards
                for item in dups:
                    somebody.possible_cards.remove(item)
                    somebody.impossible_cards.append(item)
        for player in self.p_g:
            print('**********', player.name, '**********')
            print(player.impossible_cards)
            print(player.name, 'cards -->', player.cards)
            print(player.tri_sets)
            print(player.possible_cards)

    def print_players_cards(self):
        for player in self.p_g:
            print(player.name, '-->', player.cards)

    def print_pos_combos(self):
        for player in self.p_g:
            print(player.name, '-->', len(player.possible_combinations))

    def test_for_only_one_possible_card_in_a_tri_set(self):
        for player in self.players:
            for i in range(len(player.tri_sets)):
                dups = check_for_duplicates(player.tri_sets[i], player.possible_cards + player.cards)
                if len(dups) == 1:
                    player.has_card(''.join(dups))

    def remove_extras_from_tri_sets(self):
        for player in players:
            for i in range(len(player.tri_sets)):
                dups = check_for_duplicates(player.tri_sets[i], player.impossible_cards)
                for n in range(len(dups)):
                    player.tri_sets[i].remove(dups[n])

    def check_for_mutual_impossibility(self):
        dups = players[0].impossible_cards
        for player in players:
            dups = check_for_duplicates(player.impossible_cards, dups)
        self.mutually_impossibles = self.mutually_impossibles + dups
        for card in self.mutually_impossibles:
            gamestack.has_card(card)

    def check_all_players_possible_combos(self):
        for player in players:
            player.check_for_valid_player_combinations()
        gamestack.check_for_valid_player_combinations()
        gamestack.remove_invalid_combos_for_gamestack()

    def combination_denominators_all(self):
        for player in self.p_g:
            if len(player.possible_combinations) < 100:
                print(player.possible_combinations)
            player.combination_denominators()

    def check_all_players_possible_cards_with_respect_to_possible_combos(self):
        for player in players:
            player.check_for_missing_cards_in_possible_combinations_and_update_possible_cards()
        gamestack.check_for_missing_cards_in_possible_combinations_and_update_possible_cards()

    def probabilities(self, player):
        total_combinations = [] + self.total_combinations
        player_combinations_possible = [] + player.possible_combinations
        player_combinations = []
        player_index = self.p_g.index(player)
        for combo in total_combinations:
            player_combinations.append(combo[player_index])
        player_combinations.sort()
        for combo in player_combinations_possible:
            number_of_combos = 0
            for combo2 in player_combinations:
                if combo == combo2:
                    number_of_combos += 1
            combo.insert(0, number_of_combos)
            combo.insert(0, float(100 * number_of_combos / len(player_combinations)))
        player_combinations_possible.sort()
        player_combinations_possible[::-1]
        print(player.possible_combinations)  # testing if the functions changed the combinations within player.possible
        for item in player_combinations_possible:
            print(item)
        for prob in player.possible_combinations:
            del prob[1]
            del prob[0]

    def time_calculator_for_total_combination_compiler(self):
        multiplier = 1
        total_unknown_cards = 0
        for player in self.p_g:
            total_unknown_cards += (player.n_cards - len(player.cards))
        for player in self.p_g:
            multiplier = multiplier * nCr(total_unknown_cards, player.n_cards - len(player.cards))
            total_unknown_cards -= (player.n_cards - len(player.cards))
        return multiplier

    def total_combinations_compiler(self):
        ''' Gets all the possible total combinations from the individual possible combinations,
        and then adjusts the combinations of the individuals to contain only combos which are
        consistent with all the other players on the board and the game stack.
        The function assumse that the combinations for the gamestack which do not contain on of each card type
        (weapon, room, person) have been removed from the possible combos of the gamestack.'''
        # for i in range(len(players)):
        #     exec('player_new_combinations_%s = []' % str(i))
        # print("for testing: printing all 'player_new_combinations_' to see if they are empty lists")
        for player in self.p_g:
            print('**************** first twenty combinations ***********', player.possible_combinations[:20])
        print('I just printed all the possible_combinations for each player to make sure that they are not empty')
        gamestack_new_combinations = []
        self.total_combinations = []
        if len(players) == 6:
            for comb0 in players[0].possible_combinations:
                for comb1 in players[1].possible_combinations:
                    if are_mutually_exclusive([comb0, comb1]):
                        for comb2 in players[2].possible_combinations:
                            if are_mutually_exclusive([comb0, comb1, comb2]):
                                for comb3 in players[3].possible_combinations:
                                    if are_mutually_exclusive([comb0, comb1, comb2, comb3]):
                                        for comb4 in players[4].possible_combinations:
                                            if are_mutually_exclusive([comb0, comb1, comb2, comb3, comb4]):
                                                for comb5 in players[5].possible_combinations:
                                                    for stack in gamestack.possible_combinations:
                                                        if are_mutually_exclusive([comb0, comb1, comb2, comb3, comb4, comb5, stack]):
                                                            for i in range(len(players)):
                                                                exec('player_new_combinations_%s.append(comb%s)' % (str(i), str(i)))
                                                            gamestack_new_combinations.append(stack)
                                                            self.total_combinations.append([comb0, comb1, comb2, comb3, comb4, comb5, stack])
        elif len(players) == 5:
            for comb0 in players[0].possible_combinations:
                for comb1 in players[1].possible_combinations:
                    if are_mutually_exclusive([comb0, comb1]):
                        for comb2 in players[2].possible_combinations:
                            if are_mutually_exclusive([comb0, comb1, comb2]):
                                for comb3 in players[3].possible_combinations:
                                    if are_mutually_exclusive([comb0, comb1, comb2, comb3]):
                                        for comb4 in players[4].possible_combinations:
                                            for stack in gamestack.possible_combinations:
                                                if are_mutually_exclusive([comb0, comb1, comb2, comb3, comb4, stack]):
                                                    # for i in range(len(players)):
                                                    #     exec('player_new_combinations_%s.append(comb%s)' % (str(i), str(i)))
                                                    # gamestack_new_combinations.append(stack)
                                                    self.total_combinations.append([comb0, comb1, comb2, comb3, comb4, stack])
        elif len(players) == 4:
            for comb0 in players[0].possible_combinations:
                for comb1 in players[1].possible_combinations:
                    if are_mutually_exclusive([comb0, comb1]):
                        for comb2 in players[2].possible_combinations:
                            if are_mutually_exclusive([comb0, comb1, comb2]):
                                for comb3 in players[3].possible_combinations:
                                    for stack in gamestack.possible_combinations:
                                        if are_mutually_exclusive([comb0, comb1, comb2, comb3, stack]):
                                            for i in range(len(players)):
                                                exec('player_new_combinations_%s.append(comb%s)' % (str(i), str(i)))
                                            gamestack_new_combinations.append(stack)
                                            self.total_combinations.append([comb0, comb1, comb2, comb3, stack])
        elif len(players) == 3:
            for comb0 in players[0].possible_combinations:
                for comb1 in players[1].possible_combinations:
                    if are_mutually_exclusive([comb0, comb1]):
                        for comb2 in players[2].possible_combinations:
                            for stack in gamestack.possible_combinations:
                                if are_mutually_exclusive([comb0, comb1, comb2, stack]):
                                    for i in range(len(players)):
                                        exec('player_new_combinations_%s.append(comb%s)' % (str(i), str(i)))
                                    gamestack_new_combinations.append(stack)
                                    self.total_combinations.append([comb0, comb1, comb2, stack])
        elif len(players) == 2:
            for comb0 in players[0].possible_combinations:
                for comb1 in players[1].possible_combinations:
                    for stack in gamestack.possible_combinations:
                        if are_mutually_exclusive([comb0, comb1, stack]):
                            for i in range(len(players)):
                                exec('player_new_combinations_%s.append(comb%s)' % (str(i), str(i)))
                            gamestack_new_combinations.append(stack)
                            self.total_combinations.append([comb0, comb1, stack])
        else:
            print("Either you have a number of players above six of below two. Since that is unreasonable, I will not calculate your stuff for you.")
        # for i in range(len(players)):
        #     exec('print(len(player_new_combinations_%s), players[%s].name)' % (str(i), str(i)))
        #     exec('players[i].possible_combinations = player_new_combinations_%s' % str(i))
        # gamestack.possible_combinations = gamestack_new_combinations

        # re-making the number of possible player combinations
        for player in self.p_g:
            new_player_combinations = []
            player_index = self.p_g.index(player)
            for item in self.total_combinations:
                new_player_combinations.append(item[player_index])
            remove_duplicates(new_player_combinations)
            player.possible_combinations = new_player_combinations

        print('each time is went through the loop I printed the stack combination, hopefully that was helpful')
        print('I was just pring each player.possible_combinations to make sure that they are not empty are the function is ran')

    def skim_analysis(self):
        self.filter_for_impossible_cards()
        self.internal_eval_of_tri_sets()
        self.test_for_only_one_possible_card_in_a_tri_set()
        self.check_for_mutual_impossibility()
        self.check_all_players_possible_combos()
        self.check_all_players_possible_cards_with_respect_to_possible_combos()
        self.print_pos_combos()
        self.print_players_cards()

    def update_all(self):
        print('************************** filtering card options ********************************')
        self.filter_for_impossible_cards()
        print('******************* internal evlauations of tri_sets *****************************')
        self.test_for_only_one_possible_card_in_a_tri_set()
        print('*********************** removeing extras from tri_sets ***************************')
        self.remove_extras_from_tri_sets()
        print('************ checking for mutuall impossibility amoung the possible cards *********')
        self.check_for_mutual_impossibility()
        print('******************* checking for possible comobs in each player ********************')
        self.check_all_players_possible_combos()
        print("************* checking for universally common denominators in combinations ************")
        self.combination_denominators_all()
        self.check_all_players_possible_cards_with_respect_to_possible_combos()
        self.print_players_cards()
        self.print_pos_combos()
        if self.time_calculator_for_total_combination_compiler() < 30000:
            print('****************************** compiling possible total combinations *************************')
            self.total_combinations_compiler()
            self.combination_denominators_all()
            self.check_all_players_possible_cards_with_respect_to_possible_combos()
            self.filter_for_impossible_cards()
            self.remove_extras_from_tri_sets()
            self.test_for_only_one_possible_card_in_a_tri_set()
            self.check_for_mutual_impossibility()
            self.print_players_cards()
            self.print_pos_combos()
        #     self.total_combinations_compiler()
        #     self.check_all_players_possible_cards_with_respect_to_possible_combos()
        #     self.check_all_players_possible_combos()
        #     self.total_combinations_compiler()
        #     self.total_combinations_compiler()
        #     self.check_all_players_possible_cards_with_respect_to_possible_combos()
        # self.check_all_players_possible_combos()
        # self.total_combinations_compiler()
        # self.total_combinations_compiler()
        # self.check_all_players_possible_cards_with_respect_to_possible_combos()
        # self.check_all_players_possible_combos()
        # self.total_combinations_compiler()
        # self.total_combinations_compiler()


game = Game()
