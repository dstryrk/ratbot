# RATBOT

## To create a user backup file

1. Export the backup file, unzip and place it in /data

2. Run the sorter in /src
e.g.
`python strip_json.py username ../data/Rats\ And\ Such\ Slack\ export\ Apr\ 30\ 2017 > USERNAME.txt`

This will output only channels user is active in.

To do: 
3. Run the send_digest.py for automatic emailing
`python send_digest.py`

## One time paid backup
slack_history.py is to pull down the whole logs, including private channels to disk.
This will not work when using the free version.
