#!/usr/bin/env python3
"""
小红书招聘图文生成器 - 参照HTML模板的现代设计风格
特点：浅色背景 + 大量留白 + 圆角卡片 + 清晰层次
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class XHSModernGenerator:
    """现代风格小红书图文生成器"""
    
    # 配色方案 (参照HTML模板)
    COLORS = {
        'bg': (248, 246, 243),           # 暖白背景 #F8F6F3
        'text_dark': (26, 26, 26),       # 深色文字 #1A1A1A
        'text_medium': (102, 102, 102),  # 中等灰 #666
        'text_light': (153, 153, 153),   # 浅灰 #999
        'accent': (137, 180, 232),       # 蓝色点缀 #89B4E8
        'accent_gradient': (122, 163, 217),  # 蓝色渐变 #7AA3D9
        'card_bg': (255, 255, 255),      # 卡片白 #FFFFFF
        'divider': (232, 228, 224),      # 分隔线 #E8E4E0
        'tag_bg': (210, 168, 168),       # 标签背景 #D2A8A8
        'badge_bg': (240, 240, 240),     # 徽章背景
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
    
    def _get_font(self, size, bold=False):
        """获取字体"""
        if self.font_path:
            try:
                return ImageFont.truetype(self.font_path, size)
            except:
                pass
        return ImageFont.load_default()
    
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
    
    def generate_cover(self, title, subtitle, tags, date):
        """生成封面页"""
        # 创建背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg'])
        draw = ImageDraw.Draw(img)
        
        # 字体
        title_font = self._get_font(72, bold=True)
        subtitle_font = self._get_font(28)
        tag_font = self._get_font(24)
        date_font = self._get_font(22)
        
        # 图标背景 (顶部居中)
        icon_x = self.width // 2
        icon_y = 320
        self._draw_rounded_rect(draw, [icon_x - 50, icon_y - 50, icon_x + 50, icon_y + 50], 
                               20, fill=self.COLORS['accent'])
        draw.text((icon_x, icon_y), "📋", font=self._get_font(36), 
                 fill=self.COLORS['card_bg'], anchor="mm")
        
        # 标题
        y_position = 420
        draw.text((self.width // 2, y_position), "太原编制", font=title_font,
                 fill=self.COLORS['text_dark'], anchor="mt")
        y_position += 90
        draw.text((self.width // 2, y_position), "招聘日报", font=title_font,
                 fill=self.COLORS['text_dark'], anchor="mt")
        
        # 副标题
        y_position += 80
        draw.text((self.width // 2, y_position), subtitle, font=subtitle_font,
                 fill=self.COLORS['text_medium'], anchor="mt")
        
        # 标签
        y_position += 80
        tag_x = self.width // 2
        total_width = sum([80, 80, 80]) + 20 * 2  # 简化计算
        start_x = self.width // 2 - total_width // 2
        
        for i, tag in enumerate(tags[:3]):
            bbox = draw.textbbox((0, 0), tag, font=tag_font)
            tag_width = bbox[2] - bbox[0] + 40
            
            # 标签背景
            self._draw_rounded_rect(draw, 
                                   [start_x, y_position, start_x + tag_width, y_position + 44],
                                   22, fill=(137, 180, 232, 40))
            
            # 标签文字
            draw.text((start_x + tag_width // 2, y_position + 12), tag, 
                     font=tag_font, fill=self.COLORS['accent'], anchor="mt")
            
            start_x += tag_width + 20
        
        # 底部信息
        y_position = self.height - 200
        draw.text((self.width // 2, y_position), "太原事编通 · 每日更新", 
                 font=date_font, fill=self.COLORS['text_light'], anchor="mt")
        
        return img
    
    def generate_content_page(self, page_num, jobs, page_title="岗位清单"):
        """生成内容页"""
        # 创建背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg'])
        draw = ImageDraw.Draw(img)
        
        # 字体
        title_font = self._get_font(36, bold=True)
        subtitle_font = self._get_font(22)
        num_font = self._get_font(22, bold=True)
        name_font = self._get_font(30, bold=True)
        detail_font = self._get_font(24)
        badge_font = self._get_font(20)
        page_num_font = self._get_font(120, bold=True)
        
        # 页码 (右上角，半透明)
        draw.text((self.width - 100, 80), f"{page_num:02d}", font=page_num_font,
                 fill=(200, 200, 200), anchor="mt")
        
        # 页面标题
        y_position = 100
        draw.text((80, y_position), f"📋 {page_title}", font=title_font,
                 fill=self.COLORS['text_dark'])
        y_position += 50
        draw.text((80, y_position), f"今日精选 · 共{len(jobs)}个岗位", font=subtitle_font,
                 fill=self.COLORS['text_light'])
        
        # 分隔线
        y_position += 50
        draw.line([(80, y_position), (self.width - 80, y_position)], 
                 fill=self.COLORS['divider'], width=1)
        y_position += 30
        
        # 岗位列表
        for i, job in enumerate(jobs[:5], 1):
            # 卡片背景
            card_y = y_position
            card_height = 100
            self._draw_rounded_rect(draw, 
                                   [60, card_y, self.width - 60, card_y + card_height],
                                   20, fill=self.COLORS['card_bg'])
            
            # 序号圆圈
            circle_x = 110
            circle_y = card_y + card_height // 2
            self._draw_circle(draw, circle_x, circle_y, 24, self.COLORS['accent'])
            draw.text((circle_x, circle_y), str(i), font=num_font,
                     fill=self.COLORS['card_bg'], anchor="mm")
            
            # 岗位名称
            draw.text((150, card_y + 18), job.get('name', ''), font=name_font,
                     fill=self.COLORS['text_dark'])
            
            # 岗位详情
            draw.text((150, card_y + 55), job.get('position', ''), font=detail_font,
                     fill=self.COLORS['text_medium'])
            
            # 招聘人数徽章
            count_text = f"招聘{job.get('count', '若干')}"
            bbox = draw.textbbox((0, 0), count_text, font=badge_font)
            badge_width = bbox[2] - bbox[0] + 24
            badge_x = self.width - 60 - badge_width - 20
            badge_y = card_y + 30
            
            self._draw_rounded_rect(draw, 
                                   [badge_x, badge_y, badge_x + badge_width, badge_y + 32],
                                   16, fill=(240, 240, 240))
            draw.text((badge_x + badge_width // 2, badge_y + 8), count_text, 
                     font=badge_font, fill=self.COLORS['text_medium'], anchor="mt")
            
            y_position += card_height + 16
        
        # 底部引导
        y_position = self.height - 150
        draw.text((self.width // 2, y_position), "📱 关注「太原事编通」获取更多", 
                 font=subtitle_font, fill=self.COLORS['text_light'], anchor="mt")
        
        return img
    
    def generate_summary_page(self, stats, highlights):
        """生成总结页"""
        # 创建背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg'])
        draw = ImageDraw.Draw(img)
        
        # 字体
        title_font = self._get_font(42, bold=True)
        number_font = self._get_font(64, bold=True)
        label_font = self._get_font(24)
        highlight_title_font = self._get_font(28, bold=True)
        highlight_desc_font = self._get_font(22)
        
        # 标题
        y_position = 120
        draw.text((self.width // 2, y_position), "📊 今日招聘速览", font=title_font,
                 fill=self.COLORS['text_dark'], anchor="mt")
        
        # 统计数据
        y_position += 120
        stat_width = (self.width - 160) // len(stats)
        for i, stat in enumerate(stats):
            x = 80 + i * stat_width + stat_width // 2
            
            # 数字
            draw.text((x, y_position), str(stat['number']), font=number_font,
                     fill=self.COLORS['accent'], anchor="mt")
            
            # 标签
            draw.text((x, y_position + 75), stat['label'], font=label_font,
                     fill=self.COLORS['text_medium'], anchor="mt")
        
        # 分隔线
        y_position += 160
        draw.line([(80, y_position), (self.width - 80, y_position)], 
                 fill=self.COLORS['divider'], width=2)
        
        # 亮点卡片
        y_position += 40
        for highlight in highlights[:4]:
            card_height = 100
            self._draw_rounded_rect(draw, 
                                   [60, y_position, self.width - 60, y_position + card_height],
                                   20, fill=self.COLORS['card_bg'])
            
            # 图标背景
            icon_x = 110
            icon_y = y_position + card_height // 2
            self._draw_rounded_rect(draw, 
                                   [icon_x - 28, icon_y - 28, icon_x + 28, icon_y + 28],
                                   12, fill=(137, 180, 232, 30))
            draw.text((icon_x, icon_y), highlight.get('icon', '✅'), 
                     font=self._get_font(28), fill=self.COLORS['accent'], anchor="mm")
            
            # 标题
            draw.text((150, y_position + 18), highlight.get('title', ''), 
                     font=highlight_title_font, fill=self.COLORS['text_dark'])
            
            # 描述
            draw.text((150, y_position + 55), highlight.get('desc', ''), 
                     font=highlight_desc_font, fill=self.COLORS['text_medium'])
            
            y_position += card_height + 16
        
        # 底部引导
        y_position = self.height - 180
        draw.text((self.width // 2, y_position), "💬 评论区留言你感兴趣的岗位", 
                 font=label_font, fill=self.COLORS['text_light'], anchor="mt")
        draw.text((self.width // 2, y_position + 40), "🔔 关注我，每天更新编制岗位", 
                 font=label_font, fill=self.COLORS['text_light'], anchor="mt")
        
        return img
    
    def save(self, img, filename, quality=95):
        """保存图片"""
        img.save(filename, 'PNG', quality=quality)
        print(f"  ✅ 已保存: {filename}")
        return filename


def generate_xhs_images(jobs, output_dir):
    """生成小红书图文"""
    generator = XHSModernGenerator(width=1080, height=1440)
    
    today = datetime.now().strftime('%Y.%m.%d')
    images = []
    
    # 1. 封面页
    print("\n📄 生成封面页...")
    cover = generator.generate_cover(
        title="太原编制招聘日报",
        subtitle=f"📅 {today} 最新岗位汇总",
        tags=["事业编", "国企", "教师"],
        date=today
    )
    cover_path = os.path.join(output_dir, f"cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    generator.save(cover, cover_path)
    images.append(cover_path)
    
    # 2. 内容页1
    print("\n📋 生成内容页1...")
    content1 = generator.generate_content_page(
        page_num=1,
        jobs=jobs[:5],
        page_title="岗位清单"
    )
    content1_path = os.path.join(output_dir, f"content_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    generator.save(content1, content1_path)
    images.append(content1_path)
    
    # 3. 内容页2 (如果有更多岗位)
    if len(jobs) > 5:
        print("\n📋 生成内容页2...")
        content2 = generator.generate_content_page(
            page_num=2,
            jobs=jobs[5:10],
            page_title="岗位清单"
        )
        content2_path = os.path.join(output_dir, f"content_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        generator.save(content2, content2_path)
        images.append(content2_path)
    
    # 4. 总结页
    print("\n📊 生成总结页...")
    summary = generator.generate_summary_page(
        stats=[
            {'number': len(jobs), 'label': '招聘岗位'},
            {'number': 8, 'label': '招聘单位'},
            {'number': 50, 'label': '招聘人数'}
        ],
        highlights=[
            {'icon': '🔥', 'title': '热门岗位', 'desc': '教师、医疗、国企'},
            {'icon': '📍', 'title': '工作地点', 'desc': '太原市各区县'},
            {'icon': '⏰', 'title': '报名时间', 'desc': '详见各公告'},
            {'icon': '💡', 'title': '备考建议', 'desc': '提前准备，关注官网'}
        ]
    )
    summary_path = os.path.join(output_dir, f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    generator.save(summary, summary_path)
    images.append(summary_path)
    
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
    print("🎨 生成小红书图文 (现代设计风格)")
    print("=" * 60)
    
    images = generate_xhs_images(test_jobs, output_dir)
    
    print("\n" + "=" * 60)
    print(f"✅ 生成完成！共 {len(images)} 张图片")
    print("=" * 60)
