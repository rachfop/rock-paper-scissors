import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

# Import the activity and workflow from our other files
from workflows import PlayRockPaperScissors


async def main():
    client = await Client.connect("localhost:7233")

    # Run the worker
    worker = Worker(
        client,
        task_queue="hello-signal-task-queue",
        workflows=[PlayRockPaperScissors],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
