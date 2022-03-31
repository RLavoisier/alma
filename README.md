# Technical test for Alma

## How to use

This app has been made using Python 3.8.9

First install the pip requirements :

`pip install -r requirements.txt`

Then simply launch the game with :

`python main.py`

## How it works

The game is using asyncio to generate the different ressources simultaneously.

The creation process is encapsulated in a work session (that you can launch in the game menu) of the duration of your choice.

I'm using a time tic to synchronise every worker, this allows the works that are not finished at the end of a worksession
to be continued in the next worksession (No ressource lost)

## Game settings

You can change the following game settings in game_settings.py:

`TARGET_NB_ROBOTS` : Change the number of robots needed to win the game (default: 30)

`DEFAULT_JOB_CHANGE_DURATION`: Change the time needed for a robot to change its job (default: 10)

`DEFAULT_ROBOT_MONEY_COST`: The cost in money to buy a new robot (default: 3)

`DEFAULT_ROBOT_FOO_COST`: The cost in Foo to buy a new robot (default: 6)

`DEFAULT_SELL_FOOBAR_DURATION`: The time needed to sell Foobars

`DEFAULT_ASSEMBLE_FOOBAR_DURATION`: The time needed to assemble Foobars

# Good luck