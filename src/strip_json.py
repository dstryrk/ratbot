import os
import argparse
import shutil
import json
import time
global user_dict
global channel_dict
    
user_dict = {}
channel_dict = {}

def strip_messages(file):
    message_list = []
    with open(file,'r') as json_data:
        messages = json.load(json_data)
    for message in messages:
        timestamp = message['timestamp']
        user = message['user']
        text = message['text']
        format_message = "{0}:{1}:{2}".format(user,timestamp,text)
        message_list.append(format_message)
    return message_list

def read_users(input_directory):
    global user_dict
    filepath = os.path.join(input_directory, 'users.json')
    with open(filepath, 'r') as json_data:
        userdict = json.load(json_data)
    for user in userdict:
        user_dict[user['id']] = user['name']    
    return user_dict

def read_channel(input_directory):
    global channel_dict
    filepath = os.path.join(input_directory, 'channels.json')
    with open(filepath,'r') as json_data:
        channellist = json.load(json_data)
    for channel in channellist:
        channel_dict[channel['id']] = channel['name']
    return channel_dict

def check_folders(folders):
    for folder in folders:
        newfolder = os.path.join(output_directory, folder)
        if not os.path.exists(newfolder):
            print "creating", newfolder
            #os.mkdir(newfolder)
def format_timestamp(ts):
    return time.strftime('%H:%M:%S', time.localtime(float(ts)))
    #return ts

def format_text(message):
    # change @levelsio has joined the channel into
	# @levelsio\n has joined #channel

    # convert change <@U38A3DE9> into levelsio
    if '<@' in message:
        #print "replacing <@"
        if '|' in message:
            token = message.split('<@')[1].split('>')[0]
            uname = message.split('<@')[1].split('>')[0].split('|')[0]
            if uname in user_dict.keys():
                handle = user_dict[uname]
                message = message.replace(token, handle)
        else:
            uname = message.split('<@')[1].split('>')[0]
            if uname in user_dict.keys():
                handle = user_dict[uname]
                message = message.replace(uname, handle)
    # change <#U38A3DE9> into #_chiang-mai
    if '<#' in message:
        if '|' in message:
            #print "replacing <#"
            token = message.split('<#')[1].split('>')[0]
            uname = message.split('<#')[1].split('>')[0].split('|')[0]
            if uname in channel_dict.keys():
                handle = channel_dict[uname]
                message = message.replace(token, handle)
        else:
            uname = message.split('<#')[1].split('>')[0]
            handle = channel_dict[uname]
            message = message.replace(uname, handle)
            
    return message

def format_message(message):
    message_type = message['type']
    if 'text' in message.keys():
        if "message" == message_type:
            if 'bot_id' in message.keys():       
                text = format_text(message['text']).encode('utf-8')
                timestamp = format_timestamp(message['ts'])
                message = 'user: {0}, ts: {1}\nmessage: {2}\n'.format(message['bot_id'],timestamp,text)
                return 'attachment',timestamp,text
            elif 'attachments' in message.keys():
                #print message
                user = user_dict[message['user']]
                text = format_text(message['text']).encode('utf-8')
                timestamp = format_timestamp(message['ts'])
                message = 'user: {0}, ts: {1}\nmessage: {2}\n'.format(user,timestamp,text)
                return user,timestamp,text
        
            elif 'user' in message.keys():
                user = user_dict[message['user']]
                text = format_text(message['text']).encode('utf-8')
                timestamp = format_timestamp(message['ts'])
                message = 'user: {0}, ts: {1}\nmessage: {2}\n'.format(user,timestamp,text)
                return user,timestamp,text
            elif 'file' in message.keys():
                text = format_text(message['text']).encode('utf-8')
                timestamp = format_timestamp(message['ts'])
                message = 'user: {0}, ts: {1}\nmessage: {2}\n'.format('file',timestamp,text)
                return 'file',timestamp,text
            else:
                print 'excepted',message
    
def extract_messagelist(filepath,channel,datestamp):
    if "channels.json" in filepath or "users.json" in filepath or "integration_logs.json" in filepath:
        return None
    with open(filepath, 'r') as json_data:
        message_list = json.load(json_data)

    bucket = []
    for message in message_list:
        user,ts,text = format_message(message)
        #print channel, ts, datestamp, user, text
        bucket.append([channel, ts, datestamp, user, text])

    return bucket

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'strips json into one csv')
    parser.add_argument('input_dir', metavar = 'input_dir',type=str,help='input diretory')

    args = parser.parse_args()
    input_directory = args.input_dir

    # create user lookup
    user_dict = read_users(input_directory)

    # create channel lookup
    channel_dict = read_channel(input_directory)
    
    #format messages
    messages = []
    for root,folders, files in os.walk(input_directory):
        for fil in files:
            datestamp = fil.replace('.json','')
            head,tail = os.path.split(root)
            channel = tail
            fpath = os.path.join(root,fil)
            
            messages_from_file = extract_messagelist(fpath,channel,datestamp)
            if messages_from_file:
                messages = messages + messages_from_file
    # create channel set
    import sets
    channel_set = set([mes[0] for mes in messages])
    user_lookup = {k:[] for k in channel_set}
    for mes in messages:
        for channel in channel_set:
            if mes[0] == channel:
                user_lookup[channel] = user_lookup[channel] + [mes[3]]
            
    for channel in channel_set:
        user_lookup[channel] = set(user_lookup[channel])
    user = 'mdimmic'
    for mes in messages:
        channel = mes[0]
        if user in user_lookup[channel]:
            print mes[0],mes[1],mes[2],mes[3],mes[4]
