import gamelib
import random
import math
import warnings
from sys import maxsize


class AlgoStrategy(gamelib.AlgoCore):

    BULLET_PATH = [[3, 13], [4, 13], [4, 12], [5, 12], [5, 11], [6, 11], [6, 10], [7, 10], [7, 9], [8, 9], [8, 8],
                   [9, 8], [9, 7], [10, 7], [10, 6], [11, 6], [11, 5], [12, 5], [12, 4], [13, 4], [13, 3],
                   [14, 3], [14, 2], [15, 2], [15, 1]]

    DEFENDERS_POSITIONS = [[0, 13], [1, 13], [2, 13], [5, 13], [6, 13], [7, 13], [8, 13], [9, 13], [10, 13], [11, 13],
                           [12, 13], [13, 13], [14, 13], [15, 13], [16, 13], [17, 13], [18, 13], [19, 13], [20, 13],
                           [21, 13], [22, 13], [23, 13], [24, 13], [25, 13], [26, 13], [27, 13], [1, 12], [2, 12],
                           [3, 12], [6, 12], [7, 12], [8, 12], [9, 12], [10, 12], [11, 12], [12, 12], [13, 12],
                           [14, 12], [15, 12], [16, 12], [17, 12], [18, 12], [19, 12], [20, 12], [21, 12], [22, 12],
                           [23, 12], [24, 12], [25, 12], [26, 12], [2, 11], [3, 11], [4, 11], [7, 11], [8, 11], [9, 11],
                           [10, 11], [11, 11], [12, 11], [13, 11], [14, 11], [15, 11], [16, 11], [17, 11], [18, 11],
                           [19, 11], [20, 11], [21, 11], [22, 11], [23, 11], [24, 11], [25, 11], [3, 10], [4, 10],
                           [5, 10], [8, 10], [9, 10], [10, 10], [11, 10], [12, 10], [13, 10], [14, 10], [15, 10],
                           [16, 10], [17, 10], [18, 10], [19, 10], [20, 10], [21, 10], [22, 10], [23, 10], [24, 10],
                           [4, 9], [5, 9], [6, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9], [14, 9], [15, 9],
                           [16, 9], [17, 9], [18, 9], [19, 9], [20, 9], [21, 9], [22, 9], [23, 9], [5, 8], [6, 8],
                           [7, 8], [10, 8], [11, 8], [12, 8], [13, 8], [14, 8], [15, 8], [16, 8], [17, 8], [18, 8],
                           [19, 8], [20, 8], [21, 8], [22, 8], [6, 7], [7, 7], [8, 7], [11, 7], [12, 7], [13, 7],
                           [14, 7], [15, 7], [16, 7], [17, 7], [18, 7], [19, 7], [20, 7], [21, 7], [7, 6], [8, 6],
                           [9, 6], [12, 6], [13, 6], [14, 6], [15, 6], [16, 6], [17, 6], [18, 6], [19, 6], [20, 6],
                           [8, 5], [9, 5], [10, 5], [13, 5], [14, 5], [15, 5], [16, 5], [17, 5], [18, 5], [19, 5],
                           [9, 4], [10, 4], [11, 4], [14, 4], [15, 4], [16, 4], [17, 4], [18, 4], [10, 3], [11, 3],
                           [12, 3], [15, 3], [16, 3], [17, 3], [11, 2], [12, 2], [13, 2], [16, 2], [12, 1], [13, 1],
                           [14, 1], [13, 0], [14, 0]]

    GUN_DULO = [15,1]

    ECRYPTOR_POSITIONS = [[ 5, 10],[ 8, 10],[ 6, 9],[ 9, 9]]

    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]

    def on_turn(self, turn_state):

        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        # game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()

    def starter_strategy(self, game_state):
        self.build_defences(game_state)
        self.deploy_attackers(game_state)


    def deploy_attackers(self, game_state):
        if game_state.get_resource(game_state.BITS) < 10:
            return
        while game_state.get_resource(game_state.BITS) >= 1 > 0:
            game_state.attempt_spawn(PING, self.GUN_DULO)

    def build_defences(self, game_state):
        for location in self.ECRYPTOR_POSITIONS:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)
        for location in self.DEFENDERS_POSITIONS:
            if not game_state.get_resource(game_state.CORES) > 1:
                return
            x,y = location
            if x % 2 == 0:
                #filter
                if game_state.can_spawn(FILTER, location):
                    game_state.attempt_spawn(FILTER, location)
            else:
                #detructor
                if game_state.can_spawn(DESTRUCTOR, location):
                    game_state.attempt_spawn(DESTRUCTOR, location)


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
