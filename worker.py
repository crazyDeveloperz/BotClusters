import os
from os import path as ospath
from sys import executable
from json import loads
from asyncio import create_subprocess_exec, run, sleep as asleep, gather, create_task
from asyncio.subprocess import PIPE, Process

async def start_bot(bot_name, bot_config) -> Process:
    # Setup environment variables locally for each bot
    env = os.environ.copy()
    for env_name, env_value in bot_config['env'].items():
        env[env_name] = env_value

    bot_dir = f"/app/{bot_name}"
    bot_file = ospath.join(bot_dir, bot_config['run'])

    print(f'Starting {bot_name} bot with {bot_file}')
    process = await create_subprocess_exec(executable, bot_file, cwd=bot_dir, env=env, stdout=PIPE, stderr=PIPE)
    
    # Read stdout and stderr to log the output
    stdout, stderr = await process.communicate()
    print(f'{bot_name} stdout: {stdout.decode()}')
    print(f'{bot_name} stderr: {stderr.decode()}')
    
    return process

async def main():
    try:
        with open("config.json", "r") as jsonfile:
            bots = loads(jsonfile.read())
    except FileNotFoundError:
        print("Error: config.json file not found.")
        return
    except ValueError as e:
        print(f"Error reading config.json: {e}")
        return

    bot_name, bot_config = next(iter(bots.items()))  # Only get the first bot
    await asleep(2.5)  # Wait for 2.5 seconds before starting the bot
    bot_process = await start_bot(bot_name, bot_config)

    try:
        await bot_process.wait()  # Wait for the bot process to complete
    except Exception as e:
        print(f"Error during bot execution: {e}")

if __name__ == "__main__":
    run(main())
