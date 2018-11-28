import gamelib


class AlgoStrategy(gamelib.AlgoCore):

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
        if game_state.turn_number >= 10 and game_state.turn_number % 5 == 4:
            return
        if game_state.turn_number >= 10 and game_state.turn_number % 5 == 0:
            game_state.attempt_spawn(EMP, [3,10])
            game_state.attempt_spawn(EMP, [3,10])
            game_state.attempt_spawn(EMP, [3,10])

        if game_state.get_resource(game_state.BITS) < 10:
            return
        while game_state.get_resource(game_state.BITS) >= 1 > 0:
            game_state.attempt_spawn(PING, [14,0])

    def build_defences(self, game_state):
        for location in [[25,11],[25,12], [0,13], [1,13], [1,12], [26,12], [27,13]]:
            if game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)
        for x in range(2, 23):
            if not game_state.get_resource(game_state.CORES) > 1:
                return
            location = [x,11]
            encryptor_condition = x in [2,9,16,23]
            destructor_condition = x % 3 == 0
            if encryptor_condition and game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)
            if not encryptor_condition and destructor_condition and game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
            if not encryptor_condition and not destructor_condition and game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)


        for x in range(26,3, -1):
            if not game_state.get_resource(game_state.CORES) > 1:
                return
            location = [x,13]
            destructor_condotion = x % 2 == 0
            if destructor_condotion and game_state.can_spawn(DESTRUCTOR, location):
                game_state.attempt_spawn(DESTRUCTOR, location)
            if not destructor_condotion and game_state.can_spawn(FILTER, location):
                game_state.attempt_spawn(FILTER, location)



if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
