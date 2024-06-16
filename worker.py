import os
from os import path as ospath
from sys import executable
from json import loads
from asyncio import create_subprocess_exec, run, sleep as asleep, gather, create_task
from asyncio.subprocess import DEVNULL, Process

async def start_bot(bot_name, bot_config) -> Process:
    # Setup environment variables locally for each bot
    env = os.environ.copy()
    for env_name, env_value in bot_config['env'].items():
        env[env_name] = env_value

    bot_dir = f"/app/{bot_name}"
    bot_file = ospath.join(bot_dir, bot_config['run'])

    print(f'Starting {bot_name} bot with {bot_file}')
    return await create_subprocess_exec(executable, bot_file, cwd=bot_dir, env=env, stdout=DEVNULL, stderr=DEVNULL)

async def main():
    try:
        with open("config.json", "r") as jsonfile:
            bots = loads(jsonfile.read())  # Corrected to read file content
    except FileNotFoundError:
        print("Error: config.json file not found.")
        return
    except ValueError as e:
        print(f"Error reading config.json: {e}")
        return

    bot_tasks = []
    for bot_name, bot_config in bots.items():
        await asleep(2.5)
        bot_tasks.append(create_task(start_bot(bot_name, bot_config)))

    try:
        # Wait for all bot tasks to complete
        await gather(*(task for task in bot_tasks))
    except Exception as e:
        print(f"Error during bot execution: {e}")

if __name__ == "__main__":
    run(main())
