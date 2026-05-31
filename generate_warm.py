#!/usr/bin/env python3
"""
小红书招聘图文生成器 - 暖色手绘风格
特点：奶油色背景 + 暖色调 + emoji装饰 + 活泼排版
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class XHSWarmGenerator:
    """暖色手绘风格生成器"""
    
    # 暖色调配色
    COLORS = {
        'bg': (253, 248, 243),           # 奶油白 #FDF8F3
        'card_bg': (255, 255, 255),      # 卡片白
        'text_dark': (45, 45, 45),       # 深色文字
        'text_medium': (107, 91, 79),    # 中等棕 #6B5B4F
        'text_light': (155, 139, 122),   # 浅棕 #9B8B7A
        'accent_cream': (232, 213, 196), # 奶茶色 #E8D5C4
        'accent_pink': (212, 165, 165),  # 豆沙粉 #D4A5A5
        'accent_blue': (143, 180, 201),  # 雾霾蓝 #8FB4C9
        'accent_green': (152, 200, 167), # 薄荷绿 #98C8A7
        'border': (232, 213, 196, 128),  # 边框色
    }
    
    # emoji映射
    EMOJI_MAP = {
        '教师': '🏫',
        '医疗': '🏥',
        '国企': '💼',
        '医院': '💊',
        '政府': '👔',
        '学校': '📚',
        '集团': '🏭',
        'default': '📋'
    }
    
    def __init__(self, width=1080, height=1440):
        self.width = width
        self.height = height
        self.font_path = self._find_font()
        
    def _find_font(self):
        """查找中文字体"""
        font_paths = [
            '/home/yan/.local/share/fonts/msyh.ttc',
            '/home/yan/.local/share/fonts/simhei.ttf',
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
        return None
    
    def _get_font(self, size):
        """获取字体"""
        if self.font_path:
            try:
                return ImageFont.truetype(self.font_path, size)
            except:
                pass
        return ImageFont.load_default()
    
    def _get_emoji(self, job_name):
        """根据岗位名称获取对应emoji"""
        for key, emoji in self.EMOJI_MAP.items():
            if key in job_name:
                return emoji
        return self.EMOJI_MAP['default']
    
    def _draw_rounded_rect(self, draw, xy, radius, fill=None, outline=None, width=1):
        """绘制圆角矩形"""
        x1, y1, x2, y2 = xy
        if fill:
            draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
            draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
            draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
            draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
            draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
            draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)
        if outline:
            draw.rounded_rectangle(xy, radius=radius, outline=outline, width=width)
    
    def _draw_circle(self, draw, x, y, radius, fill):
        """绘制圆形"""
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill)
    
    def _draw_deco_circles(self, draw):
        """绘制装饰圆圈"""
        # 右上角大圆
        self._draw_circle(draw, self.width - 80, 80, 60, (232, 213, 196, 100))
        # 左下角小圆
        self._draw_circle(draw, 60, self.height - 150, 40, (212, 165, 165, 100))
        # 左上角中圆
        self._draw_circle(draw, 80, 250, 30, (143, 180, 201, 80))
    
    def generate_cover(self, title, subtitle, tags, date):
        """生成封面页"""
        # 创建背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg'])
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # 装饰元素
        self._draw_deco_circles(draw)
        
        # 字体
        title_font = self._get_font(88)
        subtitle_font = self._get_font(32)
        tag_font = self._get_font(26)
        info_font = self._get_font(24)
        
        # 标题 (居中，带阴影效果)
        y_position = 380
        title_lines = title.split('\n')
        
        for i, line in enumerate(title_lines):
            # 阴影
            draw.text((self.width // 2 + 4, y_position + 4 + i * 110), line, font=title_font,
                     fill=(232, 213, 196), anchor="mt")
            # 主标题
            draw.text((self.width // 2, y_position + i * 110), line, font=title_font,
                     fill=self.COLORS['text_dark'], anchor="mt")
        
        # 副标题
        y_position += 220
        draw.text((self.width // 2, y_position), subtitle, font=subtitle_font,
                 fill=self.COLORS['text_medium'], anchor="mt")
        
        # 标签
        y_position += 80
        tag_x = self.width // 2
        total_width = 3 * 140 + 2 * 20  # 简化计算
        start_x = self.width // 2 - total_width // 2
        
        for tag in tags[:3]:
            bbox = draw.textbbox((0, 0), tag, font=tag_font)
            tag_width = bbox[2] - bbox[0] + 50
            
            # 渐变标签背景
            self._draw_rounded_rect(draw, 
                                   [start_x, y_position, start_x + tag_width, y_position + 50],
                                   25, fill=(232, 213, 196))
            
            # 标签文字
            draw.text((start_x + tag_width // 2, y_position + 14), tag, 
                     font=tag_font, fill=self.COLORS['text_medium'], anchor="mt")
            
            start_x += tag_width + 20
        
        # 底部信息
        y_position = self.height - 180
        
        # 日期
        draw.text((100, y_position), f"📅 {date}", font=info_font,
                 fill=self.COLORS['text_light'])
        
        # 账号
        draw.text((self.width - 100, y_position), "📍 招聘信息", font=info_font,
                 fill=self.COLORS['text_light'], anchor="rt")
        
        return img
    
    def generate_content_page(self, page_num, jobs, page_title="今日岗位"):
        """生成内容页"""
        # 创建背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg'])
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # 装饰元素
        self._draw_deco_circles(draw)
        
        # 字体
        title_font = self._get_font(56)
        subtitle_font = self._get_font(26)
        name_font = self._get_font(32)
        detail_font = self._get_font(24)
        count_font = self._get_font(22)
        footer_font = self._get_font(28)
        
        # 页面标题
        y_position = 100
        draw.text((80, y_position), f"📋 {page_title}", font=title_font,
                 fill=self.COLORS['text_dark'])
        
        # 副标题
        y_position += 70
        draw.text((80, y_position), f"精选{len(jobs)}个好岗位，速看！", font=subtitle_font,
                 fill=self.COLORS['text_light'])
        
        # 装饰线
        y_position += 50
        for i in range(self.width - 160):
            x = 80 + i
            # 波浪线效果
            import math
            y_offset = int(3 * math.sin(i / 20))
            draw.line([(x, y_position + y_offset), (x, y_position + y_offset + 2)], 
                     fill=self.COLORS['accent_cream'], width=1)
        
        y_position += 40
        
        # 岗位列表
        for i, job in enumerate(jobs[:5], 1):
            # 卡片背景
            card_y = y_position
            card_height = 110
            
            # 白色卡片 + 阴影效果
            self._draw_rounded_rect(draw, 
                                   [70, card_y + 4, self.width - 70, card_y + card_height + 4],
                                   24, fill=(232, 213, 196, 60))  # 阴影
            self._draw_rounded_rect(draw, 
                                   [60, card_y, self.width - 60, card_y + card_height],
                                   24, fill=self.COLORS['card_bg'])
            
            # emoji图标
            emoji = self._get_emoji(job.get('name', ''))
            draw.text((110, card_y + card_height // 2), emoji, font=self._get_font(42),
                     fill=self.COLORS['text_dark'], anchor="mm")
            
            # 岗位名称
            draw.text((160, card_y + 20), job.get('name', ''), font=name_font,
                     fill=self.COLORS['text_dark'])
            
            # 岗位详情
            draw.text((160, card_y + 60), job.get('position', ''), font=detail_font,
                     fill=self.COLORS['text_medium'])
            
            # 招聘人数标签
            count_text = f"招{job.get('count', '若干')}"
            bbox = draw.textbbox((0, 0), count_text, font=count_font)
            count_width = bbox[2] - bbox[0] + 30
            count_x = self.width - 60 - count_width - 20
            count_y = card_y + 35
            
            self._draw_rounded_rect(draw, 
                                   [count_x, count_y, count_x + count_width, count_y + 36],
                                   18, fill=self.COLORS['accent_cream'])
            draw.text((count_x + count_width // 2, count_y + 10), count_text, 
                     font=count_font, fill=self.COLORS['text_medium'], anchor="mt")
            
            y_position += card_height + 16
        
        # 底部鼓励语
        y_position = self.height - 200
        draw.text((self.width // 2, y_position), "💪 加油，上岸就在眼前！", font=footer_font,
                 fill=self.COLORS['text_medium'], anchor="mt")
        
        # 关注引导
        y_position += 50
        draw.text((self.width // 2, y_position), "获取更多招聘信息", 
                 font=subtitle_font, fill=self.COLORS['text_light'], anchor="mt")
        
        return img
    
    def generate_summary_page(self, stats, highlights):
        """生成总结页"""
        # 创建背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg'])
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # 装饰元素
        self._draw_deco_circles(draw)
        
        # 字体
        title_font = self._get_font(52)
        number_font = self._get_font(64)
        label_font = self._get_font(24)
        highlight_title_font = self._get_font(28)
        highlight_desc_font = self._get_font(22)
        footer_font = self._get_font(26)
        
        # 标题
        y_position = 120
        draw.text((self.width // 2, y_position), "📊 今日速览", font=title_font,
                 fill=self.COLORS['text_dark'], anchor="mt")
        
        # 统计卡片
        y_position += 100
        card_width = 280
        card_height = 160
        gap = 30
        start_x = (self.width - 3 * card_width - 2 * gap) // 2
        
        for i, stat in enumerate(stats):
            x = start_x + i * (card_width + gap)
            
            # 卡片背景
            self._draw_rounded_rect(draw, 
                                   [x, y_position, x + card_width, y_position + card_height],
                                   20, fill=self.COLORS['card_bg'])
            
            # 数字
            draw.text((x + card_width // 2, y_position + 40), str(stat['number']), 
                     font=number_font, fill=self.COLORS['accent_pink'], anchor="mt")
            
            # 标签
            draw.text((x + card_width // 2, y_position + 110), stat['label'], 
                     font=label_font, fill=self.COLORS['text_medium'], anchor="mt")
        
        # 分隔线
        y_position += card_height + 40
        for i in range(self.width - 160):
            x = 80 + i
            import math
            y_offset = int(2 * math.sin(i / 15))
            draw.line([(x, y_position + y_offset), (x, y_position + y_offset + 2)], 
                     fill=self.COLORS['accent_cream'], width=1)
        
        y_position += 40
        
        # 亮点卡片
        for highlight in highlights[:4]:
            card_height = 100
            
            # 卡片背景
            self._draw_rounded_rect(draw, 
                                   [60, y_position, self.width - 60, y_position + card_height],
                                   20, fill=self.COLORS['card_bg'])
            
            # emoji
            draw.text((110, y_position + card_height // 2), highlight.get('icon', '✅'), 
                     font=self._get_font(36), fill=self.COLORS['text_dark'], anchor="mm")
            
            # 标题
            draw.text((160, y_position + 18), highlight.get('title', ''), 
                     font=highlight_title_font, fill=self.COLORS['text_dark'])
            
            # 描述
            draw.text((160, y_position + 55), highlight.get('desc', ''), 
                     font=highlight_desc_font, fill=self.COLORS['text_medium'])
            
            y_position += card_height + 16
        
        # 底部鼓励语
        y_position = self.height - 200
        draw.text((self.width // 2, y_position), "🌟 祝你早日上岸，拿到铁饭碗！", 
                 font=footer_font, fill=self.COLORS['text_medium'], anchor="mt")
        
        # 互动引导
        y_position += 50
        draw.text((self.width // 2, y_position), "评论区告诉我你想考哪个岗位～", 
                 font=label_font, fill=self.COLORS['text_light'], anchor="mt")
        
        return img


def generate_xhs_images(jobs, output_dir):
    """生成小红书图文"""
    generator = XHSWarmGenerator(width=1080, height=1440)
    
    today = datetime.now().strftime('%Y.%m.%d')
    images = []
    
    # 1. 封面页
    print("\n📄 生成封面页...")
    cover = generator.generate_cover(
        title="太原编制\n招聘日报",
        subtitle="✨ 今日上岸机会来啦 ✨",
        tags=["🏫 教师招聘", "🏥 医疗招聘", "💼 国企招聘"],
        date=today
    )
    cover_path = os.path.join(output_dir, f"cover_warm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    cover.save(cover_path, 'PNG')
    images.append(cover_path)
    print(f"  ✅ {cover_path}")
    
    # 2. 内容页1
    print("\n📋 生成内容页1...")
    content1 = generator.generate_content_page(
        page_num=1,
        jobs=jobs[:5],
        page_title="今日岗位"
    )
    content1_path = os.path.join(output_dir, f"content_warm_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    content1.save(content1_path, 'PNG')
    images.append(content1_path)
    print(f"  ✅ {content1_path}")
    
    # 3. 内容页2
    if len(jobs) > 5:
        print("\n📋 生成内容页2...")
        content2 = generator.generate_content_page(
            page_num=2,
            jobs=jobs[5:10],
            page_title="今日岗位"
        )
        content2_path = os.path.join(output_dir, f"content_warm_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        content2.save(content2_path, 'PNG')
        images.append(content2_path)
        print(f"  ✅ {content2_path}")
    
    # 4. 总结页
    print("\n📊 生成总结页...")
    summary = generator.generate_summary_page(
        stats=[
            {'number': len(jobs), 'label': '招聘岗位'},
            {'number': 8, 'label': '招聘单位'},
            {'number': 50, 'label': '招聘人数'}
        ],
        highlights=[
            {'icon': '🔥', 'title': '热门方向', 'desc': '教师、医疗、国企最抢手'},
            {'icon': '📍', 'title': '工作地点', 'desc': '太原市各区县都有'},
            {'icon': '⏰', 'title': '报名提醒', 'desc': '别错过报名时间哦'},
            {'icon': '💡', 'title': '备考小贴士', 'desc': '提前准备，一战上岸！'}
        ]
    )
    summary_path = os.path.join(output_dir, f"summary_warm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    summary.save(summary_path, 'PNG')
    images.append(summary_path)
    print(f"  ✅ {summary_path}")
    
    return images


if __name__ == "__main__":
    # 测试数据
    test_jobs = [
        {"name": "太原市教育局", "position": "小学语文教师", "count": "5人"},
        {"name": "山西省人民医院", "position": "护理人员", "count": "10人"},
        {"name": "晋能控股集团", "position": "技术员", "count": "20人"},
        {"name": "太原市中心医院", "position": "医生", "count": "8人"},
        {"name": "太原市人社局", "position": "公务员", "count": "3人"},
        {"name": "山西焦煤集团", "position": "工程师", "count": "15人"},
        {"name": "太原市卫健委", "position": "护士", "count": "12人"},
    ]
    
    output_dir = "/home/yan/wechat-publisher/xhs-output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("🎨 生成小红书图文 (暖色手绘风格)")
    print("=" * 60)
    
    images = generate_xhs_images(test_jobs, output_dir)
    
    print("\n" + "=" * 60)
    print(f"✅ 生成完成！共 {len(images)} 张图片")
    print("=" * 60)
