from .. import loader, utils
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import time


def register(cb):
    cb(SpamBanMod())
    
class SpamBanMod(loader.Module):
    """this module check have u spamban or no by @SpamBot"""
    strings = {'name': 'SpamBanChecker'}

    async def spmbcmd(self, message):
        """usage: .spmb"""
        chat = "@SpamBot"
        text = "/start"
        reply = await message.get_reply_message()
        if not text and not reply:
            await message.edit("<b></b>")
            return
        await message.edit("<b>Wait...</b>")
        async with message.client.conversation(chat) as conv:
            if text:
                try:
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=178220800))
                    await message.client.send_message(chat, text)
                    response = await response
                except YouBlockedUserError:
                    await message.edit("<b>unblock @SpamBot!</b>")
                    return
            else:
                try:
                    user = await utils.get_user(reply)
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=178220800))
                    await message.client.send_message(chat, f"{reply.raw_text} (с) {user.first_name}")
                    response = await response
                except YouBlockedUserError:
                    await message.edit("<b>unblock @SpamBot!</b>")
                    return
        if response.text:
            await message.client.send_message(message.to_id, f"<b> {response.text}</b>")
            await message.delete()
        if response.media:
            await message.client.send_file(message.to_id, response.media, reply_to=reply.id if reply else None)
            await message.delete()