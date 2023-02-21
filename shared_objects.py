from dataclasses import dataclass


@dataclass
class RockPaperScissors:
    rock: str = "rock"
    paper: str = "paper"
    scissors: str = "scissors"

    def is_valid_choice(self, choice: str) -> bool:
        return choice in [self.rock, self.paper, self.scissors]


@dataclass
class GameResult:
    player1_choice: str
    player2_choice: str
    winner: str


@dataclass
class GameStats:
    player1_wins: int = 0
    player2_wins: int = 0
    ties: int = 0
