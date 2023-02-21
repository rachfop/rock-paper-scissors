import asyncio
from typing import List

from temporalio import workflow

from shared_objects import GameResult, GameStats, RockPaperScissors


@workflow.defn
class PlayRockPaperScissors:
    def __init__(self) -> None:
        self._player1_choice: asyncio.Queue[str] = asyncio.Queue()
        self._player2_choice: asyncio.Queue[str] = asyncio.Queue()
        self._game_results: List[GameResult] = []
        self._game_stats: GameStats = GameStats()
        self._rps: RockPaperScissors = RockPaperScissors()
        self._exit = False

    @workflow.run
    async def run(self) -> List[str]:
        move: List[str] = []

        while True:
            await workflow.wait_condition(
                lambda: not self._player1_choice.empty() or self._exit
            )
            await workflow.wait_condition(
                lambda: not self._player2_choice.empty() or self._exit
            )

            # Drain and process queue
            while not self._player1_choice.empty() and not self._player2_choice.empty():
                move.append(f"{self._player1_choice.get_nowait()}")
                move.append(f"{self._player2_choice.get_nowait()}")

            game_result = GameResult(
                player1_choice=move[0],
                player2_choice=move[1],
                winner="",
            )

            if game_result.player1_choice == game_result.player2_choice:
                self._game_stats.ties += 1
                game_result.winner = "tie"

            elif (
                (
                    game_result.player1_choice == RockPaperScissors().rock
                    and game_result.player2_choice == RockPaperScissors().scissors
                )
                or (
                    game_result.player1_choice == RockPaperScissors().paper
                    and game_result.player2_choice == RockPaperScissors().rock
                )
                or (
                    game_result.player1_choice == RockPaperScissors().scissors
                    and game_result.player2_choice == RockPaperScissors().paper
                )
            ):

                self._game_stats.player1_wins += 1
                game_result.winner = "player 1"
            else:
                self._game_stats.player2_wins += 1
                game_result.winner = "player 2"

            self._game_results.append(game_result)
            if self._exit:
                return move

    @workflow.signal
    async def submit_player_1_move(self, name: str) -> None:
        await self._player1_choice.put(name)

    @workflow.signal
    async def submit_player_2_move(self, name: str) -> None:
        await self._player2_choice.put(name)

    @workflow.query
    async def get_game_stats(self):
        return self._game_stats

    @workflow.signal
    async def send_not_active(self):
        self._game_stats.active = False

    @workflow.signal
    def exit(self) -> None:
        self._exit = True
