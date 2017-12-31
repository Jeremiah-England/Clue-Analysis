# Clue-Analysis

Goal of the Program:

To keep track of all the information given during a Clue game and combinatorically calculate the probability of each possible combination of cards being in the gamestack after making all possible inferences. 

Raw Information:

For each turn, the program collects three pieces of information:
1.	A list of three cards which I know a player does not have when he passes up showing any cards to the guesser. 
2.	A list the three cards (a tri_set) which a player has at least one of if they show a card to the guesser.
3.	If is it my turn, that a player has a particular card when he shows it to me. 

The program starts the game knowing—
-	names of all the original cards
-	the number of players
-	how many cards each player holds
-	that one of each type (weapon, room, murderer) must be in the gamestack. 

Outline of the Program and Calculations:

I created a class for Player and Game.

For the Player class, I have the following attributes which you need to know to understand the calculations:
  Possible_cards: an exhaustive list of all the cards which the player might have. 

Possible_combinations: an exhaustive list of all the possible combinations of cards which a player might have.
  Tri_sets: an exhaustive list of three card sets which we know that player must have (deduced from the player’s response to a guess.)
  Cards: the cards which I know the player has (empty in the beginning of the game).

The calculation of the probability of each possible combination being in the gamestack is as follows:
  1.	Remove the cards which a player is known to have from all the other players’ possible cards sets.
  2.	Test all the tri_sets for each player to find if only one of the possible_cards for that player is found in the tri_set. If this is so, then obviously the player must have the card.
  3.	Check if there is a card which is not found in any of the players’ possible_cards sets or in the players’ known cards. This card must be somewhere, so obviously it is in the gamestack.
  4.	For each player, remove all the combinations from the possible_combinations if the combination does not “explain” all of the tri_sets. That is, if you assume that the combination is in fact the player’s cards, is at least one of the cards found in all the tri_sets? Since we know that a player must have at least one card in each tri_set, a combination of cards that does not contain any of a tri_set’s cards is not possible for that player
  5.	Check if a card is found in all the possible_combinations; and if it is, the player must have the card.
  6.	Now that we have updated the possible_combinations using the tri_sets, there is a possibility that we removed the last combination which contained a particular card. And if all of the possible combinations are missing a particular card, then it is impossible that the player has that card. So we iterate through all the possible_cards and remove the ones which are not found in the any possible_combinations.
  7.	This next step is the big calculation which can blow up if done when each player has to many possible_combinations. How we calculated the possible combinations for each player only used information which was particular to that player. However, each player’s possible cards and combinations are not independent from all the other players’. To check that each combination for each player is actually valid, create a list possible combinations for the entire game by creating an exhaustive list of combinations of player combinations, one from each player. Then remove all of the game combinations which duplicate one of the cards. In the process, so many invalid total combinations are removed that usually some of the prior possible_combinations for a player are nowhere to be found in the total_game_combinations. I then remove these from the player’s possible_combinations. 
  8.	Since each step of the process reveals more information which could have been used to make more deductions in the previous steps, I iterate through the process several times until my output stops changing (where output is the number of possible_combinations for each player and their known cards). 
  9.	To calculate the total probability of each possible_combinations for the gamestack (I do it for each player’s possible_combinations too), I find the number of appearances of that combination in the total_combinations for the game. This number divided by the number of total_combinations_possible is the probability of the combination being in the gamestack. 

Using the program:

If you decide to use try the program out, there are several things which you should know:
  1.	Check the names of the cards on your Clue board to ensure that they are the same as elements of the lists weapons, rooms, and people.
  2.	When the script is ran, it will prompt you for everything which you need to set the game up. 
  3.	Answer the prompts for the players’ names in the order which their turns will happen.
  4.	Name your own player “you”
  5.	To do a turn where you are guessing ‘plum’, ’revovler’, and ’courtyard’; type you.turn(‘plum’, ‘revolver’, ‘courtyard’). For other players, replace ‘you’ with their name.
  6.	An instance of Game() is automatically created called ‘game.’
  7.	To run the calculations, type game.update_all(). However, this will probably not run calculation #7 above. I have a check on it which keeps it from running when the number of possible_combinations is large and I expect the calculation to blow up. This check is really low though, simply because I don’t know how predict calculate how long it will take.  If you wish to bypass the check, run game.total_combination_compiler().

Second Guesses and Improvements:

There were several points during the development and testing of the program where I realized that I had neglected to make some inference. For example, I discovered that inference #5 was missing when I was neared the end of a test game and began to make mental inferences which the computer was neglecting. So even though the inferences seem complete and exhaustive, I could be missing something somewhere. 

A more important drawback to the program is that it gives no suggestions for what to guess which would reveal the most information. The next stage of the program should include a method of Game() that finds the guesses which have the highest potential of revealing the most information. 




