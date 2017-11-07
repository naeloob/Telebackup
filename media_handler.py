from os import path, makedirs
from pathlib import Path

from telethon.tl.types import \
    User, \
    Message, MessageMediaContact, MessageMediaPhoto, MessageMediaDocument, \
    DocumentAttributeAnimated, DocumentAttributeAudio, \
    DocumentAttributeVideo, DocumentAttributeSticker, \
    DocumentAttributeFilename

from telethon.utils import get_extension


class MediaHandler:
    """Media handler which stores the tree structure for saving media.
       Can also retrieve the media file path given an entity or a message"""

    #region Initialization

    tree_structure = {
        'propics': path.join('media', 'profile_photos'),
        'photos': path.join('media', 'photos'),

        'gifs': path.join('media', 'documents', 'gifs'),
        'audios': path.join('media', 'documents', 'audios'),
        'videos': path.join('media', 'documents', 'videos'),
        'stickers': path.join('media', 'documents', 'stickers'),
        'documents': path.join('media', 'documents', 'files'),
    }

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.directories = {k: path.join(base_dir, v)
                            for k, v in MediaHandler.tree_structure.items()}

    #endregion

    #region Tree creation

    def make_tree(self):
        for d in self.directories.values():
            makedirs(d, exist_ok=True)

    #endregion

    #region Default files

    def get_default_file(self, media_type, ext='.png'):
        return path.abspath(path.join(self.directories[media_type], 'default'+ext))

    #endregion

    #region HTML file paths

    def get_html_path(self, date):
        """Retrieves the output file for the backup with the given name, in the given date.
           An example might be 'backups/exported/year/MM/dd.html'"""
        return path.abspath(path.join(self.base_dir,
                                      str(date.year),
                                      str(date.month),
                                      '{}.html'.format(date.day)))

    def get_html_uri(self, date):
        """Retrieves the output file for the given date as URI"""
        return Path(self.get_html_path(date)).as_uri()

    #endregion

    #region Profile pictures file paths

    def get_propic_path(self, entity, allow_multiple=False):
        """Gets the profile picture full path for the given entity.
           If allow_multiple is given, a more unique ID will be given to the files (photo.photo_id)
           If allow_multiple is NOT given, a more generic ID will be given to the files (entity.id)"""
        name = self.get_propic_name(entity, allow_multiple=allow_multiple)
        return path.abspath(path.join(self.directories['propics'], name)) if name else None

    def get_propic_name(self, entity, allow_multiple=False):
        """Gets the profile picture name for the given entity.
           If allow_multiple is given, a more unique ID will be given to the files (photo.photo_id)
           If allow_multiple is NOT given, a more generic ID will be given to the files (entity.id)"""
        if isinstance(entity, int):
            # Hope it is an user ID
            return '{}.jpg'.format(entity)

        if isinstance(entity, User):
            if not entity.photo:
                return None

            # TODO Perhaps a better way would be to keep all the versions,
            # and a symlink when downloading a new one
            file_id = str(entity.photo.photo_id if allow_multiple else entity.id)
            return '{}{}'.format(file_id, get_extension(entity.photo))

    #endregion

    #region Message media file paths

    def get_msg_media_path(self, msg, saveName=False):
        result = None
        if isinstance(msg.media, MessageMediaPhoto):
            media_type = 'photos'
            result = path.join(self.directories['photos'], '{}{}'
                               .format(msg.media.photo.id, get_extension(msg.media)))

        if isinstance(msg.media, MessageMediaDocument):
            media_type = None
            name = None
            for attr in msg.media.document.attributes:
                if isinstance(attr, DocumentAttributeAnimated):
                    media_type = 'gifs'
                    break
                if isinstance(attr, DocumentAttributeAudio):
                    media_type = 'audios'
                    break
                if isinstance(attr, DocumentAttributeVideo):
                    media_type = 'videos'
                    break
                if isinstance(attr, DocumentAttributeSticker):
                    media_type = 'stickers'
                    break
                if isinstance(attr, DocumentAttributeFilename):
                    media_type = 'documents'
                    #name = attr.file_name
                    break
            if not media_type:
                return None

            result = path.join(self.directories[media_type], '{}{}'
                               .format(name if saveName and name else msg.media.document.id , get_extension(msg.media)))
        if result:
            return path.abspath(result) if not saveName else path.abspath(path.join(self.directories[media_type],''))

    #endregion

    #region Message media file name

    def get_msg_media_name(self, msg, file, saveName=False):
        if isinstance(msg, Message):
            date = msg.date
            media = msg.media
        else:
            date = datetime.now()
            media = msg

        possible_names = []
        if isinstance(media, MessageMediaPhoto):
            kind = 'photo'
            extension = '.jpg'
            possible_names = None
        elif isinstance(media, MessageMediaDocument):
            kind = 'document'
            document = media.document
            extension = get_extension(media)
            for attr in document.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    possible_names.insert(0, attr.file_name)

                elif isinstance(attr, DocumentAttributeAudio):
                    possible_names.append('{} - {}'.format(
                        attr.performer, attr.title
                    ))
        elif isinstance(media, MessageMediaContact):
            first_name = media.first_name
            last_name = media.last_name
            phone_number = media.phone_number

            kind = 'contact'
            extension = '.vcard'
            possible_names = [first_name, phone_number, last_name]

        return file, kind, extension,date, possible_names
    #endregion


    """
    'propic': path.join(self.directories['propics'],
'{}.jpg'.format(self.entity.photo.photo_big.local_id))
    """
