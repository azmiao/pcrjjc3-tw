from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

class CreateImg:
    def __init__(self,w,h,img_w=0,img_h=0,color='white',image_type='RGBA',background='',text=''):
        self.w = int(w)
        self.h = int(h)
        self.img_w = int(img_w)
        self.img_h = int(img_h)
        self.current_w = 0
        self.current_h = 0
        if not background:
            self.markImg = Image.new(image_type, (self.w, self.h), color)
        else:
            if w == 0 and h == 0:
                self.markImg = Image.open(background)
                w, h = self.markImg.size
            else:
                self.markImg = Image.open(background).resize((self.w, self.h), Image.ANTIALIAS)
        self.draw = ImageDraw.Draw(self.markImg)
        if text:
            path_to_ttf = 'simhei.ttf'
            font = ImageFont.truetype(path_to_ttf, size=20)
            self.draw.text(xy=(20,20),text=text, font=font, fill='#000000')
        self.size = self.w, self.h

    # 贴图
    def paste(self, img, pos=None, alpha=False):
        if isinstance(img, CreateImg):
            img = img.markImg
        if self.current_w == self.w:
            self.current_w = 0
            self.current_h += self.img_h
        if not pos:
            pos = (self.current_w, self.current_h)
        if alpha:
            try:
                self.markImg.paste(img, pos, img)
            except ValueError:
                img = img.convert("RGBA")
                self.markImg.paste(img, pos, img)
        else:
            self.markImg.paste(img, pos)
        self.current_w += self.img_w
        return self.markImg

    # 转bs4:
    def pic2bs4(self):
        buf = BytesIO()
        self.markImg.save(buf, format='PNG')
        base64_str = base64.b64encode(buf.getvalue()).decode()
        return base64_str

async def generate_img(img_data) -> str:
    # 空角色的头像
    blank_img = img_data['blank']
    img_b = CreateImg(100, 100, background=blank_img)
    # 修补用的白色格子
    img_repair = CreateImg(100, 100, color='white')
    # 创建四条画布
    card_head = CreateImg(500, 100, 250, 100)
    card_img_0 = CreateImg(500, 100, 100, 100)
    card_body = CreateImg(500, 100, 250, 100)
    card_img_1 = CreateImg(500, 100, 100, 100)

    # 第一排01：最爱的角色
    try:
        c_favorite_name = list(img_data['f'].keys())[0]
        c_favorite_img = img_data['f'][c_favorite_name]
        head_f = CreateImg(250, 100, color='white',text=f'最爱的角色：\n\n{c_favorite_name}')
        img_f = CreateImg(100, 100, background = c_favorite_img)
    except:
        head_f = CreateImg(250, 100, color='white',text=f'最爱的角色：\n\n(无)')
        img_f = img_b
    # 第一排02：好友支援角色
    try:
        c_friend_support1_name = list(img_data['fr1'].keys())[0]
        c_friend_support1_img = img_data['fr1'][c_friend_support1_name]
        text_fr1 = c_friend_support1_name
        img_fr1 = CreateImg(100, 100, background = c_friend_support1_img)
    except:
        text_fr1 = '无'
        img_fr1 = img_b
    try:
        c_friend_support2_name = list(img_data['fr2'].keys())[0]
        c_friend_support2_img = img_data['fr2'][c_friend_support2_name]
        text_fr2 = c_friend_support2_name
        img_fr2 = CreateImg(100, 100, background = c_friend_support2_img)
    except:
        text_fr2 = '无'
        img_fr2 = img_b
    # 第一排填充
    card_head.paste(head_f)
    head_fr = CreateImg(250, 100, color='white',text=f'好友支援角色：\n{text_fr1}\n{text_fr2}')
    card_head.paste(head_fr)
    # 最爱头像
    card_img_0.paste(img_f)
    # 修补两格
    card_img_0.paste(img_repair)
    card_img_0.paste(img_repair)
    # 好友支援头像
    card_img_0.paste(img_fr1)
    card_img_0.paste(img_fr2)

    # 第二排01：地下城支援角色
    try:
        c_clan_support1_name = list(img_data['cl1'].keys())[0]
        c_clan_support1_img = img_data['cl1'][c_clan_support1_name]
        text_cl1 = c_clan_support1_name
        img_cl1 = CreateImg(100, 100, background = c_clan_support1_img)
    except:
        text_cl1 = '无'
        img_cl1 = img_b
    try:
        c_clan_support2_name = list(img_data['cl2'].keys())[0]
        c_clan_support2_img = img_data['cl2'][c_clan_support2_name]
        text_cl2 = c_clan_support2_name
        img_cl2 = CreateImg(100, 100, background = c_clan_support2_img)
    except:
        text_cl2 = '无'
        img_cl2 = img_b
    # 第二排02：战队支援角色
    try:
        c_clan_support3_name = list(img_data['cl3'].keys())[0]
        c_clan_support3_img = img_data['cl3'][c_clan_support3_name]
        text_cl3 = c_clan_support3_name
        img_cl3 = CreateImg(100, 100, background = c_clan_support3_img)
    except:
        text_cl3 = '无'
        img_cl3 = img_b
    try:
        c_clan_support4_name = list(img_data['cl4'].keys())[0]
        c_clan_support4_img = img_data['cl4'][c_clan_support4_name]
        text_cl4 = c_clan_support4_name
        img_cl4 = CreateImg(100, 100, background = c_clan_support4_img)
    except:
        text_cl4 = '无'
        img_cl4 = img_b
    # 第二排填充
    body_cl12 = CreateImg(250, 100, color='white',text=f'地下城支援角色：\n{text_cl1}\n{text_cl2}')
    card_body.paste(body_cl12)
    # 修补两格
    body_cl34 = CreateImg(250, 100, color='white',text=f'战队支援角色：\n{text_cl3}\n{text_cl4}')
    card_body.paste(body_cl34)
    # 地下城支援头像
    card_img_1.paste(img_cl1)
    card_img_1.paste(img_cl2)
    # 修补一格
    card_img_1.paste(img_repair)
    # 战队支援头像
    card_img_1.paste(img_cl3)
    card_img_1.paste(img_cl4)

    # 创建整个画布
    A = CreateImg(500, 400, 500, 100)
    A.paste(card_head)
    A.paste(card_img_0)
    A.paste(card_body)
    A.paste(card_img_1)
    return A.pic2bs4()