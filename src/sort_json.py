import os
import argparse
import shutil
import json

'''
"id": "U19KTJ12P",
        "team_id": "T0H0GDCLF",
        "name": "valthalion",
        "deleted": false,
        "status": null,
        "color": "5870dd",
        "real_name": "Jeff Hiatt",
        "tz": "America\/Chicago",
        "tz_label": "Central Daylight Time",
        "tz_offset": -18000,
        "profile": {
            "first_name": "Jeff",
            "last_name": "Hiatt",
            "avatar_hash": "g6ab8459a957",
            "real_name": "Jeff Hiatt",
            "real_name_normalized": "Jeff Hiatt",
            "image_24": "https:\/\/secure.gravatar.com\/avatar\/6ab8459a957281f46295c6d77110691b.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0002-24.png",
            "image_32": "https:\/\/secure.gravatar.com\/avatar\/6ab8459a957281f46295c6d77110691b.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2F0180%2Fimg%2Favatars%2Fava_0002-32.png",
            "image_48": "https:\/\/secure.gravatar.com\/avatar\/6ab8459a957281f46295c6d77110691b.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0002-48.png",
            "image_72": "https:\/\/secure.gravatar.com\/avatar\/6ab8459a957281f46295c6d77110691b.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2F66f9%2Fimg%2Favatars%2Fava_0002-72.png",
            "image_192": "https:\/\/secure.gravatar.com\/avatar\/6ab8459a957281f46295c6d77110691b.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2F7fa9%2Fimg%2Favatars%2Fava_0002-192.png",
            "image_512": "https:\/\/secure.gravatar.com\/avatar\/6ab8459a957281f46295c6d77110691b.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2F7fa9%2Fimg%2Favatars%2Fava_0002-512.png",
            "fields": null
        },
        "is_admin": false,
        "is_owner": false,
        "is_primary_owner": false,
        "is_restricted": false,
        "is_ultra_restricted": false,
        "is_bot": false,
        "updated": 1463522559

{
        "id": "C2ZAW9R7G",
        "name": "book-club",
        "created": "1478291049",
        "creator": "U0H0HPESU",
        "is_archived": true,
        "is_general": false,
        "members": [],
        "topic": {
            "value": "",
            "creator": "",
            "last_set": "0"
        },
        "purpose": {
            "value": "An analysis of Our Kids",
            "creator": "U0H0HPESU",
            "last_set": "1478291050"
        }
    },
'''
def check_user_in_channel(user,channel):
    members = channel['members']
    user_id = user['id']
    if user_id in members:
        return True
    else:
        return False

def read_users():
    with open('../data/output/2017-01/users.json') as json_data:
        userdict= json.load(json_data)
    print "user length", len(userdict)
    return userdict

def read_channel():
    with open('../data/output/2017-01/channels.json') as json_data:
        channeldict= json.load(json_data)
    print "channel length", len(channeldict)
    return channeldict

def check_folders(folders):
    for folder in folders:
        newfolder = os.path.join(output_directory, folder)
        if not os.path.exists(newfolder):
            print "creating", newfolder
            #os.mkdir(newfolder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'splits files into temp directory')
    parser.add_argument('datemonth', metavar = 'datemonth',type=str,help='date month in YYYY-MM form')
    args = parser.parse_args()
    datestring = args.datemonth
    input_directory = '../data/Rats And Such Slack export Apr 4 2017'
    output_directory = '../data/output/{0}'.format(datestring)

    users = read_users()
    channels = read_channel()

    for user in users:
        # create user directory
        username = user['name']
        print 'creating user directory', username
        output_directory = '../data/output/{0}/{1}'.format(username, datestring)
        print input_directory
        print output_directory

        try:
            pass #shutil.copytree(input_directory,output_directory)
        except:
            pass

        for channel in channels:
            print
            print user['name'], channel['name']
            print 'checking ', os.path.join(output_directory, channel['name'])
            if not check_user_in_channel(user, channel):
                destination = os.path.join(output_directory, channel['name'])
                print "removing - not in channel", destination
                shutil.rmtree(destination)
            else:
                print "channel ok", destination

        # remove files
        for root, folders, files  in os.walk(output_directory):
            # remove files not in date range
            for file in files:
                if datestring not in file:
                    if not('channels.json' in file or 'integration_logs.json' in file or 'users.json' in file):
                        print file
                        dest = os.path.join(root, file)
                        print "removing - not w/i date range", dest
                        os.remove(dest)
                