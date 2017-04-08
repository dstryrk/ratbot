# RATBOT

1. Export the new file and place it in /data

2. Run the sorter in /src
`python sort_json.py YYYY-MM`

This will sort the log output by user and strip out all messages except the year and month

3. Place slack2json.php in the directory to convert and run 
`php slack2json.php` which will create an html log

4. Run the send_digest.py
`python send_digest.py`

Notes: slack_history.py is to pull down the whole logs, including private channels to disk.
This will not work when using the free version.
