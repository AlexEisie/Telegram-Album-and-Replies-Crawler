from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputMessagesFilterPhotos
import csv
import os
#需要字节填写的部分
api_id = 123456789
api_hash = 'a1b2c3d4'
phone = '+11145141919'
#telegram客户端连接
client = TelegramClient(phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
#获取目标频道
chats = []
last_date = None
chunk_size = 200
channels = []
result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)
for chat in chats:
    try:
        if chat.broadcast == True:
            channels.append(chat)
    except:
        continue
print('Choose a group to scrape members from:')
i = 0
for c in channels:
    print(str(i) + '- ' + c.title)
    i += 1
c_index = input("Enter a Number: ")
target_channel = channels[int(c_index)]
#获取过滤内容
searchtarget= input("Enter Search Str:")

# 获取所有符合要求的消息
for message in client.iter_messages(target_channel, limit=None, search=searchtarget):
	if message.grouped_id == 0 :
        #若为单个图片
		if message.media:
			client.download_media(message,os.path.join(searchtarget,str(message.id)))
	else:
        #若为相簿
        #检查路径可用性
		if not os.path.exists(os.path.join(searchtarget,str(message.id))) :
			os.makedirs(os.path.join(searchtarget,str(message.id)))
        #获取相簿内其他图片
		offset=0
		while offset<20 :
			attachmessage=client.get_messages(target_channel,ids=(message.id+offset))
			if attachmessage == None:
                #达到频道消息末端
				break
			offset=offset+1
			if attachmessage.grouped_id :
				if attachmessage.grouped_id == message.grouped_id :
					if attachmessage.media:
                        #下载相簿内其他图片
						print("get same group message:"+str(attachmessage.id))
						client.download_media(attachmessage,os.path.join(searchtarget,str(message.id),str(attachmessage.id)))
					try:
                        #获取当前图片的回复消息
						for replymessage in client.iter_messages(target_channel, reverse=True,limit=None,reply_to=attachmessage.id) :
							if replymessage.media:
								print("get reply message:"+str(replymessage.id))
								client.download_media(replymessage,os.path.join(searchtarget,str(message.id),str(replymessage.id)))
					except:
						print("No Reply In Message:"+str(attachmessage.id))