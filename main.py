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

replyDict = {'二胖': '胖酱',
             '老牛': '🐂酱',
             '冬冬': '冬哥',
             '马晨': '晨酱',
             '程伟华': '华酱',
             '冯晓波': '波🐒',
             '杨乐': '杨总',
             '王龙': '龙🐶',
             '赵凯宁': '智障'}


@itchat.msg_register(INCOME_MSG)
def text_reply(msg):
    if 'SystemInfo' in msg.keys() and msg.SystemInfo == 'uins':
        print('选中用户置顶事件,无消息')
        return
    print(msg)
    friends = itchat.get_friends()
    fromUser = list(filter(lambda x: x.UserName ==
                           msg['FromUserName'], friends))[0]
    # if fromUser == itchat.search_friends():
    #     print('消息来自自己!')
    #     return
    if (fromUser.RemarkName in ['冬冬', '移动卡']) or (fromUser == itchat.search_friends()):
        result = jieba.cut(msg.Text, cut_all=False)
        result = "/ ".join(result)
        print("Default Mode: " + result)  # 精确模式
        words = jieba.posseg.cut(msg.Text)
        result += '\n'
        for word, flag in words:
            result += '''词语:%s
词性:%s\n''' % (word, flag)
            print('%s %s' % (word, flag))
        return result
    if fromUser.RemarkName in replyDict.keys():
        result = '''嗯?
%s今天有没有很努力呦~''' % replyDict[fromUser.RemarkName]
        print(result)
        return result


@itchat.msg_register(TEXT, isGroupChat=True)
def group_reply(msg):
    if msg.isAt:
        msg.user.send(u'@%s\u2005I received: %s' % (
            msg.actualNickName, msg.text))


def main():
    itchat.auto_login(hotReload=True, enableCmdQR=2,
                      statusStorageDir='./cache/itchat.pkl')
    # itchat.send(
    #     '老马你好', toUserName='@80b8aa7efc9ad5fa4653375cb265ad66ed63e9579f4eeeeb7c283480db300af8')
    # friends = itchat.get_friends()
    # print(friends)
    itchat.run()


if __name__ == '__main__':
    main()
