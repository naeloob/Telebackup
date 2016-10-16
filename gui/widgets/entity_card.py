import tkinter as tk

from PIL import ImageTk, Image
from telethon.utils import get_display_name

from utils import get_cached_client, sanitize_string


class EntityCard(tk.Frame):
    """Improved entry with support for validation, delete and paste.
       As optional arguments, it can take:
         field max_length = integer
         function on_change(entry_contents)
         function paste_filter(clipboard_contents) returns string
    """
    def __init__(self, master=None, **kwargs):

        # Set the custom attributes and pop'em out
        self.entity = kwargs.pop('entity')

        # Initialize the frame
        super().__init__(master, **kwargs)

        self.config(borderwidth=2, relief='ridge')

        # Set up our custom widget
        self.profile_picture = tk.Label(self)
        self.profile_picture.grid(row=0, column=0, sticky=tk.NSEW)

        self.right_column = tk.Frame(self)
        self.right_column.grid(row=0, column=1)

        self.name_label = tk.Label(self.right_column,
                                   text=sanitize_string(get_display_name(self.entity)))
        self.name_label.grid(row=0)

        if hasattr(self.entity, 'username'):
            self.username_label = tk.Label(self.right_column,
                                           text='@{}'.format(self.entity.username))
            self.username_label.grid(row=1)

        if hasattr(self.entity, 'phone'):
            self.phone_label = tk.Label(self.right_column,
                                        text='+{}'.format(self.entity.phone))
            self.phone_label.grid(row=2)

        elif hasattr(self.entity, 'participants_count'):
            self.participants_label = tk.Label(self.right_column,
                                               text='{} participants'.format(self.entity.participants_count))
            self.participants_label.grid(row=2)

        self.msg_count_label = tk.Label(self.right_column,
                                        text='??? messages')
        self.msg_count_label.grid(row=3)

    def update_profile_photo(self, photo_file):
        """Updates the profile photo"""
        self.profile_picture_photo = ImageTk.PhotoImage(
            Image.open(photo_file).resize((64, 64), Image.ANTIALIAS))

        self.profile_picture.config(image=self.profile_picture_photo)

    def update_msg_count(self, count):
        """Updates the message count"""
        self.msg_count_label.config(text='{} messages'.format(count))
