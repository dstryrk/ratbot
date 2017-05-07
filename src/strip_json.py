import os
import argparse
import shutil
import json
import time
user_dict = {}

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

    
def check_user_in_channel(user,channel):
    print user
    print channel_dict
    print channel_dict.keys()
    print 'channel', channel_dict['members']
    inv_map = {v: k for k, v in user_dict.iteritems()}
    members = channeldict['members']
    user_id = inv_map[user] #user['id']

    if user_id in members:
        return True
    else:
        return False

def read_users(input_directory):
    global user_dict
    filepath = os.path.join(input_directory, 'users.json')
    #print filepath
    with open(filepath, 'r') as json_data:
        userdict= json.load(json_data)
    #print "user length", len(userdict)
    for user in userdict:
        user_dict[user['id']] = user['name']
    
    return user_dict
'''
def read_channel(input_directory):
    global channeldict
    filepath = os.path.join(input_directory, 'channels.json')
    print filepath
    with open(filepath,'r') as json_data:
        channeldict= json.load(json_data)
    return channeldict
'''
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
        try:
            uname = message.split('<@')[1].split('>')[0].split('|')[0]
            handle = user_dict[uname]
            message = message.replace(uname, handle)
        except:
            pass

    # change <#U38A3DE9> into #_chiang-mai
    if '<#U' in message:
        #print "replacing <#"
        uname = message.split('<#')[1].split('>')[0]
        #uname = message.split('<#')[1].split('>')[0].split('|')[0]
        handle = user_dict[uname]
        message = message.replace(uname, handle)
        #handle = "#_" + user_dict[uname]
        #token = '<#' + uname + '>'
        message = message.replace(uname, handle)
    return message

def format_usercode(usercode):
    return user_dict(usercode)


def format_message(message):
    message_type = message['type']
    #print 
    #print "message type:", message_type
    #print "message keys:", message.keys()
    #print "message\n",message
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

def extract_messages(message_list):
    bucket = []
    for message in message_list:
        user,ts,text = format_message(message)
        #print channel, ts, datestamp, user, text
        bucket.append([channel, ts, datestamp, user, text])

def extract_messagelist(filepath,channel,datestamp):
    if "channels.json" in filepath or "users.json" in filepath or "integration_logs.json" in filepath:
        return
    with open(filepath, 'r') as json_data:
        message_list = json.load(json_data)
    return message_list



if __name__ == "__main__":
    global user_dict
    global channel_dict
    parser = argparse.ArgumentParser(description = 'strips json into one csv')
    parser.add_argument('input_dir', metavar = 'input_dir',type=str,help='input diretory')

    args = parser.parse_args()
    input_directory = args.input_dir

    output_file = '../data/output/{0}.output.csv'


    # create user lookup
    user_dict = read_users(input_directory)
    
    # create channel lookup
    messages = []
    for root,folders, files in os.walk(input_directory):
        for fil in files:
            datestamp = fil.replace('.json','')
            head,tail = os.path.split(root)
            channel = tail
            fpath = os.path.join(root,fil)
            
            message_list = extract_messagelist(fpath,channel,datestamp)
            if message_list:
                m = extract_messages(message_list)
                print m
                print fpath
                messages = messages + m
    
    print messages[0]