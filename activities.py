from temporalio import activity


@activity.defn
async def post_tie() -> str:
    return "Tie game, no one wins!"


@activity.defn
async def post_player1_win() -> str:
    return "Player 1 wins!"


@activity.defn
async def post_player2_win() -> str:
    return "Player 2 wins!"


@activity.defn
async def post_invalid_choice() -> str:
    return "Invalid choice, try again!"
