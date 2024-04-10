# iTeachChem-discord-bot
A discord bot made to help in doubt solving in **iTeachChem** discord Server. Feel free to use the code :)

## Requirements
- discord.py==2.3.2
- Python 3.12.3

## Setup
Create your bot from the [Discord Developers Portal](https://discord.com/developers/applications) and under the Bot section, copy your Bot token and paste it in the [config.py](/config.py) file. Put other essential things in the file. 

After this, Paste the role ids and the forum channel id in the [info.py](/utils/info.py) file. 

**NOTE:** 
- Paste the correct Role IDs for the subjects.
- Make sure you have a tag named "Solved" in that forum channel. Whenever the post is closed, the bot will change the tag of that post to Solved.

### Permissions
The Bot should have all of these permissions to properly work in your server.

![image](https://github.com/Picchiiii/iTeachChem-discord-bot/assets/152993271/f220241d-fc15-4b53-b532-e8dae98d8381)

## Working of Bot
The bot checks for the given forum channel id and when a post is made in that forum channel. It sends an embed mentioning the OP of that post to choose which subject doubt ping they want to do. Users can give points to users who helped them solve that doubt.


## Commands

### User commands
- `+ping` to check ping of bot.
- `+solved @usermention` to lock and archive the forum post when the doubt is solved. Mention the user who helped you clear your doubt. This will give them a point.
- `+lb` to check the leaderboard of users.
- `+stats` to view your stats (`+stats @usermention` to view a user's stats)

### Mod only commands
- `+reopen` to open a thread if it's already closed. You need `manage threads` permissions to use this command.
- `+fsolved` to close a thread without giving anyone a point. This command is to be used during conflicts if any post has been made accidentally. This command will force solve the post and close it.
- `+fsolved @usermention` to give a user the point in case there is a problem. This will be added in their stats.
- `+sq @user <number>` to set a user's point (Admin Only). This command is used to fix points of members in the server in case of any problem.
- `+status <activity> <status>` This command is used to set the status of the bot (Bot owner only). You can have any type of status possible inside of a discord bot. "Playing", "listening", "watching" and "Custom".

## Errors
Feel free to message me on my discord 
