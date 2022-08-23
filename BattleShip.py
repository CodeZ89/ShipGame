
# Description: This program contains a class that when initiated acts like the game 'BattleShip'.
#              All data members of the class are private. The class contains methods that allow two
#              players to place ships on a 10 x 10 grid. The players can place as many or as little
#              ships as they want. They do not need to take turns when placing ships. Once ships are
#              placed on the board, players take turns firing torpedoes at coordinates on the opposing
#              player's board. A torpedo can be fired at the same spot more than once. If a fired torpedo
#              is at a coordinate of an opposing player's ship, that portion of a player's ship is hit.
#              When all coordinates of a ship are hit, the ship is then sunk. When all a player's ships
#              are sunk, they lose the game.


class ShipGame:
    """Class to represent the ShipGame or BattleShip, this game is played by
    two players who take turns 'firing' torpedoes at coordinates on their opponents
    board. Player 1 always starts first."""

    def __init__(self):
        """Init method that initializes all require data members. All data
        members are private."""
        self._current_state = 'UNFINISHED'
        self._player1 = 'first'
        self._player2 = 'second'
        self._player1_ships = []
        self._player2_ships = []
        self._player1_num_ships = 0
        self._player2_num_ships = 0
        self._player_turn = self._player1
        self._last_player_turn = None

    def get_current_state(self):
        """Method that returns the current state of the game - 'UNFINISHED', 'FIRST_WON',
        or 'SECOND_WON'"""
        return self._current_state

    def get_num_ships_remaining(self, player):
        """
        Method that returns the number of ships that a player still has on their board.
        Takes one parameter:
        :param player - player to check number of ships in their a_float arsenal
        :returns num of ships that player has on the board
        """
        if player == 'first':
            return self._player1_num_ships
        else:
            return self._player2_num_ships

    def place_ship(self, player, ship_length, coordinates, ship_orientation):
        """Method that allows a player to place a ship on the board.
        Takes 4 parameters:
        :param player: player placing a ship on their board.
        :param ship_length - length of the ship they want to place,
        :param coordinates -location on board of where they would like to place the ship
        :param ship_orientation - vertical or horizontal position of ship to be placed
            on the board.
        :return True if a player places a ship in a valid location (i.e. ship is greater
        than 2 spaces long, does not intersect with an already placed ship, and is within
        the bounds of the board. Otherwise returns False."""

        if ship_orientation == 'R':
            if player == 'first':
                new_ship = []
                for i in range(ship_length):                        #create a ship with input specifications
                    new_ship.append(coordinates[0:])
                    new_coord = int(coordinates[1])
                    new_coord += 1
                    coordinates = coordinates[0] + str(new_coord)
                if self.validate_ship_placement(player, ship_length, new_ship):     #check if ship is valid
                    self._player1_ships.append(new_ship)
                    self._player1_num_ships += 1
                    return True
            elif player == 'second':
                new_ship = []
                for i in range(ship_length):
                    new_ship.append(coordinates[0:])
                    new_coord = int(coordinates[1])
                    new_coord += 1
                    coordinates = coordinates[0] + str(new_coord)
                if self.validate_ship_placement(player, ship_length, new_ship):
                    self._player2_ships.append(new_ship)
                    self._player2_num_ships += 1
                    return True
        else:
            if ship_orientation == 'C':
                if player == 'first':
                    new_ship = []
                    for i in range(ship_length):
                        new_ship.append(coordinates[0:])
                        new_coord = ord(coordinates[0])
                        new_coord += 1
                        coordinates = chr(new_coord) + coordinates[1]
                    if self.validate_ship_placement(player, ship_length, new_ship):
                        self._player1_ships.append(new_ship)
                        self._player1_num_ships += 1
                        return True
                elif player == 'second':
                    new_ship = []
                    for i in range(ship_length):
                        new_ship.append(coordinates[0:])
                        new_coord = ord(coordinates[0])
                        new_coord += 1
                        coordinates = chr(new_coord) + coordinates[1]
                    if self.validate_ship_placement(player, ship_length, new_ship):
                        self._player2_ships.append(new_ship)
                        self._player2_num_ships += 1
                        return True

    def fire_torpedo(self, player, coordinates):
        """
        Method that allows a player to fire a torpedo at their opponents board. Takes
        as parameters the player whose turn it is to fire a torpedo and the coordinates
        that they would like to fire the torpedo. If it is not the player's turn or if
        a player has already won, the method will return False. Otherwise, the method
        will record the move, check if the move has hit the opponents ship, check if a
        hit ship has been sunk, update the current game state (if the ship hit sinks
        and was the final ship to be sunk) and finally return True.
        Takes two parameters:
        :param player - current player being fired at
        :param coordinates - coordinates of fired torpedo on opposing
        player's board
        """
        if self._current_state == 'FIRST_WON' or self._current_state == 'SECOND_WON':
            return False
        if self.same_player_turn(player):               #if same player is trying to make another move
            return False
        if player == 'first':
            for i in self._player2_ships:
                for j in i:
                    if j == coordinates:
                        i.remove(j)
            for i in self._player2_ships:
                if i == []:
                    self._player2_ships.remove(i)
                    self._player2_num_ships -= 1
                if self.check_ship_count(player):
                    return False
            self.switch_turns()
            return True
        else:
            for i in self._player1_ships:
                for j in i:
                    if j == coordinates:
                        i.remove(j)
            for i in self._player1_ships:
                if i == []:
                    self._player1_ships.remove(i)
                    self._player1_num_ships -= 1
                if self.check_ship_count(player):
                    return False
            self.switch_turns()
            return True

    def validate_ship_placement(self, player, ship_length, coordinates):
        """
        Method to validate the placement of a ship by a player on the board. Will check
        to see if a ship of a particular length is able to fit on the board and does not
        cross paths with another placed ship.
        Takes three parameters:
        :param player: player attempting to place a ship
        :param ship_length: length of ship currently trying to be placed on the board
        :param coordinates: coordinates given by user to place ship on board
        :returns: True if valid move, False if move is not valid
        """
        if ship_length not in range(2, 6):                  #invalid length of ship
            return False
        if player == 'first':
            for i in coordinates:
                if int(i[1]) not in range(0,11):
                    return False
            for i in coordinates:
                if i[0] < 'A' or i[0] > 'J':
                    return False
            for i in coordinates:                           #check if a ship is already placed in that position
                for j in self._player1_ships:
                    for x in j:
                        if i in x:
                            return False
            else:
                return True
        if player == 'second':
            for i in coordinates:
                if int(i[1]) not in range(0,11):
                    return False
            for i in coordinates:
                for j in self._player2_ships:
                    for x in j:
                        if i in x:
                            return False
            else:
                return True

    def switch_turns(self):
        """
        Method that is utilized in the ShipGame class to switch turns once a player has made
        a valid move.
        Takes no parameters
        Purpose: once a player has made a valid move - switches the player's turn to the next
        player's number also set's the last_players turn data member.
        """
        if self._last_player_turn is None:                       #if it is the first turn of the game
            self._player_turn = 'first'
        if self._player_turn == 'first':
            self._player_turn = 'second'
            self._last_player_turn = 'first'
        else:
            self._player_turn = 'first'
            self._last_player_turn = 'second'


    def same_player_turn(self, player):
        """
        Method to ensure a player cannot make more than one valid move at a time.
        Checks to make sure that last player to make a move was not the same player
        as the current player trying to make a move.
        Takes one parameter:
        :param player: represents the current player trying to make a move
        :return: True if player trying to make a move the same as the last player
        to make a move. False if other player is trying to make a move.
        """
        if player == 'first' and self._last_player_turn == 'first':
            return True
        if player == 'second' and self._last_player_turn == 'second':
            return True

    def check_ship_count(self, player):
        """
        Method that checks if either player has 0 ships in their ship list. Updates
        current_state data member if either player has won.
        :param player: current player firing a torpedo
        :return: True if either player's ship count is 0. False otherwise. Updates current state
        """
        if player == 'first':
            if self._player2_num_ships == 0:
                self._current_state = 'FIRST_WON'
                return True
        else:
            if self._player1_num_ships == 0:
                self._current_state = 'SECOND_WON'
                return True




