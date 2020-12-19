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

from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram
from helper_funcs.help_Nekmo_ffmpeg import take_screen_shot, cult_small_video
from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


@pyrogram.Client.on_message(pyrogram.Filters.command(["trim"]))
async def trim(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
    TRChatBase(update.from_user.id, update.text, "trim")
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("🤭 Sorry Dude, You are **B A N N E D 🤣🤣🤣**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="**𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 𝗧𝗼 𝗠𝘆 <u>𝗖𝗵𝗮𝗻𝗻𝗲𝗹</u> 𝗕𝗲𝗹𝗼𝘄 𝗕𝗲𝗳𝗼𝗿𝗲 𝗨𝘀𝗶𝗻𝗴 𝗠𝗲 😇**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="📣 𝗖𝗟𝗜𝗖𝗞 𝗛𝗘𝗥𝗘 𝗧𝗢 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗕𝗘 📣", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
            return
    TRChatBase(update.from_user.id, update.text, "trim")
    saved_file_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
    if os.path.exists(saved_file_path):
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=update.message_id
        )
        commands = update.command
        if len(commands) == 3:
            # output should be video
            cmd, start_time, end_time = commands
            o = await cult_small_video(saved_file_path, Config.DOWNLOAD_LOCATION, start_time, end_time)
            logger.info(o)
            if o is not None:
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.UPLOAD_START,
                    message_id=a.message_id
                )
                c_time = time.time()
                await bot.send_video(
                    chat_id=update.chat.id,
                    video=o,
                    # caption=description,
                    # duration=duration,
                    # width=width,
                    # height=height,
                    supports_streaming=True,
                    # reply_markup=reply_markup,
                    # thumb=thumb_image_path,
                    reply_to_message_id=update.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        a,
                        c_time
                    )
                )
                os.remove(o)
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                    disable_web_page_preview=True,
                    message_id=a.message_id
                )
        elif len(commands) == 2:
            # output should be screenshot
            cmd, start_time = commands
            o = await take_screen_shot(saved_file_path, Config.DOWNLOAD_LOCATION, start_time)
            logger.info(o)
            if o is not None:
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.UPLOAD_START,
                    message_id=a.message_id
                )
                c_time = time.time()
                await bot.send_document(
                    chat_id=update.chat.id,
                    document=o,
                    # thumb=thumb_image_path,
                    # caption=description,
                    # reply_markup=reply_markup,
                    reply_to_message_id=update.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        a,
                        c_time
                    )
                )
                c_time = time.time()
                await bot.send_photo(
                    chat_id=update.chat.id,
                    photo=o,
                    # caption=Translation.CUSTOM_CAPTION_UL_FILE,
                    reply_to_message_id=update.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        a,
                        c_time
                    )
                )
                os.remove(o)
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                    disable_web_page_preview=True,
                    message_id=a.message_id
                )
        else:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text=Translation.FF_MPEG_RO_BOT_RE_SURRECT_ED,
                message_id=a.message_id
            )
    else:
        # reply help message
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FF_MPEG_RO_BOT_STEP_TWO_TO_ONE,
            reply_to_message_id=update.message_id
        )


@pyrogram.Client.on_message(pyrogram.Filters.command(["storageinfo"]))
async def storage_info(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
    TRChatBase(update.from_user.id, update.text, "storageinfo")
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("🤭 Sorry Dude, You are **B A N N E D 🤣🤣🤣**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="**𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 𝗧𝗼 𝗠𝘆 <u>𝗖𝗵𝗮𝗻𝗻𝗲𝗹</u> 𝗕𝗲𝗹𝗼𝘄 𝗕𝗲𝗳𝗼𝗿𝗲 𝗨𝘀𝗶𝗻𝗴 𝗠𝗲 😇**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="📣 𝗖𝗟𝗜𝗖𝗞 𝗛𝗘𝗥𝗘 𝗧𝗢 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗕𝗘 📣", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
            return
    TRChatBase(update.from_user.id, update.text, "storageinfo")
    saved_file_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
    if os.path.exists(saved_file_path):
        metadata = extractMetadata(createParser(saved_file_path))
        duration = None
        if metadata.has("duration"):
            duration = metadata.get('duration')
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FF_MPEG_RO_BOT_STOR_AGE_INFO.format(duration),
            reply_to_message_id=update.message_id
        )
    else:
        # reply help message
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FF_MPEG_RO_BOT_STEP_TWO_TO_ONE,
            reply_to_message_id=update.message_id
        )


@pyrogram.Client.on_message(pyrogram.Filters.command(["clearmedia"]))
async def clear_media(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
    TRChatBase(update.from_user.id, update.text, "clearmedia")
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("🤭 Sorry Dude, You are **B A N N E D 🤣🤣🤣**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="**𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 𝗧𝗼 𝗠𝘆 <u>𝗖𝗵𝗮𝗻𝗻𝗲𝗹</u> 𝗕𝗲𝗹𝗼𝘄 𝗕𝗲𝗳𝗼𝗿𝗲 𝗨𝘀𝗶𝗻𝗴 𝗠𝗲 😇**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="📣 𝗖𝗟𝗜𝗖𝗞 𝗛𝗘𝗥𝗘 𝗧𝗢 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗕𝗘 📣", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
            return
    TRChatBase(update.from_user.id, update.text, "clearmedia")
    saved_file_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
    if os.path.exists(saved_file_path):
        os.remove(saved_file_path)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.FF_MPEG_DEL_ETED_CUSTOM_MEDIA,
        reply_to_message_id=update.message_id
    )


@pyrogram.Client.on_message(pyrogram.Filters.command(["downloadmedia"]))
async def download_media(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
    TRChatBase(update.from_user.id, update.text, "downloadmedia")
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("🤭 Sorry Dude, You are **B A N N E D 🤣🤣🤣**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="**𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 𝗧𝗼 𝗠𝘆 <u>𝗖𝗵𝗮𝗻𝗻𝗲𝗹</u> 𝗕𝗲𝗹𝗼𝘄 𝗕𝗲𝗳𝗼𝗿𝗲 𝗨𝘀𝗶𝗻𝗴 𝗠𝗲 😇**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="📣 𝗖𝗟𝗜𝗖𝗞 𝗛𝗘𝗥𝗘 𝗧𝗢 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗕𝗘 📣", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
            return
    TRChatBase(update.from_user.id, update.text, "downloadmedia")
    saved_file_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
    if not os.path.exists(saved_file_path):
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=update.message_id
        )
        try:
            c_time = time.time()
            await bot.download_media(
                message=update.reply_to_message,
                file_name=saved_file_path,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.DOWNLOAD_START,
                    a,
                    c_time
                )
            )
        except (ValueError) as e:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text=str(e),
                message_id=a.message_id
            )
        else:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text=Translation.SAVED_RECVD_DOC_FILE,
                message_id=a.message_id
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS,
            reply_to_message_id=update.message_id
        )
