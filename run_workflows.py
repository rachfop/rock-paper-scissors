import asyncio

from temporalio.client import Client

from shared_objects import RockPaperScissors

# Import the workflow from the previous code
from workflows import PlayRockPaperScissors


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")
    while True:
        # Execute a workflow
        handle = await client.start_workflow(
            PlayRockPaperScissors.run,
            id="hello-signal-workflow-id",
            task_queue="hello-signal-task-queue",
        )

        await handle.signal(
            PlayRockPaperScissors.submit_player_1_move, input("Enter your move: ")
        )
        await handle.signal(
            PlayRockPaperScissors.submit_player_2_move, input("Enter your move: ")
        )
        await handle.signal(PlayRockPaperScissors.exit)
        # Show result
        result = await handle.result()
        user_1_action = result[0]
        user_2_action = result[1]
        # print(f"\n{user_1_action}, {user_2_action}.\n")
        if user_1_action == user_2_action:
            print("Both players selected the same move, it's a tie!")
        elif user_1_action == RockPaperScissors.rock:
            if user_2_action == RockPaperScissors.scissors:
                print("Rock smashes scissors! You win!")
            else:
                print("Paper covers rock! You lose.")
        elif user_1_action == RockPaperScissors.paper:
            if user_2_action == RockPaperScissors.rock:
                print("Paper covers rock! You win! dude")
            else:
                print("Scissors cuts paper! You lose.")
        elif user_1_action == RockPaperScissors.scissors:
            if user_2_action == RockPaperScissors.paper:
                print("Scissors cuts paper! You win!")
            else:
                print("Rock smashes scissors! You lose.")
        print(f"Result: {result}")
        print(f"Stats: {await handle.query(PlayRockPaperScissors.get_game_stats)}")
        play_again = input("Play again? (y/n): ")
        if play_again.lower() != "y":
            await handle.signal(PlayRockPaperScissors.exit)
            break


if __name__ == "__main__":
    asyncio.run(main())
