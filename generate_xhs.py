#!/usr/bin/env python3
"""
小红书招聘图文生成器 - 模仿爆款风格
风格特点：浅色背景 + 大量留白 + 清单式排版 + 圆角卡片
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class XHSRecruitmentGenerator:
    """小红书招聘图文生成器"""
    
    # 小红书风格配色 (莫兰迪色系)
    COLORS = {
        'bg_warm': (250, 247, 242),        # 暖白背景
        'bg_cream': (252, 249, 244),       # 米白背景
        'bg_light_gray': (245, 245, 247),  # 浅灰背景
        'text_dark': (51, 51, 51),         # 深灰文字
        'text_medium': (102, 102, 102),    # 中灰文字
        'text_light': (153, 153, 153),     # 浅灰文字
        'accent_blue': (135, 169, 206),    # 雾霾蓝
        'accent_pink': (210, 168, 168),    # 豆沙粉
        'accent_green': (152, 193, 167),   # 薄荷绿
        'accent_orange': (210, 178, 144),  # 奶茶色
        'card_white': (255, 255, 255),     # 卡片白
        'card_shadow': (240, 240, 240),    # 卡片阴影
        'divider': (230, 230, 230),        # 分隔线
    }
    
    def __init__(self, width=1080, height=1440):
        """初始化生成器 (9:16比例，适合小红书)"""
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
    
    def generate_cover(self, title, subtitle, tags, date):
        """生成封面页 (大标题 + 标签)"""
        # 创建暖白背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg_warm'])
        draw = ImageDraw.Draw(img)
        
        # 字体
        title_font = self._get_font(72, bold=True)
        subtitle_font = self._get_font(36)
        tag_font = self._get_font(28)
        date_font = self._get_font(24)
        
        # 绘制装饰线条 (顶部)
        draw.line([(100, 120), (self.width - 100, 120)], fill=self.COLORS['divider'], width=2)
        
        # 绘制大标题 (居中，分两行)
        y_position = 200
        title_lines = self._split_title(title, 8)
        for line in title_lines:
            draw.text((self.width // 2, y_position), line, font=title_font, 
                     fill=self.COLORS['text_dark'], anchor="mt")
            y_position += 90
        
        # 绘制副标题
        y_position += 40
        draw.text((self.width // 2, y_position), subtitle, font=subtitle_font,
                 fill=self.COLORS['text_medium'], anchor="mt")
        
        # 绘制标签
        y_position += 100
        tag_x = self.width // 2
        for tag in tags[:3]:  # 最多3个标签
            # 绘制标签背景
            bbox = draw.textbbox((0, 0), tag, font=tag_font)
            tag_width = bbox[2] - bbox[0] + 40
            tag_box = [tag_x - tag_width//2, y_position, tag_x + tag_width//2, y_position + 45]
            self._draw_rounded_rect(draw, tag_box, 22, fill=self.COLORS['accent_blue'])
            
            # 绘制标签文字
            draw.text((tag_x, y_position + 10), tag, font=tag_font,
                     fill=self.COLORS['card_white'], anchor="mt")
            
            tag_x += tag_width + 20
        
        # 绘制日期
        y_position = self.height - 150
        draw.text((self.width // 2, y_position), date, font=date_font,
                 fill=self.COLORS['text_light'], anchor="mt")
        
        # 绘制装饰线条 (底部)
        draw.line([(100, self.height - 100), (self.width - 100, self.height - 100)], 
                 fill=self.COLORS['divider'], width=2)
        
        return img
    
    def _split_title(self, title, max_chars):
        """分割标题 (每行最多字符数)"""
        lines = []
        current = ""
        for char in title:
            current += char
            if len(current) >= max_chars:
                lines.append(current)
                current = ""
        if current:
            lines.append(current)
        return lines
    
    def generate_content_page(self, page_num, items, page_title=""):
        """生成内容页 (清单式排版)"""
        # 创建暖白背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg_warm'])
        draw = ImageDraw.Draw(img)
        
        # 字体
        page_font = self._get_font(28)
        num_font = self._get_font(48, bold=True)
        title_font = self._get_font(32, bold=True)
        content_font = self._get_font(26)
        small_font = self._get_font(22)
        
        # 绘制页码 (右上角)
        draw.text((self.width - 80, 60), f"{page_num:02d}", font=self._get_font(60, bold=True),
                 fill=self.COLORS['divider'], anchor="mt")
        
        # 绘制页面标题
        y_position = 120
        if page_title:
            draw.text((100, y_position), page_title, font=title_font,
                     fill=self.COLORS['text_dark'])
            y_position += 60
        
        # 绘制分隔线
        draw.line([(100, y_position), (self.width - 100, y_position)], 
                 fill=self.COLORS['divider'], width=1)
        y_position += 40
        
        # 绘制清单项
        for i, item in enumerate(items[:5], 1):
            # 绘制序号圆圈
            circle_x = 100
            circle_y = y_position + 25
            draw.ellipse([circle_x - 25, circle_y - 25, circle_x + 25, circle_y + 25],
                        fill=self.COLORS['accent_blue'])
            draw.text((circle_x, circle_y), str(i), font=num_font,
                     fill=self.COLORS['card_white'], anchor="mm")
            
            # 绘制卡片背景
            card_box = [140, y_position, self.width - 80, y_position + 100]
            self._draw_rounded_rect(draw, card_box, 12, fill=self.COLORS['card_white'],
                                   outline=self.COLORS['card_shadow'], width=1)
            
            # 绘制标题
            draw.text((160, y_position + 15), item.get('title', ''), font=title_font,
                     fill=self.COLORS['text_dark'])
            
            # 绘制详情
            detail = item.get('detail', '')
            draw.text((160, y_position + 55), detail, font=content_font,
                     fill=self.COLORS['text_medium'])
            
            # 绘制标签
            if 'tag' in item:
                tag_text = item['tag']
                bbox = draw.textbbox((0, 0), tag_text, font=small_font)
                tag_width = bbox[2] - bbox[0] + 20
                tag_box = [160, y_position + 80, 160 + tag_width, y_position + 105]
                self._draw_rounded_rect(draw, tag_box, 10, fill=self.COLORS['accent_pink'])
                draw.text((170, y_position + 82), tag_text, font=small_font,
                         fill=self.COLORS['card_white'])
            
            y_position += 120
        
        # 绘制底部引导
        y_position = self.height - 120
        draw.text((self.width // 2, y_position), "📱 获取更多招聘信息", 
                 font=small_font, fill=self.COLORS['text_light'], anchor="mt")
        
        return img
    
    def generate_summary_page(self, stats, highlights):
        """生成总结页 (数据统计 + 亮点)"""
        # 创建暖白背景
        img = Image.new('RGB', (self.width, self.height), self.COLORS['bg_warm'])
        draw = ImageDraw.Draw(img)
        
        # 字体
        title_font = self._get_font(48, bold=True)
        stat_font = self._get_font(64, bold=True)
        label_font = self._get_font(28)
        content_font = self._get_font(26)
        
        # 绘制标题
        y_position = 150
        draw.text((self.width // 2, y_position), "📊 今日招聘速览", font=title_font,
                 fill=self.COLORS['text_dark'], anchor="mt")
        
        # 绘制统计数据
        y_position += 100
        stat_width = (self.width - 200) // len(stats)
        for i, stat in enumerate(stats):
            x = 100 + i * stat_width + stat_width // 2
            draw.text((x, y_position), str(stat['number']), font=stat_font,
                     fill=self.COLORS['accent_blue'], anchor="mt")
            draw.text((x, y_position + 70), stat['label'], font=label_font,
                     fill=self.COLORS['text_medium'], anchor="mt")
        
        # 绘制分隔线
        y_position += 150
        draw.line([(100, y_position), (self.width - 100, y_position)], 
                 fill=self.COLORS['divider'], width=2)
        
        # 绘制亮点内容
        y_position += 60
        for highlight in highlights[:4]:
            # 绘制亮点卡片
            card_box = [80, y_position, self.width - 80, y_position + 120]
            self._draw_rounded_rect(draw, card_box, 15, fill=self.COLORS['card_white'],
                                   outline=self.COLORS['card_shadow'], width=1)
            
            # 绘制图标
            draw.text((120, y_position + 20), highlight.get('icon', '✅'), 
                     font=self._get_font(36), fill=self.COLORS['accent_green'])
            
            # 绘制标题
            draw.text((170, y_position + 15), highlight.get('title', ''), font=title_font,
                     fill=self.COLORS['text_dark'])
            
            # 绘制内容
            draw.text((170, y_position + 60), highlight.get('content', ''), font=content_font,
                     fill=self.COLORS['text_medium'])
            
            y_position += 140
        
        # 绘制底部引导
        y_position = self.height - 150
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
    """生成小红书图文 (多页)"""
    generator = XHSRecruitmentGenerator(width=1080, height=1440)
    
    today = datetime.now().strftime('%Y.%m.%d')
    month = datetime.now().strftime('%m月')
    
    images = []
    
    # 第1页: 封面
    cover = generator.generate_cover(
        title=f"太原编制招聘日报",
        subtitle=f"📅 {today} 最新岗位汇总",
        tags=["事业编", "国企", "教师"],
        date=today
    )
    cover_path = os.path.join(output_dir, f"xhs_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    cover.save(cover_path, 'PNG')
    images.append(cover_path)
    print(f"  ✅ 封面页: {cover_path}")
    
    # 第2-3页: 内容页 (每页5个岗位)
    for page_num in range(1, 3):
        page_items = []
        start_idx = (page_num - 1) * 5
        for job in jobs[start_idx:start_idx + 5]:
            page_items.append({
                'title': job.get('name', '未知单位'),
                'detail': job.get('position', '招聘岗位'),
                'tag': job.get('count', '若干')
            })
        
        if page_items:
            content_page = generator.generate_content_page(
                page_num=page_num + 1,
                items=page_items,
                page_title=f"📋 岗位清单 ({page_num})"
            )
            content_path = os.path.join(output_dir, f"xhs_content_{page_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            content_page.save(content_path, 'PNG')
            images.append(content_path)
            print(f"  ✅ 内容页{page_num}: {content_path}")
    
    # 最后一页: 总结页
    summary = generator.generate_summary_page(
        stats=[
            {'number': len(jobs), 'label': '招聘岗位'},
            {'number': 10, 'label': '招聘单位'},
            {'number': 50, 'label': '招聘人数'}
        ],
        highlights=[
            {'icon': '🔥', 'title': '热门岗位', 'content': '教师、医疗、国企'},
            {'icon': '📍', 'title': '工作地点', 'content': '太原市各区县'},
            {'icon': '⏰', 'title': '报名时间', 'content': '详见各公告'},
            {'icon': '💡', 'title': '备考建议', 'content': '提前准备，关注官网'}
        ]
    )
    summary_path = os.path.join(output_dir, f"xhs_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    summary.save(summary_path, 'PNG')
    images.append(summary_path)
    print(f"  ✅ 总结页: {summary_path}")
    
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
    
    print("=" * 50)
    print("🎨 生成小红书图文 (新风格)")
    print("=" * 50)
    
    images = generate_xhs_images(test_jobs, output_dir)
    
    print("\n" + "=" * 50)
    print(f"✅ 生成完成！共 {len(images)} 张图片")
    print("=" * 50)
