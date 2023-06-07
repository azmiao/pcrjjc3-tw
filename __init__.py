from json import load, dump
from nonebot import get_bot
from hoshino import priv
from hoshino.typing import NoticeSession, MessageSegment
from .pcrclient import pcrclient, ApiException, get_headers
from asyncio import Lock
from os.path import dirname, join, exists
from copy import deepcopy
from traceback import format_exc
from .safeservice import SafeService
from .playerpref import decryptxml
from .create_img import generate_info_pic, generate_support_pic, _get_cx_name
from hoshino.util import pic2b64
import time
import requests
import os
import json

sv_help = '''
注意：数字3为服务器编号，支持1、2、3或4

关键词之间可以留空格也可以不留

[竞技场绑定 3 uid] 绑定竞技场

[竞技场查询 3 uid] 查询竞技场简要信息（绑定后无需输入3 uid）

[删除竞技场订阅] 删除竞技场排名变动推送绑定

[竞技场订阅状态] 查看绑定状态

[详细查询 3 uid] 查询账号详细信息（绑定后无需输入3 uid）

[查询群数] 查询bot所在群的数目

[查询竞技场订阅数] 查询绑定账号的总数量

[查询头像框] 查看自己设置的详细查询里的角色头像框

[更换头像框] 更换详细查询生成的头像框，默认彩色

[清空竞技场订阅] 清空所有绑定的账号(仅限主人)
'''.strip()

# 启动时的两个文件，不存在就创建
# headers文件
header_path = os.path.join(os.path.dirname(__file__), 'headers.json')
if not os.path.exists(header_path):
    default_headers = get_headers()
    with open(header_path, 'w', encoding='UTF-8') as f:
        json.dump(default_headers, f, indent=4, ensure_ascii=False)

# 头像框设置文件，默认彩色
current_dir = os.path.join(os.path.dirname(__file__), 'frame.json')
if not os.path.exists(current_dir):
    data = {
        "default_frame": "color.png",
        "customize": {}
    }
    with open(current_dir, 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

sv = SafeService('竞技场推送_tw', help_=sv_help, bundle='pcr查询')

@sv.on_fullmatch('竞技场帮助', only_to_me=False)
async def send_jjchelp(bot, ev):
    await bot.send(ev, f'{sv_help}')

@sv.on_fullmatch('查询群数', only_to_me=False)
async def group_num(bot, ev):
    self_ids = bot._wsr_api_clients.keys()
    for sid in self_ids:
        gl = await bot.get_group_list(self_id=sid)
        msg = f"本Bot目前正在为【{len(gl)}】个群服务"
    await bot.send(ev, f'{msg}')

# 读取绑定配置
curpath = dirname(__file__)
config = join(curpath, 'binds.json')
root = {
    'arena_bind' : {}
}
if exists(config):
    with open(config) as fp:
        root = load(fp)
binds = root['arena_bind']

# 读取代理配置
with open(join(curpath, 'account.json')) as fp:
    pinfo = load(fp)

# 一些变量初始化
cache = {}
client = None

# 设置异步锁保证线程安全
lck = Lock()
captcha_lck = Lock()
qlck = Lock()

# 查询配置文件是否存在
def judge_file(cx):
    cx_path = os.path.join(os.path.dirname(__file__), f'{cx}cx_tw.sonet.princessconnect.v2.playerprefs.xml')
    if os.path.exists(cx_path):
        return True
    else:
        return False

# 获取配置文件
def get_client():
    acinfo_1cx = decryptxml(join(curpath, '1cx_tw.sonet.princessconnect.v2.playerprefs.xml')) if judge_file(1) else {'admin': ''}
    client_1cx = pcrclient(acinfo_1cx['UDID'], acinfo_1cx['SHORT_UDID'], acinfo_1cx['VIEWER_ID'],
        acinfo_1cx['TW_SERVER_ID'], pinfo['proxy']) if judge_file(1) else None
    acinfo_2cx = decryptxml(join(curpath, '2cx_tw.sonet.princessconnect.v2.playerprefs.xml')) if judge_file(2) else {'admin': ''}
    client_2cx = pcrclient(acinfo_2cx['UDID'], acinfo_2cx['SHORT_UDID'], acinfo_2cx['VIEWER_ID'],
        acinfo_2cx['TW_SERVER_ID'], pinfo['proxy']) if judge_file(2) else None
    acinfo_3cx = decryptxml(join(curpath, '3cx_tw.sonet.princessconnect.v2.playerprefs.xml')) if judge_file(3) else {'admin': ''}
    client_3cx = pcrclient(acinfo_3cx['UDID'], acinfo_3cx['SHORT_UDID'], acinfo_3cx['VIEWER_ID'],
        acinfo_3cx['TW_SERVER_ID'], pinfo['proxy']) if judge_file(3) else None
    acinfo_4cx = decryptxml(join(curpath, '4cx_tw.sonet.princessconnect.v2.playerprefs.xml')) if judge_file(4) else {'admin': ''}
    client_4cx = pcrclient(acinfo_4cx['UDID'], acinfo_4cx['SHORT_UDID'], acinfo_4cx['VIEWER_ID'],
        acinfo_4cx['TW_SERVER_ID'], pinfo['proxy']) if judge_file(4) else None
    return client_1cx, client_2cx, client_3cx, client_4cx, acinfo_1cx, acinfo_2cx, acinfo_3cx, acinfo_4cx

async def query(cx:str, id: str):
    client_1cx, client_2cx, client_3cx, client_4cx, _, _, _, _ = get_client()
    if cx == '1': client = client_1cx
    elif cx == '2': client = client_2cx
    elif cx == '3': client = client_3cx
    else: client = client_4cx
    if client == None:
        return 'lack shareprefs'
    async with qlck:
        while client.shouldLogin:
            await client.login()
        res = (await client.callapi('/profile/get_profile', {
                'target_viewer_id': int(id)
            }))
        return res

def save_binds():
    with open(config, 'w') as fp:
        dump(root, fp, indent=4)

@sv.on_fullmatch('查询竞技场订阅数', only_to_me=False)
async def pcrjjc_number(bot, ev):
    global binds, lck

    async with lck:
        await bot.send(ev, f'当前竞技场已订阅的账号数量为【{len(binds)}】个')

@sv.on_fullmatch('清空竞技场订阅', only_to_me=False)
async def pcrjjc_del(bot, ev):
    global binds, lck

    async with lck:
        if not priv.check_priv(ev, priv.SUPERUSER):
            await bot.send(ev, '抱歉，您的权限不足，只有bot主人才能进行该操作！')
            return
        else:
            num = len(binds)
            binds.clear()
            save_binds()
            await bot.send(ev, f'已清空全部【{num}】个已订阅账号！')

@sv.on_rex(r'^竞技场绑定\s*(\d)\s*(\d{9})$') # 支持匹配空格，空格可有可无且长度无限制
async def on_arena_bind(bot, ev):
    global binds, lck

    if ev['match'].group(1) != '1' and ev['match'].group(1) != '2' and \
        ev['match'].group(1) != '3' and ev['match'].group(1) != '4':
        await bot.send(ev, '服务器选择错误！支持的服务器有1/2/3/4')
        return
    async with lck:
        uid = str(ev['user_id'])
        last = binds[uid] if uid in binds else None
        cx = ev['match'].group(1)
        binds[uid] = {
            'cx': cx,
            'id': ev['match'].group(2),
            'uid': uid,
            'gid': str(ev['group_id']),
            'arena_on': last is None or last['arena_on'],
            'grand_arena_on': last is None or last['grand_arena_on'],
        }
        save_binds()
        is_file = judge_file(cx)
        msg = '竞技场绑定成功'
        msg += f'\n注：本bot未识别到台服{cx}服配置文件，因此查询该服的玩家信息功能不可用，请联系维护组解决' if not is_file else ''

    await bot.finish(ev, msg, at_sender=True)

@sv.on_rex(r'^竞技场查询\s*(\d)?\s*(\d{9})?$')
async def on_query_arena(bot, ev):
    global binds, lck

    robj = ev['match']
    cx = robj.group(1)
    id = robj.group(2)
    cx_name = _get_cx_name(cx)

    async with lck:
        if id == None and cx == None:
            uid = str(ev['user_id'])
            if not uid in binds:
                await bot.finish(ev, '您还未绑定竞技场', at_sender=True)
                return
            else:
                id = binds[uid]['id']
                cx = binds[uid]['cx']
                cx_name = _get_cx_name(cx)
        try:
            res = await query(cx, id)
            
            if res == 'lack shareprefs':
                await bot.finish(ev, f'查询出错，缺少该服的配置文件', at_sender=True)
                return
            last_login_time = int (res['user_info']['last_login_time'])
            last_login_date = time.localtime(last_login_time)
            last_login_str = time.strftime('%Y-%m-%d %H:%M:%S',last_login_date)
            
            await bot.send(ev, 
f'''区服：{cx_name}
昵称：{res['user_info']["user_name"]}
jjc排名：{res['user_info']["arena_rank"]}
pjjc排名：{res['user_info']["grand_arena_rank"]}
最后登录：{last_login_str}''', at_sender=False)
        except ApiException as e:
            await bot.finish(ev, f'查询出错，{e}', at_sender=True)
        except requests.exceptions.ProxyError:
            await bot.finish(ev, f'查询出错，连接代理失败，请再次尝试', at_sender=True)
        except Exception as e:
            await bot.finish(ev, f'查询出错，{e}', at_sender=True)

@sv.on_rex(r'^详细查询\s*(\d)?\s*(\d{9})?$')
async def on_query_arena_all(bot, ev):
    global binds, lck

    robj = ev['match']
    cx = robj.group(1)
    id = robj.group(2)
    uid = str(ev['user_id'])

    async with lck:
        if id == None and cx == None:
            if not uid in binds:
                await bot.finish(ev, '您还未绑定竞技场', at_sender=True)
                return
            else:
                id = binds[uid]['id']
                cx = binds[uid]['cx']
        try:
            res = await query(cx, id)
            if res == 'lack shareprefs':
                await bot.finish(ev, f'查询出错，缺少该服的配置文件', at_sender=True)
                return
            sv.logger.info('开始生成竞技场查询图片...') # 通过log显示信息
            result_image = await generate_info_pic(res, cx, uid)
            result_image = pic2b64(result_image) # 转base64发送，不用将图片存本地
            result_image = MessageSegment.image(result_image)
            result_support = await generate_support_pic(res, uid)
            result_support = pic2b64(result_support) # 转base64发送，不用将图片存本地
            result_support = MessageSegment.image(result_support)
            sv.logger.info('竞技场查询图片已准备完毕！')
            try:
                await bot.finish(ev, f"\n{str(result_image)}\n{result_support}", at_sender=True)
            except Exception as e:
                sv.logger.info("do nothing")
        except ApiException as e:
            await bot.finish(ev, f'查询出错，{e}', at_sender=True)
        except requests.exceptions.ProxyError:
            await bot.finish(ev, f'查询出错，连接代理失败，请再次尝试', at_sender=True)
        except Exception as e:
            await bot.finish(ev, f'查询出错，{e}', at_sender=True)

# @on_command('/pcrval')
async def validate(session):
    global binds, lck, validate
    _, _, _, _, acinfo_1cx, acinfo_2cx, acinfo_3cx, acinfo_4cx = get_client()
    if session.ctx['user_id'] == acinfo_1cx['admin'] or session.ctx['user_id'] == acinfo_2cx['admin'] \
        or session.ctx['user_id'] == acinfo_3cx['admin'] or session.ctx['user_id'] == acinfo_4cx['admin']:
        validate = session.ctx['message'].extract_plain_text().strip()[8:]
        captcha_lck.release()

@sv.on_prefix('删除竞技场订阅')
async def delete_arena_sub(bot,ev):
    global binds, lck

    uid = str(ev['user_id'])

    if ev.message[0].type == 'at':
        if not priv.check_priv(ev, priv.SUPERUSER):
            await bot.finish(ev, '删除他人订阅请联系维护', at_sender=True)
            return
        uid = str(ev.message[0].data['qq'])
    elif len(ev.message) == 1 and ev.message[0].type == 'text' and not ev.message[0].data['text']:
        uid = str(ev['user_id'])


    if not uid in binds:
        await bot.finish(ev, '未绑定竞技场', at_sender=True)
        return

    async with lck:
        binds.pop(uid)
        save_binds()

    await bot.finish(ev, '删除竞技场订阅成功', at_sender=True)

@sv.on_fullmatch('竞技场订阅状态')
async def send_arena_sub_status(bot,ev):
    global binds, lck
    uid = str(ev['user_id'])

    
    if not uid in binds:
        await bot.send(ev,'您还未绑定竞技场', at_sender=True)
    else:
        info = binds[uid]
        await bot.finish(ev,
    f'''
    当前竞技场绑定ID：{info['id']}
    竞技场订阅：{'开启' if info['arena_on'] else '关闭'}
    公主竞技场订阅：{'开启' if info['grand_arena_on'] else '关闭'}''',at_sender=True)

@sv.on_notice('group_decrease.leave')
async def leave_notice(session: NoticeSession):
    global lck, binds
    uid = str(session.ctx['user_id'])
    gid = str(session.ctx['group_id'])
    bot = get_bot()
    if uid not in binds:
        return
    async with lck:
        bind_cache = deepcopy(binds)
        info = bind_cache[uid]
        if info['gid'] == gid:
            binds.pop(uid)
            save_binds()
            await bot.send_group_msg(
                group_id = int(info['gid']),
                message = f'{uid}退群了，已自动删除其绑定在本群的竞技场订阅推送'
            )

@sv.on_prefix(('竞技场换头像框', '更换竞技场头像框', '更换头像框'))
async def change_frame(bot, ev):
    user_id = ev.user_id
    frame_tmp = ev.message.extract_plain_text()
    path = os.path.join(os.path.dirname(__file__), 'img/frame/')
    frame_list = os.listdir(path)
    if not frame_list:
        await bot.finish(ev, 'img/frame/路径下没有任何头像框，请联系维护组检查目录')
    if frame_tmp not in frame_list:
        msg = f'文件名输入错误，命令样例：\n竞技场换头像框 color.png\n目前可选文件有：\n' + '\n'.join(frame_list)
        await bot.finish(ev, msg)
    data = {str(user_id): frame_tmp}
    current_dir = os.path.join(os.path.dirname(__file__), 'frame.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        f_data = json.load(f)
    f_data['customize'] = data
    with open(current_dir, 'w', encoding='UTF-8') as rf:
        json.dump(f_data, rf, indent=4, ensure_ascii=False)
    await bot.send(ev, f'已成功选择头像框:{frame_tmp}')
    frame_path = os.path.join(os.path.dirname(__file__), f'img/frame/{frame_tmp}')
    msg = MessageSegment.image(f'file:///{os.path.abspath(frame_path)}')
    await bot.send(ev, msg)

# see_a_see（
@sv.on_fullmatch(('查竞技场头像框', '查询竞技场头像框', '查询头像框'))
async def see_a_see_frame(bot, ev):
    user_id = str(ev.user_id)
    current_dir = os.path.join(os.path.dirname(__file__), 'frame.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        f_data = json.load(f)
    id_list = list(f_data['customize'].keys())
    if user_id not in id_list:
        frame_tmp = f_data['default_frame']
    else:
        frame_tmp = f_data['customize'][user_id]
    path = os.path.join(os.path.dirname(__file__), f'img/frame/{frame_tmp}')
    msg = MessageSegment.image(f'file:///{os.path.abspath(path)}')
    await bot.send(ev, msg)

# 每隔6小时更新一次版本号
@sv.scheduled_job('interval', hour='6')
async def update_ver():
    header_path = os.path.join(os.path.dirname(__file__), 'headers.json')
    default_headers = get_headers()
    with open(header_path, 'w', encoding='UTF-8') as f:
        json.dump(default_headers, f, indent=4, ensure_ascii=False)
    sv.logger.info(f'pcr-jjc3-tw的游戏版本已更新至最新')
