from itchat.content import *
import itchat

import jieba.posseg as pseg
import jieba
# @itchat.msg_register(itchat.content.TEXT)
# def text_reply(msg):
#     result = '已收到:%s' % msg.text
#     print(result)
#     return result
# pseg.POSTokenizer()
from datetime import datetime

m_print = print


def func_print(*argvs, **kwargvs):
    # if(len(argvs) > 0):
    #     now = datetime.strftime(datetime.now(), '%Y-%M-%D %H:%m:%S')
    #     temp = tuple(now) + argvs
    time = '[%s] ' % datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    m_print(time, end='')
    m_print(*argvs, **kwargvs)


print = func_print

# global requestUser, replyDict
requestUser = None
replyDict = {'二胖': '胖酱',
             '郑凯': '胖酱',
             '老牛': '🐂酱',
             #  '冬冬': '冬哥',
             '马晨': '晨酱',
             "李浩": "浩酱",
             "清白之年": "浩酱",
             '程伟华': '华酱',
             #  '冯晓波': '波🐒',
             '杨乐': '杨总',
             '王龙': '龙🐶',
             '赵凯宁': '🐶宁'}


controller = True


@itchat.msg_register(TEXT)
def text_reply(msg):
    global replyDict, requestUser, controller
    if 'SystemInfo' in msg.keys() and msg.SystemInfo == 'uins':
        print('选中用户置顶事件,无消息')
        return
    message = '''好友消息:
@[%s]\u2005I received: %s''' % (msg.User.NickName,  msg.Text)
    print(message)
    # print(msg)
    friends = itchat.get_friends()
    fromUser = list(filter(lambda x: x.UserName ==
                           msg['FromUserName'], friends))[0]
    if fromUser == itchat.search_friends():
        # print('消息来自自己!')
        if(msg.Text == 'on'):
            controller = True
            print(controller)
        elif msg.Text == 'off':
            controller = False
            print(controller)
        return
    # or (fromUser == itchat.search_friends()):
    if(fromUser.NickName != 'Sayonara'):
        ask_xiaobing(msg.Text, fromUser)
    if(fromUser.RemarkName in replyDict.keys()) or (fromUser.NickName in replyDict.keys()):
        requestUser = fromUser
        ask_xiaobing(msg.Text, fromUser)
    if (fromUser.RemarkName in ['冬冬1', '移动卡']):
        word = cut(msg.Text)
        fromUser.send(word)
    # if fromUser.RemarkName in replyDict.keys():
    #     encourage(fromUser)
    #     replyDict.pop(fromUser.RemarkName)


def encourage(user):
    word = '''嗯?
%s 今天有没有很努力呦~''' % replyDict[user.RemarkName]
    print(word)
    # return result
    user.send(word)


def cut(text):
    word = jieba.cut(text, cut_all=False)
    word = "/ ".join(word)
    print("Default Mode: " + word)  # 精确模式
    words = jieba.posseg.cut(text)
    word += '\n'
    for word, flag in words:
        word += '''词语:%s
词性:%s\n''' % (word, flag)
        print('%s %s' % (word, flag))
    return word


@itchat.msg_register(INCOME_MSG, isMpChat=True)
def mp_reply(msg):
    print(msg)
    message = u'''公众号消息:
@[%s]\u2005I received: %s''' % (msg.NickName, msg.Content)
    print(message)
    if msg.isAt:
        msg.User.send(message)


@itchat.msg_register(INCOME_MSG, isGroupChat=True)
def group_reply(msg):
    # print(msg)
    message = u'''群消息[%s]:
@[%s]\u2005I received: %s''' % (msg.User.NickName, msg.ActualNickName, msg.Content)
    print(message)
    if msg.isAt:
        # msg.User.send(message)
        text = msg.Content.split('\u2005')[1:]
        print('text:%s'%text)
        if len(text)>0:
            ask_xiaobing(text, msg.User)
        else:
            msg.User.send('干啥?')


def ask_xiaobing(text=None, user=None):
    global requestUser, controller
    if controller is False:
        return
    if user is None:
        return
    requestUser = user
    xiaoBing = filter(lambda x: x.NickName == '小冰',
                      itchat.get_mps()).__next__()
    xiaoBing.send(text)


@itchat.msg_register(INCOME_MSG, isMpChat=True)
def request_from_xiaobing(msg):
    global requestUser
    # print(msg)
    if msg.User.NickName == '小冰' and requestUser is not None:
        requestUser.send(msg.Content)
        userName = requestUser.RemarkName
        if len(requestUser.RemarkName) == 0:
            userName = requestUser.NickName
        message = '''[小冰] 自动回复:
[@%s]:%s
''' % (userName, msg.Content)
        print(message)
        requestUser = None


# @itchat.msg_register(TEXT, isGroupChat=True)
def main():
    itchat.auto_login(hotReload=True, enableCmdQR=0,
                      statusStorageDir='./cache/itchat_y1l.pkl')
    # itchat.send(
    #     '老马你好', toUserName='@80b8aa7efc9ad5fa4653375cb265ad66ed63e9579f4eeeeb7c283480db300af8')
    # friends = itchat.get_friends()
    # print(friends)
    ask_xiaobing()
    itchat.run()


if __name__ == '__main__':
    main()
