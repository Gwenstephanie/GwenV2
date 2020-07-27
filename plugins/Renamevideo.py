#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import Client, Filters

from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image


@pyrogram.Client.on_message(pyrogram.Filters.command(["rename"]))
async def rename_doc(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    TRChatBase(update.from_user.id, update.text, "rename")
    if (" " in update.text) and (update.reply_to_message is not None):
        cmd, file_name = update.text.split(" ", 1)
        if len(file_name) > 64:
            await update.reply_text(
                Translation.IFLONG_FILE_NAME.format(
                    alimit="64",
                    num=len(file_name)
                )
            )
            return
        description = Translation.CUSTOM_CAPTION_UL_FILE
        download_location = Config.DOWNLOAD_LOCATION + "/"
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_START,
                a,
                c_time
            )
        )
        if the_real_download_location is not None:
            try:
                await bot.edit_message_text(
                    text=Translation.SAVED_RECVD_DOC_FILE,
                    chat_id=update.chat.id,
                    message_id=a.message_id
                )
            except:
                pass
            new_file_name = download_location + file_name
            os.rename(the_real_download_location, new_file_name)
            await bot.edit_message_text(
                text=Translation.UPLOAD_START,
                chat_id=update.chat.id,
                message_id=a.message_id
                )
            if local_file_name.upper().endswith(("MKV", "MP4", "WEBM")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            #
            width = 0
            height = 0
            thumb_image_path = None
            if os.path.exists(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            else:
                thumb_image_path = await take_screen_shot(
                    local_file_name,
                    os.path.dirname(os.path.abspath(local_file_name)),
                    (duration / 2)
                )
                # get the correct width, height, and duration for videos greater than 10MB
                if os.path.exists(thumb_image_path):
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    # resize image
                    # ref: https://t.me/PyrogramChat/44663
                    # https://stackoverflow.com/a/21669827/4723940
                    Image.open(thumb_image_path).convert(
                        "RGB"
                    ).save(thumb_image_path)
                    img = Image.open(thumb_image_path)
                    # https://stackoverflow.com/a/37631799/4723940
                    img.resize((320, height))
                    img.save(thumb_image_path, "JPEG")
                    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            #
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            # send video
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaVideo(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        width=width,
                        height=height,
                        duration=duration,
                        supports_streaming=True
                    )
                    # quote=True,
                )
            else:
                sent_message = await message.reply_video(
                    video=local_file_name,
                    # quote=True,
                    caption=caption_str,
                    parse_mode="html",
                    duration=duration,
                    width=width,
                    height=height,
                    thumb=thumb,
                    supports_streaming=True,
                    disable_notification=True,
                    # reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                )
            if thumb is not None:
                os.remove(thumb)
        elif local_file_name.upper().endswith(("MP3", "M4A", "M4B", "FLAC", "WAV")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            title = ""
            artist = ""
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("title"):
                title = metadata.get("title")
            if metadata.has("artist"):
                artist = metadata.get("artist")
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            # send audio
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaAudio(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        duration=duration,
                        performer=artist,
                        title=title
                    )
                    # quote=True,
                )
            else:
                sent_message = await message.reply_audio(
                    audio=local_file_name,
                    # quote=True,
                    caption=caption_str,
                    parse_mode="html",
                    duration=duration,
                    performer=artist,
                    title=title,
                    thumb=thumb,
                    disable_notification=True,
                    # reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                )
            if thumb is not None:
                os.remove(thumb)
        else:
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            # if a file, don't upload "thumb"
            # this "diff" is a major derp -_- 😔😭😭
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            #
            # send document
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaDocument(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html"
                    )
                    # quote=True,
                )
            else:
                sent_message = await message.reply_document(
                    document=local_file_name,
                    # quote=True,
                    thumb=thumb,
                    caption=caption_str,
                    parse_mode="html",
                    disable_notification=True,
                    # reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                )
            try:
                os.remove(new_file_name)
            except:
                pass
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                chat_id=update.chat.id,
                message_id=a.message_id,
                disable_web_page_preview=True
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.REPLY_TO_DOC_FOR_RENAME_FILE,
            reply_to_message_id=update.message_id
        )
