import gamelib


class AlgoStrategy(gamelib.AlgoCore):

    def __init__(self):
        super().__init__()

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
        while game_state.get_resource(game_state.BITS) > 0:
            game_state.attempt_spawn(PING, [13, 0])

    def build_defences(self, game_state):
        main_destructors = [[4, 12], [5, 12], [22, 12], [23, 12]]
        main_filters = [[3, 12], [4, 13], [5, 13], [22, 13], [24, 12], [23, 13]]
        main_encryptors = [[23, 11], [4, 11], [22, 10], [5, 10], [21, 9], [6, 9]]

        secondary_destructors = [[6, 12], [21, 12], [5, 11], [22, 11], [6, 11], [21, 11], [7, 11], [20, 11]] + \
                                [[8, 11], [19, 11], [9, 11], [18, 11], [10, 11], [17, 11]]
        secondary_filters = [[7, 12], [8, 12], [21, 13], [19, 12], [20, 12], [6, 13]] + \
                            [[8, 12], [19, 12], [9, 12], [18, 12], [10, 12], [17, 12]]

        self.build_by_locationlist(game_state, DESTRUCTOR, main_destructors)
        self.build_by_locationlist(game_state, FILTER, main_filters)
        self.build_by_locationlist(game_state, ENCRYPTOR, main_encryptors)
        self.build_by_locationlist(game_state, DESTRUCTOR, secondary_destructors)
        self.build_by_locationlist(game_state, FILTER, secondary_filters)

    def build_by_locationlist(self, game_state, piece_type, locations):
        for location in locations:
            if game_state.can_spawn(piece_type, location):
                game_state.attempt_spawn(piece_type, location)


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
