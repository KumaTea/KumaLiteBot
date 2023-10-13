import os
import random
import logging
import telegram
from uuid import uuid4
import azure.functions as func
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


bot = telegram.Bot(token=os.environ["BOT_TOKEN"])

MIN_LEN = 10
MAX_LEN = 100


def insert(query):
    text = query.split()[0]
    insertion = query.split()[1]

    return insertion.join(list(text))


def repeat(text):
    if not text:
        return logging.info('repeat: blank text')

    length = len(text)

    if length <= MIN_LEN:
        result = text * random.randint(MIN_LEN-length, int(MAX_LEN/length))
    elif length <= MAX_LEN:
        result = text
        while len(result) < MAX_LEN:
            result += text
            if random.randint(0, 1):
                break
    else:
        result = '太长了禁止复读' * random.randint(1, 10)

    return result


def inline(update):
    query = update.inline_query.query
    if not query:
        return logging.info('inline: not update.inline_query.query')

    if len(query.split()) == 2 and len(query.split()[1]) <= 2:
        # insert mode
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title='发癫',
                description=f'开始发癫：{query.split()[0][:10]}...',
                input_message_content=InputTextMessageContent(insert(query)),
            ),
        ]
    else:
        # repeat
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title='复读',
                description=f'开始复读：{query[:10]}...',
                input_message_content=InputTextMessageContent(repeat(query)),
            ),
        ]
    return update.inline_query.answer(results)


def nonsense_reply():
    replies = '咋会这样呢 对对对 好家伙 说的是啊 谁不是呢 振作点儿 真过意不去 好说好说 简直难以想象 有道理 上班不忙吗 你不上班吗 你很无聊吗 最近很闲吗 我觉得也是 wow 确实 可以的 厉害了 我都行，看你 太棒了 蛮好的 不错 别见外 啊？这也太内个了吧 太过分了 咋能这样呢 这叫啥事啊 这人也真是 怎么回事 真有你的 原来是这样 我就知道 还是你厉害，我就不行 我可以理解为这是高级凡尔赛吗 怎么能这样呢 哇 嚯 害 服了 详细说说 开眼界了 好问题 会好的 笑死 真的耶 怎么啦 难搞哦 我懂 妈耶 还是要打起精神来 我也这么觉得 就是..（个人理解） 真的吗！好厉害 啊是吗？ 我也是 那也是 你知道我多想成为你吗 对对对 不愧是你 我觉得挺牛的 可不是嘛 你说的没错 看你自己 也没啥意思 生活嘛 抱抱你，太心疼了 太生气了 好惨啊 咋能这样啊 我也生气了 无语了 666 真行啊 都这样 咋欺负人呢 不难过了哦 会好起来的 硬着头皮上吧，慢慢来 为什么？ 怎么会？ 真的啊？ 我都不知道谀！ 那怎么办？ 后来呢？ 原来是这样！ 我辈楷模 有内味儿了 瑞思拜 大佬大佬 学到了 interesting nice fine good omg 那还挺好的 那就先这样 好像是有点儿 没事儿 美女的事你少管 哈哈不用啦 确实，该干嘛就干嘛'
    return random.choice(replies.split())


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="bot", auth_level=func.AuthLevel.ANONYMOUS)
def main(req):
    res = ''
    try:
        if not req.method == "POST":
            return 'I am working!'
        update = Update.de_json(req.get_json(), bot)
        if update.inline_query:
            res = inline(update)
        elif update.message:
            msg = update.message
            if msg.chat.id > 0:
                res = msg.reply_text(nonsense_reply())
        else:
            logger.info('Unknown type. Ignoring...')
    except Exception as e:
        logger.debug(str(req.get_json()))
        logger.error(str(e))
    return res if type(res) is str else ''
