class GameStats:
    def __init__(self, dd_game):
        self.settings = dd_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.health = self.settings.health
        self.score = 0
        self.level = 1

