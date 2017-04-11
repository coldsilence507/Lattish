from qqbot import QQBotSlot as qqbotslot, QQBot
from tenhoubot import main as starttenhou
import threading
import re

is_playing = False
qq_group = None


class BotConnector(object):

    def __init__(self, qqbot):
        self.qbot = qqbot
        self.stop_wait = False

    def on_receive_message(self, message):
        if 'WAIT_READY' in message:
            self.qbot.SendTo(qq_group, '我排好了，你们赶紧的')
        if 'WAIT_TO_END' in message:
            self.qbot.SendTo(qq_group, '操你们妈啊，喊3缺1叫我，然后又没人来')
        if 'FINAL_RESULT' in message:
            result = re.search(r'FINAL_RESULT\s*(.*)', message).group(1)
            self.qbot.SendTo(qq_group, '刚刚跟你们这群菜鸡打了一局，结果感人')
            self.qbot.SendTo(qq_group, result)


class TenhouThread (threading.Thread):

    def __init__(self, connector):
        threading.Thread.__init__(self)
        self.connector = connector

    def run(self):
        global is_playing
        is_playing = True
        starttenhou(self.connector)
        is_playing = False

@qqbotslot
def onQQMessage(bot, contact, member, content):
    global qq_group
    global botConnector
    if contact.qq == '625219436':
        qq_group = contact
        if "Lattish" in content or "@ME" in content:
            if "缺人" in content:
                if not is_playing:
                    bot.SendTo(contact, '3缺1再叫我，谢谢，你说缺人谁他妈知道你缺几个')
                else:
                    bot.SendTo(contact, '我正在跟别人干着呢，叫也没用')
            elif "3缺1" in content or "三缺一" in content:
                if not is_playing:
                    bot.SendTo(contact, '你群打个麻将都贵阳，知道了，这就上线')
                    tenhou_thread = TenhouThread(botConnector)
                    tenhou_thread.setDaemon(True)
                    tenhou_thread.start()
                else:
                    bot.SendTo(contact, '我正在跟别人干着呢，叫也没用')
            elif "别排" in content:
                if is_playing:
                    bot.SendTo(contact, '你他妈遛我玩呢？下回缺人别JB找我')
                    botConnector.stop_wait = True
                else:
                    bot.SendTo(contact, '你他妈是不是傻，老子本来也没排啊')
            elif "地址" in content or "链接" in content:
                bot.SendTo(contact, '不会自己看群公告啊，傻逼')
                bot.SendTo(contact, '网页版：http://tenhou.net/3/?L2587')
                bot.SendTo(contact, 'Flash 版：http://tenhou.net/0/?L2587')
            elif "操大黄妈" in content:
                bot.SendTo(contact, '不操,guen')
            else:
                bot.SendTo(contact, '操你妈要求真多')


if __name__ == '__main__':
    bot = QQBot()
    botConnector = BotConnector(bot)
    bot.Login(qq='2913658983')
    bot.Run()
