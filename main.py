from backuper import Backuper
from utils import create_client

import telethon.tl as tl
import re


def searchEntityByStr(client, sSearch):
    chats = client(tl.functions.messages.GetAllChatsRequest([]))
    
    r=re.compile('.*'+sSearch+'.*')
    SubGrupo = (x for x in chats.chats if r.match(x.title))
    return next(SubGrupo)
    


def main(client):
    """Main method"""
    
    """
    entity = client.get_dialogs(1)[1][0]
    backuper = Backuper(client, entity)
    #backuper.start_backup()
    backuper.start_media_backup(dl_propics=False,dl_photos=False,dl_docs=True,saveName=True)
    """
    
    entity = searchEntityByStr(client,'.*') #Search Entity
    backuper = Backuper(client, entity)
    backuper.start_backup()
    backuper.start_media_backup(dl_propics=False,dl_photos=False,dl_docs=True,saveName=True,filter=None)



if __name__ == '__main__':
    client = None
    try:
        client = create_client()
        main(client)

    finally:
        if client:
            client.disconnect()
