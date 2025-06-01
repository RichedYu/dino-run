import pygame
import random
import math
import sys
import os

# Initialize Pygame
# 初始化 Pygame
pygame.init()
pygame.mixer.init() # Initialize the mixer for sound / 初始化混音器以播放声音

# Game Constants
# 游戏常量
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 400
GROUND_HEIGHT = 80 # Height of the ground surface from the bottom / 地面距离底部的高度

# Colors (RGB values) - Enhanced color palette
# 颜色 (RGB值) - 增强调色板
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
GREEN = (0, 180, 0)         # Main green for cactus/dino / 仙人掌/恐龙的主要绿色
DARK_GREEN = (0, 120, 0)    # Darker green for details/shadows / 用于细节/阴影的深绿色
RED = (220, 50, 50)         # For danger, life power-up / 用于危险提示，生命道具
ORANGE = (255, 140, 0)      # For fireballs, sunset / 用于火球，日落
YELLOW = (255, 215, 0)      # For score power-up, fireball core / 用于得分道具，火球核心
BLUE = (30, 144, 255)       # For invincibility power-up / 用于无敌道具
PURPLE = (148, 0, 211)      # For Pterodactyl / 用于翼龙
BROWN = (139, 69, 19)       # For ground line / 用于地面线条
SAND = (224, 198, 153)      # Lighter ground color, more like sand/desert / 较浅的地面颜色，更像沙子/沙漠

# Sky colors for day/night cycle
# 日夜循环的天空颜色
SKY_COLORS = {
    'day': (135, 206, 235),    # Light blue for daytime / 白天的浅蓝色
    'sunset': (255, 165, 0),   # Orange/Red for sunset / 日落的橙色/红色
    'night': (25, 25, 112)     # Dark blue for night / 夜晚的深蓝色
}

# Game Settings
# 游戏设置
GRAVITY = 0.8
JUMP_STRENGTH = -17 # Slightly stronger jump / 跳跃力度稍强
DUCK_SPEED = 8      # Not directly used, speed is game_speed / 未直接使用，速度是 game_speed
GAME_SPEED = 7      # Initial game speed / 初始游戏速度
SPEED_INCREASE = 0.003 # How much speed increases per frame / 每帧速度增加量

# --- Language Settings ---
# --- 语言设置 ---
LANGUAGES = {
    "EN": {
        "caption": "Enhanced Pixel Dino Run",
        "score": "Score",
        "hi_score": "Hi",
        "lives": "Lives",
        "last_life": "Last Life!",
        "invincible": "INVINCIBLE",
        "paused": "PAUSED",
        "resume": "Press P to Resume",
        "game_over": "GAME OVER",
        "final_score": "Final Score",
        "new_high_score": "New High Score!",
        "restart": "Press R to Restart",
        "jump_inst": "SPACE/UP: Jump",
        "duck_inst": "DOWN/S: Duck",
        "shoot_inst": "X: Shoot",
        "pause_inst": "P: Pause",
        "lang_inst": "L: Switch Lang",
        "start_message_title": "Starting Enhanced Pixel Dino Run...",
        "controls_title": "Controls:",
        "powerups_title": "Power-ups:",
        "powerup_life": "Red (♥): Extra Life",
        "powerup_invincible": "Blue (★): Temporary Invincibility",
        "powerup_score": "Yellow (◆): Bonus Score",
        "font_loaded_success": "Successfully loaded font: {font_name}",
        "font_load_warning_specific": "Warning: Pixel font '{font_name}' exists but failed to load. Using default system font.",
        "font_load_warning_missing": "Warning: Pixel font '{font_name}' not found in assets/fonts/. Using default system font.",
        "user_chinese_font_success": "Successfully loaded user's Chinese font: {font_path}",
        "user_chinese_font_error": "Warning: User's Chinese font '{font_path}' failed to load: {error}. Trying system fonts...",
        "chinese_font_success": "Successfully loaded Chinese system font: {font_name}",
        "chinese_font_system_warning": "Warning: Chinese system fonts '{font_names}' not found. Using default system font for Chinese (may not display well).",
        "created_dir": "Created directory:",
        "create_dir_warning": "Warning: Could not create directory",
        "save_highscore_warning": "Warning: Could not save high score."
    },
    "CN": {
        "caption": "像素恐龙跑酷加强版",
        "score": "分数",
        "hi_score": "最高分",
        "lives": "生命",
        "last_life": "最后一条命!",
        "invincible": "无敌状态",
        "paused": "已暂停",
        "resume": "按 P键 继续",
        "game_over": "游戏结束",
        "final_score": "最终得分",
        "new_high_score": "新高分!",
        "restart": "按 R键 重新开始",
        "jump_inst": "空格/上: 跳跃",
        "duck_inst": "下/S: 下蹲",
        "shoot_inst": "X:射击",
        "pause_inst": "P: 暂停",
        "lang_inst": "L: 切换语言",
        "start_message_title": "开始运行 像素恐龙跑酷加强版...",
        "controls_title": "操作说明:",
        "powerups_title": "道具说明:",
        "powerup_life": "红色 (♥): 额外生命",
        "powerup_invincible": "蓝色 (★): 短暂无敌",
        "powerup_score": "黄色 (◆): 额外加分",
        "font_loaded_success": "成功加载字体: {font_name}",
        "font_load_warning_specific": "警告: 像素字体 '{font_name}' 存在但加载失败。将使用默认系统字体。",
        "font_load_warning_missing": "警告: 像素字体 '{font_name}' 未在 assets/fonts/ 找到。将使用默认系统字体。",
        "user_chinese_font_success": "成功加载用户自定义中文字体: {font_path}",
        "user_chinese_font_error": "警告: 用户自定义中文字体 '{font_path}' 加载失败: {error}。尝试系统字体...",
        "chinese_font_success": "成功加载中文系统字体: {font_name}",
        "chinese_font_system_warning": "警告: 中文系统字体 '{font_names}' 未找到。将使用默认系统字体显示中文 (可能效果不佳)。",
        "created_dir": "已创建目录:",
        "create_dir_warning": "警告: 无法创建目录",
        "save_highscore_warning": "警告: 无法保存最高分。"
    }
}
current_language = "EN" # Default language / 默认语言

def get_text(key):
    """获取当前语言的文本 / Get text for the current language"""
    return LANGUAGES[current_language].get(key, key) # Fallback to key if not found / 如果未找到则返回键本身

# --- Asset Loading ---
# --- 资源加载 ---

# --- AudioManager ---
class AudioManager:
    """音频管理器 / Audio Manager"""

    def __init__(self):
        """初始化音频管理器 / Initialize audio manager"""
        self.sounds = {}
        self.music_playing = False

        # 音效文件路径 / Sound effect file paths
        # 用户需要将音效文件（通常是 .wav 格式）放入 "assets/sounds/" 文件夹中，
        # 并确保下面的文件名与实际文件名匹配。
        # User needs to place sound files (usually .wav format) into the "assets/sounds/" folder,
        # and ensure the filenames below match the actual filenames.
        base_sound_path = "assets/sounds/"
        self.sound_files = {
            'jump': os.path.join(base_sound_path, 'jump.mp3'),       # 例如: 'your_jump_sound.wav'
            'land': os.path.join(base_sound_path, 'land.mp3'),       # 例如: 'your_land_sound.wav'
            'duck': os.path.join(base_sound_path, 'duck.mp3'),       # 例如: 'your_duck_sound.wav'
            'fireball': os.path.join(base_sound_path, 'fireball.mp3'), # 例如: 'your_fireball_sound.wav'
            'hit': os.path.join(base_sound_path, 'hit.mp3'),         # 例如: 'your_hit_sound.wav'
            'powerup': os.path.join(base_sound_path, 'powerup.mp3'),   # 例如: 'your_powerup_sound.wav'
            'destroy': os.path.join(base_sound_path, 'destroy.mp3'),   # 例如: 'your_destroy_sound.wav'
            'game_over': os.path.join(base_sound_path, 'game_over.mp3'),# 例如: 'your_game_over_sound.wav'
            'pause': os.path.join(base_sound_path, 'pause.mp3')      # 例如: 'your_pause_sound.wav'
        }

        # 背景音乐文件路径 / Background music file path
        # 用户需要将背景音乐文件（通常是 .mp3 格式）放入 "assets/music/" 文件夹中，
        # 并确保下面的文件名与实际文件名匹配。
        # User needs to place the background music file (usually .mp3 format) into the "assets/music/" folder,
        # and ensure the filename below matches the actual filename.
        self.music_file = os.path.join("assets/music/", 'background_lemon.mp3') # 例如: 'your_background_music.mp3'

        self.load_sounds()

    def load_sounds(self):
        """加载音效文件 / Load sound files"""
        if not pygame.mixer.get_init(): # Ensure mixer is initialized / 确保混音器已初始化
            pygame.mixer.init()

        for sound_name, file_path in self.sound_files.items():
            if os.path.exists(file_path):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    self.sounds[sound_name].set_volume(0.5) # Set default volume / 设置默认音量
                except pygame.error as e:
                    print(f"Warning: Could not load sound '{sound_name}' from {file_path}: {e}")
                    self.sounds[sound_name] = None
            else:
                # print(f"Warning: Sound file not found for '{sound_name}': {file_path}")
                self.sounds[sound_name] = None # Placeholder if file doesn't exist / 如果文件不存在则使用占位符

    def play_sound(self, sound_name):
        """播放音效 / Play sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except pygame.error as e:
                print(f"Warning: Could not play sound '{sound_name}': {e}")

    def stop_sound(self, sound_name):
        """停止特定音效 / Stop a specific sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].stop()
            except pygame.error as e:
                print(f"Warning: Could not stop sound '{sound_name}': {e}")

    def play_music(self):
        """播放背景音乐 / Play background music"""
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if os.path.exists(self.music_file) and not self.music_playing:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.set_volume(0.3) # Set music volume / 设置音乐音量
                pygame.mixer.music.play(-1)  # 循环播放 / Loop playback
                self.music_playing = True
            except pygame.error as e:
                print(f"Warning: Could not load or play music from {self.music_file}: {e}")

    def stop_music(self):
        """停止背景音乐 / Stop background music"""
        if self.music_playing:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
            except pygame.error as e:
                print(f"Warning: Could not stop music: {e}")

# --- ParticleSystem ---
class ParticleSystem:
    """粒子系统 / Particle System"""

    def __init__(self):
        """初始化粒子系统 / Initialize particle system"""
        self.particles = []

    def add_explosion(self, x, y, color=ORANGE, count=12, size_range=(2,5), speed_range=(1,4), life_range=(20,40)):
        """添加爆炸粒子效果 / Add explosion particle effect"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(speed_range[0], speed_range[1])
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed

            particle = {
                'x': x, 'y': y,
                'vx': velocity_x, 'vy': velocity_y,
                'life': random.randint(life_range[0], life_range[1]),
                'max_life': life_range[1],
                'color': color,
                'size': random.randint(size_range[0], size_range[1])
            }
            self.particles.append(particle)

    def add_pickup_effect(self, x, y, color=YELLOW, count=8, size_range=(3,6), speed_range=(0.5,2), life_range=(30,50)):
        """添加道具拾取粒子效果 / Add pickup particle effect"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(speed_range[0], speed_range[1])
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed - 1.5  # 向上飘散 / Drift upward

            particle = {
                'x': x, 'y': y,
                'vx': velocity_x, 'vy': velocity_y,
                'life': random.randint(life_range[0], life_range[1]),
                'max_life': life_range[1],
                'color': color,
                'size': random.randint(size_range[0], size_range[1])
            }
            self.particles.append(particle)

    def update(self):
        """更新粒子 / Update particles"""
        for particle in self.particles[:]: # Iterate over a copy for safe removal / 迭代副本以便安全删除
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.05  # Slight gravity effect on particles / 对粒子施加轻微重力效果
            particle['life'] -= 1

            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        """绘制粒子 / Draw particles"""
        for particle in self.particles:
            # Calculate alpha for fade out effect
            # 计算淡出效果的 alpha 值
            alpha = int(255 * (particle['life'] / particle['max_life']))
            # Create a temporary surface for the particle to handle alpha transparency
            # 为粒子创建临时表面以处理 alpha 透明度
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*particle['color'], alpha),
                               (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))

# --- Background ---
class Background:
    """背景管理器 / Background Manager"""

    def __init__(self, width, height):
        """初始化背景 / Initialize background"""
        self.width = width
        self.height = height
        self.ground_y = height - GROUND_HEIGHT

        # 云朵 / Clouds
        self.clouds = []
        self.generate_clouds()

        # 地面装饰 / Ground decorations
        self.ground_decorations = []
        self.ground_scroll_x = 0
        self.generate_ground_decorations()

        # 远景山丘 (中景层) / Background hills (Mid-ground layer)
        self.hills_mid = []
        self.generate_hills_layer(self.hills_mid, count=5, y_base_offset=20, height_range=(40,100), color_offset=-30, speed_multiplier=0.2)

        # 更远的山丘 (远景层) / Farther hills (Far-ground layer)
        self.hills_far = []
        self.generate_hills_layer(self.hills_far, count=3, y_base_offset=50, height_range=(80,150), color_offset=-60, speed_multiplier=0.1)

        self.time_factor = 0 # For day/night cycle / 用于日夜循环

    def generate_clouds(self, count=7):
        """生成云朵 / Generate clouds"""
        self.clouds = []
        for i in range(count):
            cloud = {
                'x': random.randint(0, self.width * 2), # Start some off-screen / 一些从屏幕外开始
                'y': random.randint(30, self.height // 3),
                'speed': random.uniform(0.1, 0.5), # Slower speeds for clouds / 云朵的较慢速度
                'size': random.randint(20, 40),
                'type': random.randint(0, 2) # Different cloud shapes / 不同的云朵形状
            }
            self.clouds.append(cloud)

    def generate_ground_decorations(self, count=30):
        """生成地面装饰 / Generate ground decorations (rocks, grass tufts)"""
        self.ground_decorations = []
        for i in range(count):
            decoration = {
                'x': random.randint(0, self.width * 2), # Spread over a wider area for scrolling / 分布在更宽的区域以便滚动
                'type': random.choice(['rock', 'grass', 'bush']),
                'size': random.randint(4, 10),
                'color_variation': random.randint(-10, 10) # Slight color variation / 轻微的颜色变化
            }
            self.ground_decorations.append(decoration)

    def generate_hills_layer(self, hill_list, count, y_base_offset, height_range, color_offset, speed_multiplier):
        """生成一层山丘 / Generate a layer of hills"""
        hill_list.clear()
        current_x = -random.randint(50,150)
        for _ in range(count * 2): # Generate more to cover scrolling / 生成更多以覆盖滚动区域
            h_width = random.randint(200, 400)
            h_height = random.randint(height_range[0], height_range[1])
            hill = {
                'x': current_x,
                'y_offset': y_base_offset, # How much higher than ground_y the base is / 底部比 ground_y 高多少
                'width': h_width,
                'height': h_height,
                'color_offset': color_offset, # How much darker than sky color / 比天空颜色暗多少
                'speed_multiplier': speed_multiplier # Relative to game_speed / 相对于游戏速度
            }
            hill_list.append(hill)
            current_x += h_width - random.randint(30,80) # Overlap hills slightly / 山丘略微重叠

    def get_sky_color(self):
        """获取当前天空颜色，实现日夜平滑过渡 / Get current sky color with smooth day/night transition"""
        # Cycle duration (e.g., 3000 frames for a full day-night-day cycle)
        # 循环持续时间 (例如，3000帧完成一个完整的日-夜-日循环)
        cycle_duration = 3000
        time_in_cycle = self.time_factor % cycle_duration

        # Define transition points (as fractions of cycle_duration)
        # 定义过渡点 (以 cycle_duration 的分数表示)
        day_end = 0.40    # End of day, start of sunset / 白天结束，日落开始
        sunset_end = 0.55 # End of sunset, start of night / 日落结束，夜晚开始
        night_end = 0.85  # End of night, start of sunrise / 夜晚结束，日出开始
        sunrise_end = 1.0 # End of sunrise, back to day (same as 0.0) / 日出结束，回到白天 (与0.0相同)

        current_sky = SKY_COLORS['day'] # Default / 默认

        if time_in_cycle < day_end * cycle_duration: # Daytime / 白天
            current_sky = SKY_COLORS['day']
        elif time_in_cycle < sunset_end * cycle_duration: # Sunset transition / 日落过渡
            progress = (time_in_cycle - day_end * cycle_duration) / ((sunset_end - day_end) * cycle_duration)
            current_sky = self._interpolate_color(SKY_COLORS['day'], SKY_COLORS['sunset'], progress)
        elif time_in_cycle < night_end * cycle_duration: # Nighttime / 夜晚
            current_sky = SKY_COLORS['night']
        else: # Sunrise transition / 日出过渡
            progress = (time_in_cycle - night_end * cycle_duration) / ((sunrise_end - night_end) * cycle_duration)
            current_sky = self._interpolate_color(SKY_COLORS['night'], SKY_COLORS['day'], progress)
        return current_sky

    def _interpolate_color(self, color1, color2, t):
        """Helper to interpolate between two RGB colors / 辅助函数，在两种RGB颜色之间进行插值"""
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

    def update(self, game_speed):
        """更新背景元素位置 / Update background element positions"""
        self.time_factor += 0.5 # Slower day/night cycle progression / 较慢的日夜循环进程

        # Update clouds / 更新云朵
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed'] * (game_speed / GAME_SPEED) # Scale cloud speed slightly with game speed / 根据游戏速度略微调整云朵速度
            if cloud['x'] + cloud['size'] * 2 < 0: # If cloud moves off screen left / 如果云朵移出屏幕左侧
                cloud['x'] = self.width + random.randint(cloud['size'], cloud['size'] + 100) # Reappear on the right / 在右侧重新出现
                cloud['y'] = random.randint(30, self.height // 3) # New random height / 新的随机高度

        # Update ground decorations (scroll with game speed)
        # 更新地面装饰 (随游戏速度滚动)
        self.ground_scroll_x = (self.ground_scroll_x - game_speed) % self.width # Keep scroll within window width for seamless loop /保持滚动在窗口宽度内以实现无缝循环

        # Update parallax scrolling hills
        # 更新视差滚动山丘
        for hill_layer in [self.hills_mid, self.hills_far]:
            for hill in hill_layer:
                hill['x'] -= game_speed * hill['speed_multiplier']
                if hill['x'] + hill['width'] < 0:
                    # Find the rightmost hill's x and width to position this one after it
                    # 找到最右边山丘的x和宽度，以便将此山丘定位在其后
                    max_x = 0
                    for h_other in hill_layer:
                        if h_other['x'] + h_other['width'] > max_x:
                            max_x = h_other['x'] + h_other['width']
                    hill['x'] = max_x - random.randint(0,50) # Reposition to the far right, slightly overlapping / 重新定位到最右边，略微重叠

    def draw(self, screen):
        """绘制背景所有元素 / Draw all background elements"""
        sky_color = self.get_sky_color()
        screen.fill(sky_color) # Fill sky / 填充天空

        # Draw far hills / 绘制远景山丘
        for hill in self.hills_far:
            self.draw_hill_shape(screen, hill, sky_color)

        # Draw mid hills / 绘制中景山丘
        for hill in self.hills_mid:
            self.draw_hill_shape(screen, hill, sky_color)

        # Draw clouds / 绘制云朵
        for cloud in self.clouds:
            self.draw_cloud_shape(screen, cloud['x'], cloud['y'], cloud['size'], cloud['type'])

        # Draw ground / 绘制地面
        pygame.draw.rect(screen, SAND, (0, self.ground_y, self.width, GROUND_HEIGHT))
        # Draw ground decorations / 绘制地面装饰
        for i in range(len(self.ground_decorations)):
            deco = self.ground_decorations[i]
            # Calculate position based on base x and current scroll, wrapping around
            # 根据基础x和当前滚动计算位置，并进行环绕
            draw_x = (deco['x'] + self.ground_scroll_x)
            if -20 < draw_x < self.width + 20 : # Only draw if visible / 仅在可见时绘制
                 self.draw_ground_decoration_shape(screen, draw_x, self.ground_y, deco)
        pygame.draw.line(screen, BROWN, (0, self.ground_y), (self.width, self.ground_y), 3)


    def draw_hill_shape(self, screen, hill, sky_color):
        """Helper to draw a single hill with varying color / 辅助函数，绘制具有不同颜色的单个山丘"""
        hill_base_color = tuple(max(0, c + hill['color_offset']) for c in sky_color)
        # Simple polygon for a hill / 山丘的简单多边形
        points = [
            (int(hill['x']), self.ground_y - hill['y_offset']),
            (int(hill['x'] + hill['width'] * 0.2), self.ground_y - hill['y_offset'] - hill['height'] * 0.7),
            (int(hill['x'] + hill['width'] * 0.5), self.ground_y - hill['y_offset'] - hill['height']),
            (int(hill['x'] + hill['width'] * 0.8), self.ground_y - hill['y_offset'] - hill['height'] * 0.6),
            (int(hill['x'] + hill['width']), self.ground_y - hill['y_offset'])
        ]
        pygame.draw.polygon(screen, hill_base_color, points)

    def draw_cloud_shape(self, screen, x, y, size, cloud_type):
        """Helper to draw a single cloud (pixel art style with circles) / 辅助函数，绘制单个云朵 (带圆圈的像素艺术风格)"""
        # Base cloud color, slightly off-white for depth against pure white text
        # 云朵基础颜色，略微偏白，以在纯白色文本中产生深度感
        cloud_color = (240, 240, 240)
        shadow_color = (200, 200, 200) # Simple shadow / 简单阴影

        if cloud_type == 0: # Fluffy cloud / 蓬松的云
            pygame.draw.circle(screen, shadow_color, (int(x + size*0.5 + 2), int(y + size*0.3 + 2)), int(size * 0.6))
            pygame.draw.circle(screen, cloud_color, (int(x), int(y)), size)
            pygame.draw.circle(screen, cloud_color, (int(x + size), int(y)), int(size * 0.8))
            pygame.draw.circle(screen, cloud_color, (int(x + size * 0.5), int(y - size * 0.3)), int(size * 0.7))
        elif cloud_type == 1: # Longer cloud / 较长的云
            pygame.draw.ellipse(screen, shadow_color, (x+2, y+2, size * 2.5, size * 1.2))
            pygame.draw.ellipse(screen, cloud_color, (x, y, size * 2.5, size * 1.2))
            pygame.draw.circle(screen, cloud_color, (int(x + size * 0.5), int(y + size * 0.2)), int(size*0.8))
            pygame.draw.circle(screen, cloud_color, (int(x + size * 1.8), int(y + size * 0.1)), int(size*0.7))
        else: # Small puff / 小团云
            pygame.draw.circle(screen, shadow_color, (int(x+2), int(y+2)), int(size * 0.7))
            pygame.draw.circle(screen, cloud_color, (int(x), int(y)), int(size * 0.7))

    def draw_ground_decoration_shape(self, screen, x, ground_y, decoration):
        """Helper to draw ground decorations (pixel art style) / 辅助函数，绘制地面装饰 (像素艺术风格)"""
        size = decoration['size']
        # Apply color variation to base colors
        # 将颜色变化应用于基础颜色
        rock_color = tuple(max(0, min(255, c + decoration['color_variation'])) for c in GRAY)
        grass_color = tuple(max(0, min(255, c + decoration['color_variation'])) for c in DARK_GREEN)

        if decoration['type'] == 'rock':
            pygame.draw.rect(screen, rock_color, (int(x), int(ground_y - size), size, size))
            pygame.draw.rect(screen, tuple(max(0,c-20) for c in rock_color), (int(x+1), int(ground_y - size+1), size-2, size-2)) # Inner shadow / 内部阴影
        elif decoration['type'] == 'grass':
            for i in range(size // 2): # Draw a few blades / 绘制几片草叶
                pygame.draw.line(screen, grass_color,
                                 (int(x + i*2 - size//2 +2), int(ground_y)),
                                 (int(x + i*2 - size//2 +2 + random.randint(-1,1)), int(ground_y - size - random.randint(0,2))), 1)
        elif decoration['type'] == 'bush':
            pygame.draw.circle(screen, grass_color, (int(x), int(ground_y - size // 2)), size)
            pygame.draw.circle(screen, tuple(max(0,c-20) for c in grass_color), (int(x), int(ground_y - size // 2)), int(size*0.7))


# --- Dinosaur ---
class Dinosaur:
    """恐龙玩家类 - Player dinosaur class (Enhanced Pixel Art Style) / 恐龙玩家类 - 玩家恐龙类 (增强像素艺术风格)"""

    def __init__(self, x, y, audio_manager):
        """初始化恐龙 / Initialize the dinosaur"""
        self.x = x
        self.base_y = y # Store base y for landing / 存储基础y坐标用于着陆
        self.y = y
        self.width = 44  # Pixel art dimensions / 像素艺术尺寸
        self.height = 56 # Pixel art dimensions / 像素艺术尺寸
        self.velocity_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.original_height = self.height
        self.duck_height = 28 # Pixel art ducking height / 像素艺术下蹲高度

        self.audio_manager = audio_manager

        # 动画相关 / Animation related
        self.run_animation_timer = 0
        self.run_frame_count = 4 # Number of running frames / 跑步动画帧数
        self.run_frame_duration = 6 # How many game ticks per animation frame / 每动画帧的游戏刻度数
        self.run_frame = 0
        self.jump_stretch = 0  # 跳跃拉伸效果 / Jump stretch effect

        # 无敌状态 / Invincibility state
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 180 # 3 seconds at 60 FPS / 60帧/秒情况下持续3秒

        # 状态 / States
        self.is_hurt = False # For visual feedback when hit but not game over / 用于被击中但未游戏结束时的视觉反馈
        self.hurt_timer = 0
        self.hurt_duration = 30 # How long hurt visual lasts / 受伤视觉效果持续时间

    def jump(self):
        """恐龙跳跃 / Make dinosaur jump"""
        if not self.is_jumping and not self.is_ducking:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            self.jump_stretch = 6  # 起跳拉伸效果 / Jump stretch effect (positive for stretch up)
            self.audio_manager.play_sound('jump')

    def duck(self):
        """恐龙下蹲 / Make dinosaur duck"""
        if not self.is_jumping and not self.is_ducking: # Can only duck if not already ducking / 仅当未下蹲时才能下蹲
            self.is_ducking = True
            self.height = self.duck_height
            self.y = self.base_y + (self.original_height - self.duck_height) # Adjust y to keep feet on ground / 调整y坐标以使脚保持在地面上
            # self.audio_manager.play_sound('duck') # Play sound when ducking starts / 下蹲开始时播放声音

    def stop_duck(self):
        """停止下蹲 / Stop ducking"""
        if self.is_ducking : # Can only stop ducking if currently ducking / 仅当当前正在下蹲时才能停止下蹲
            self.is_ducking = False
            self.height = self.original_height
            self.y = self.base_y # Reset to original y / 重置为原始y坐标

    def make_invincible(self, duration=None):
        """设置无敌状态 / Set invincible state"""
        self.invincible = True
        self.invincible_timer = duration if duration is not None else self.invincible_duration
        # self.audio_manager.play_sound('powerup') # Or a specific invincible sound / 或特定的无敌音效

    def take_damage(self):
        """受到伤害时的视觉反馈 / Visual feedback for taking damage"""
        if not self.invincible: # Should only take damage if not invincible / 仅当非无敌状态时才会受到伤害
            self.is_hurt = True
            self.hurt_timer = self.hurt_duration
            # self.audio_manager.play_sound('hit') # This sound might be better handled in Game class upon life loss / 此声音可能在Game类中处理生命值减少时更好

    def update(self):
        """更新恐龙状态 / Update dinosaur state"""
        # 更新跳跃物理 / Update jump physics
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.y += self.velocity_y

            ground_y = self.base_y # Dinosaur's feet should land on base_y / 恐龙的脚应该落在 base_y 上
            if self.y >= ground_y:
                self.y = ground_y
                self.velocity_y = 0
                self.is_jumping = False
                self.jump_stretch = -4  # 落地压缩效果 / Landing compression effect (negative for squash)
                self.audio_manager.play_sound('land')

        # 更新跑步动画 (only if not jumping and not ducking, or handle ducking animation separately)
        # 更新跑步动画 (仅当未跳跃且未下蹲时，或单独处理下蹲动画)
        if not self.is_jumping and not self.is_ducking:
            self.run_animation_timer += 1
            if self.run_animation_timer >= self.run_frame_duration:
                self.run_frame = (self.run_frame + 1) % self.run_frame_count
                self.run_animation_timer = 0
        elif self.is_ducking:
            # Potentially a different animation timer/frame for ducking if needed
            # 如果需要，可以为下蹲设置不同的动画计时器/帧
            self.run_animation_timer +=1
            if self.run_animation_timer >= self.run_frame_duration * 1.5: # Slower animation when ducking / 下蹲时动画较慢
                self.run_frame = (self.run_frame +1) % 2 # Simpler 2-frame ducking slide / 更简单的2帧下蹲滑动动画
                self.run_animation_timer = 0


        # 更新拉伸/压缩效果 / Update stretch/squash effect
        if self.jump_stretch > 0:
            self.jump_stretch -= 0.5
            if self.jump_stretch < 0: self.jump_stretch = 0
        elif self.jump_stretch < 0:
            self.jump_stretch += 0.5
            if self.jump_stretch > 0: self.jump_stretch = 0

        # 更新无敌状态 / Update invincibility state
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # 更新受伤状态 / Update hurt state
        if self.is_hurt:
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.is_hurt = False

    def get_rect(self):
        """获取恐龙的碰撞矩形 / Get dinosaur collision rectangle"""
        # Adjust hitbox to be slightly smaller than visual sprite for fairness
        # 调整碰撞框使其略小于视觉精灵图以确保公平
        margin_x = 6
        margin_y = 4
        current_y = self.y if not self.is_ducking else self.base_y + (self.original_height - self.duck_height)
        current_height = self.height if self.is_ducking else self.original_height

        return pygame.Rect(self.x + margin_x, current_y + margin_y,
                           self.width - margin_x * 2, current_height - margin_y * 2)

    def draw(self, screen):
        """绘制恐龙 (像素艺术风格) / Draw the dinosaur (Pixel Art Style)"""
        # 无敌时闪烁效果 / Blinking effect when invincible
        if self.invincible and (self.invincible_timer // 6 % 2 == 0) : # Blink every 6 frames / 每6帧闪烁一次
            return

        # 确定颜色 / Determine color
        if self.is_hurt and (self.hurt_timer // 4 % 2 == 0): # Hurt blink / 受伤闪烁
            body_color = RED
        elif self.invincible:
            body_color = BLUE # Or a cycling rainbow color for invincibility / 或使用循环彩虹色表示无敌
        else:
            body_color = DARK_GREEN

        eye_color = WHITE
        pupil_color = BLACK

        # 应用拉伸/压缩效果 (adjust y and height based on jump_stretch)
        # Positive jump_stretch means stretching upwards (y decreases, height increases)
        # Negative jump_stretch means squashing downwards (y increases slightly, height decreases)
        # 应用拉伸/压缩效果 (根据 jump_stretch 调整y和高度)
        # 正的 jump_stretch 表示向上拉伸 (y减少，高度增加)
        # 负的 jump_stretch 表示向下压缩 (y略微增加，高度减少)
        visual_y = self.y - self.jump_stretch
        visual_height = self.height + abs(self.jump_stretch) if self.is_ducking else self.original_height + abs(self.jump_stretch)
        if self.is_ducking:
            visual_y = self.base_y + (self.original_height - self.duck_height) - self.jump_stretch


        # --- PIXEL ART DRAWING LOGIC ---
        # This is a placeholder. For true pixel art, you would blit pre-drawn sprite frames.
        # We'll use pygame.draw.rect to simulate a blocky, pixelated look.
        # All coordinates are relative to self.x, visual_y
        # --- 像素艺术绘制逻辑 ---
        # 这是一个占位符。对于真正的像素艺术，你会blit预先绘制的精灵帧。
        # 我们将使用 pygame.draw.rect 来模拟块状、像素化的外观。
        # 所有坐标都相对于 self.x, visual_y

        if self.is_ducking:
            # Ducking Pose (example pixel art)
            # 下蹲姿势 (像素艺术示例)
            # Body / 身体
            pygame.draw.rect(screen, body_color, (self.x, visual_y, self.width, visual_height)) # Main low body / 主要的低矮身体
            # Head part / 头部
            pygame.draw.rect(screen, body_color, (self.x + self.width - 16, visual_y + 4, 16, 16))
            # Eye / 眼睛
            pygame.draw.rect(screen, eye_color, (self.x + self.width - 8, visual_y + 8, 4, 2)) # Squinting eye / 眯着的眼睛
            pygame.draw.rect(screen, pupil_color, (self.x + self.width - 7, visual_y + 8, 2, 2))
        else:
            # Running/Jumping Pose (example pixel art - needs multiple frames for animation)
            # 跑步/跳跃姿势 (像素艺术示例 - 需要多帧动画)
            # Frame 0 (Standing-ish or one run frame) / 帧 0 (类似站立或一帧跑步)
            if self.run_frame == 0 or self.is_jumping:
                pygame.draw.rect(screen, body_color, (self.x + 4, visual_y + 12, 36, visual_height - 20)) # Torso / 躯干
                pygame.draw.rect(screen, body_color, (self.x + 28, visual_y, 16, 24)) # Head / 头部
                pygame.draw.rect(screen, eye_color, (self.x + 36, visual_y + 6, 4, 4)) # Eye / 眼睛
                pygame.draw.rect(screen, pupil_color, (self.x + 38, visual_y + 7, 2, 2)) # Pupil / 瞳孔
                pygame.draw.rect(screen, body_color, (self.x, visual_y + 28, 12, 12)) # Tail / 尾巴
                # Legs / 腿
                pygame.draw.rect(screen, body_color, (self.x + 12, visual_y + visual_height - 16, 8, 16)) # Back Leg / 后腿
                pygame.draw.rect(screen, body_color, (self.x + 24, visual_y + visual_height - 12, 8, 12)) # Front Leg / 前腿
            # Frame 1 (Other run frame) / 帧 1 (另一帧跑步)
            elif self.run_frame == 1:
                pygame.draw.rect(screen, body_color, (self.x + 4, visual_y + 12, 36, visual_height - 20))
                pygame.draw.rect(screen, body_color, (self.x + 28, visual_y, 16, 24))
                pygame.draw.rect(screen, eye_color, (self.x + 36, visual_y + 6, 4, 4))
                pygame.draw.rect(screen, pupil_color, (self.x + 38, visual_y + 7, 2, 2))
                pygame.draw.rect(screen, body_color, (self.x, visual_y + 28, 12, 10)) # Tail slightly up / 尾巴略微向上
                # Legs / 腿
                pygame.draw.rect(screen, body_color, (self.x + 10, visual_y + visual_height - 12, 8, 12))
                pygame.draw.rect(screen, body_color, (self.x + 26, visual_y + visual_height - 16, 8, 16))
            # Frame 2 / 帧 2
            elif self.run_frame == 2:
                pygame.draw.rect(screen, body_color, (self.x + 4, visual_y + 12, 36, visual_height - 20))
                pygame.draw.rect(screen, body_color, (self.x + 28, visual_y, 16, 24))
                pygame.draw.rect(screen, eye_color, (self.x + 36, visual_y + 6, 4, 4))
                pygame.draw.rect(screen, pupil_color, (self.x + 38, visual_y + 7, 2, 2))
                pygame.draw.rect(screen, body_color, (self.x, visual_y + 26, 12, 12)) # Tail / 尾巴
                # Legs / 腿
                pygame.draw.rect(screen, body_color, (self.x + 12, visual_y + visual_height - 16, 8, 16))
                pygame.draw.rect(screen, body_color, (self.x + 24, visual_y + visual_height - 10, 8, 10))
            # Frame 3 / 帧 3
            elif self.run_frame == 3:
                pygame.draw.rect(screen, body_color, (self.x + 4, visual_y + 12, 36, visual_height - 20))
                pygame.draw.rect(screen, body_color, (self.x + 28, visual_y, 16, 24))
                pygame.draw.rect(screen, eye_color, (self.x + 36, visual_y + 6, 4, 4))
                pygame.draw.rect(screen, pupil_color, (self.x + 38, visual_y + 7, 2, 2))
                pygame.draw.rect(screen, body_color, (self.x, visual_y + 28, 12, 10)) # Tail slightly up / 尾巴略微向上
                # Legs / 腿
                pygame.draw.rect(screen, body_color, (self.x + 10, visual_y + visual_height - 10, 8, 10))
                pygame.draw.rect(screen, body_color, (self.x + 26, visual_y + visual_height - 16, 8, 16))

            # Small arm (pixel art style) / 小手臂 (像素艺术风格)
            pygame.draw.rect(screen, body_color, (self.x + 26, visual_y + 20, 6, 6))

        # If hurt and not invincible, draw X over eyes (or modify eye drawing)
        # 如果受伤且非无敌状态，在眼睛上画X (或修改眼睛绘制)
        if self.is_hurt and not self.invincible:
            pygame.draw.line(screen, BLACK, (self.x + 36 - 2, visual_y + 6 - 1), (self.x + 36 + 2, visual_y + 6 + 3), 2)
            pygame.draw.line(screen, BLACK, (self.x + 36 + 2, visual_y + 6 - 1), (self.x + 36 - 2, visual_y + 6 + 3), 2)


# --- Fireball ---
class Fireball:
    """火球类 / Fireball class (Enhanced with trail and particles) / 火球类 (增强了轨迹和粒子效果)"""

    def __init__(self, x, y, audio_manager, particle_system):
        """初始化火球 / Initialize fireball"""
        self.x = x
        self.y = y
        self.width = 18 # Slightly larger for pixel art / 像素艺术略大一些
        self.height = 10
        self.speed = 15
        self.active = True
        self.animation_timer = 0
        self.trail_positions = []  # 火球轨迹 / Fireball trail
        self.audio_manager = audio_manager
        self.particle_system = particle_system
        self.audio_manager.play_sound('fireball')

    def update(self):
        """更新火球状态 / Update fireball state"""
        # 记录轨迹位置 / Record trail positions
        self.trail_positions.append((self.x + self.width // 2, self.y + self.height // 2))
        if len(self.trail_positions) > 6: # Shorter trail for pixel art / 像素艺术的轨迹较短
            self.trail_positions.pop(0)

        self.x += self.speed
        self.animation_timer += 1

        if self.x > WINDOW_WIDTH + 50: # Give some margin before deactivating / 在停用前留出一些边距
            self.active = False

    def get_rect(self):
        """获取火球的碰撞矩形 / Get fireball collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """绘制火球 (像素艺术风格) / Draw the fireball (Pixel Art Style)"""
        if not self.active:
            return

        # 绘制火球轨迹 (simple pixel trail) / 绘制火球轨迹 (简单像素轨迹)
        for i, (trail_x, trail_y) in enumerate(self.trail_positions):
            alpha = int(150 * (i / len(self.trail_positions))) # Fade out / 淡出
            trail_size = max(1, int((self.width // 3) * (i / len(self.trail_positions))))

            trail_color_base = ORANGE
            if i < len(self.trail_positions) / 2 :
                trail_color_base = RED

            # For pixel art, draw small rects or circles
            # 对于像素艺术，绘制小矩形或圆形
            pygame.draw.rect(screen, (*trail_color_base, alpha) if pygame.Surface.get_flags(screen) & pygame.SRCALPHA else trail_color_base,
                             (int(trail_x - trail_size//2), int(trail_y - trail_size//2), trail_size, trail_size))


        # 火球核心 (Pixel art style - layered rects/circles)
        # 火球核心 (像素艺术风格 - 分层矩形/圆形)
        # Outer flame (Reddish orange) / 外层火焰 (红橙色)
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # Mid flame (Orange) / 中层火焰 (橙色)
        pygame.draw.rect(screen, ORANGE, (self.x + 2, self.y + 2, self.width - 4, self.height - 4))
        # Core (Yellow) / 核心 (黄色)
        pygame.draw.rect(screen, YELLOW, (self.x + 4, self.y + 4, self.width - 8, self.height - 8))
        # Highlight (White) / 高光 (白色)
        pygame.draw.rect(screen, WHITE, (self.x + 6, self.y + 5, self.width - 12, self.height - 10))


# --- Obstacle Base Class ---
class Obstacle:
    """障碍物基类 / Base obstacle class"""

    def __init__(self, x, y, width, height, obstacle_type, particle_system, audio_manager):
        """初始化障碍物 / Initialize obstacle"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = obstacle_type
        # self.speed = GAME_SPEED # Speed will be passed in update / 速度将在 update 中传递
        self.active = True
        self.can_be_destroyed_by_fireball = True # Default, can be overridden / 默认值，可以被覆盖
        self.particle_system = particle_system
        self.audio_manager = audio_manager

    def update(self, game_speed):
        """更新障碍物位置 / Update obstacle position"""
        self.x -= game_speed
        if self.x + self.width < 0: # If obstacle is off-screen to the left / 如果障碍物移出屏幕左侧
            self.active = False

    def get_rect(self):
        """获取障碍物的碰撞矩形 / Get obstacle collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def on_destroy(self):
        """障碍物被摧毁时的效果 / Effect when obstacle is destroyed"""
        self.active = False
        # Add destruction particles (e.g., green for cactus, purple for pterodactyl)
        # 添加销毁粒子 (例如，仙人掌为绿色，翼龙为紫色)
        destroy_color = GREEN if self.type == "cactus" else PURPLE if self.type == "pterodactyl" else GRAY
        self.particle_system.add_explosion(self.x + self.width // 2, self.y + self.height // 2, color=destroy_color)
        self.audio_manager.play_sound('destroy')

    def draw(self, screen):
        """绘制障碍物 (由子类实现) / Draw the obstacle (Implemented by subclasses)"""
        pass

# --- Cactus Obstacle ---
class Cactus(Obstacle):
    """仙人掌障碍物类 (像素艺术风格) / Cactus obstacle class (Pixel Art Style)"""

    def __init__(self, x, particle_system, audio_manager):
        """初始化仙人掌 / Initialize cactus"""
        # Randomly choose cactus type (single, double, triple small, etc.)
        # 随机选择仙人掌类型 (单个、双个、三个小型等)
        self.cactus_type = random.randint(0, 2)

        base_y = WINDOW_HEIGHT - GROUND_HEIGHT
        if self.cactus_type == 0: # Single tall cactus / 单个高仙人掌
            width, height = 20, 50
        elif self.cactus_type == 1: # Two medium cacti / 两个中等仙人掌
            width, height = 45, 35 # Total width for two / 两个的总宽度
        else: # Three small cacti / 三个小仙人掌
            width, height = 60, 25 # Total width for three / 三个的总宽度

        super().__init__(x, base_y - height, width, height, "cactus", particle_system, audio_manager)

    def draw(self, screen):
        """绘制仙人掌 (像素艺术风格) / Draw the cactus (Pixel Art Style)"""
        if not self.active:
            return

        # Main cactus color / 主要仙人掌颜色
        cactus_color = GREEN
        darker_cactus_color = DARK_GREEN

        if self.cactus_type == 0: # Single tall cactus / 单个高仙人掌
            # Body / 身体
            pygame.draw.rect(screen, cactus_color, (self.x + 4, self.y, self.width - 8, self.height))
            # Arms / 手臂
            pygame.draw.rect(screen, cactus_color, (self.x, self.y + 10, 4, 15))
            pygame.draw.rect(screen, cactus_color, (self.x + self.width - 4, self.y + 15, 4, 15))
            # Highlights/details / 高光/细节
            pygame.draw.rect(screen, darker_cactus_color, (self.x + 6, self.y + 2, self.width - 12, 4))


        elif self.cactus_type == 1: # Two medium cacti / 两个中等仙人掌
            # Cactus 1 / 仙人掌 1
            pygame.draw.rect(screen, cactus_color, (self.x, self.y, 20, self.height))
            pygame.draw.rect(screen, cactus_color, (self.x - 3, self.y + 8, 6, 10))
            pygame.draw.rect(screen, darker_cactus_color, (self.x + 2, self.y + 2, 16, 3))
            # Cactus 2 (offset to the right) / 仙人掌 2 (向右偏移)
            pygame.draw.rect(screen, cactus_color, (self.x + 25, self.y + 5, 20, self.height - 5)) # Slightly shorter / 略短
            pygame.draw.rect(screen, cactus_color, (self.x + 25 + 17, self.y + 12, 6, 10))
            pygame.draw.rect(screen, darker_cactus_color, (self.x + 27, self.y + 7, 16, 3))


        else: # Three small cacti / 三个小仙人掌
            spacing = 2
            single_width = (self.width - spacing * 2) // 3
            for i in range(3):
                current_x = self.x + i * (single_width + spacing)
                pygame.draw.rect(screen, cactus_color, (current_x, self.y, single_width, self.height))
                pygame.draw.rect(screen, darker_cactus_color, (current_x + 1, self.y + 1, single_width - 2, 3))


# --- Pterodactyl Obstacle ---
class Pterodactyl(Obstacle):
    """翼龙障碍物类 (像素艺术风格) / Pterodactyl obstacle class (Pixel Art Style)"""

    def __init__(self, x, particle_system, audio_manager):
        """初始化翼龙 / Initialize pterodactyl"""
        # Random height level for pterodactyl
        # 翼龙的随机高度级别
        height_options = [
            WINDOW_HEIGHT - GROUND_HEIGHT - 70,  # Low / 低
            WINDOW_HEIGHT - GROUND_HEIGHT - 100, # Mid / 中
            WINDOW_HEIGHT - GROUND_HEIGHT - 35,  # Very low (duckable) / 非常低 (可下蹲躲避)
        ]
        pter_y = random.choice(height_options)
        self.width_sprite = 48 # Pixel art dimensions / 像素艺术尺寸
        self.height_sprite = 24
        super().__init__(x, pter_y - self.height_sprite, self.width_sprite, self.height_sprite, "pterodactyl", particle_system, audio_manager)

        self.wing_animation_timer = 0
        self.wing_frame = 0
        self.wing_frame_duration = 8 # Ticks per wing frame / 每翼帧的刻度数
        self.can_be_destroyed_by_fireball = True # Pterodactyls can be shot down / 翼龙可以被击落

    def update(self, game_speed):
        """更新翼龙状态 / Update pterodactyl state"""
        super().update(game_speed)
        self.wing_animation_timer += 1
        if self.wing_animation_timer >= self.wing_frame_duration:
            self.wing_frame = (self.wing_frame + 1) % 2 # 2-frame wing animation / 2帧翅膀动画
            self.wing_animation_timer = 0

    def draw(self, screen):
        """绘制翼龙 (像素艺术风格) / Draw the pterodactyl (Pixel Art Style)"""
        if not self.active:
            return

        body_color = PURPLE
        wing_color = GRAY
        darker_purple = (90,0,150)

        # Body / 身体
        pygame.draw.rect(screen, body_color, (self.x + 8, self.y + 8, self.width_sprite - 24, 12)) # Main body / 主体
        # Head / 头部
        pygame.draw.rect(screen, body_color, (self.x + self.width_sprite - 20, self.y + 4, 16, 8)) # Head / 头部
        pygame.draw.rect(screen, darker_purple, (self.x + self.width_sprite - 8, self.y + 6, 4, 4)) # Beak/Eye area / 喙/眼睛区域

        # Wings (2-frame animation) / 翅膀 (2帧动画)
        if self.wing_frame == 0: # Wings up / 翅膀向上
            pygame.draw.polygon(screen, wing_color, [
                (self.x, self.y + 10), (self.x + 20, self.y), (self.x + 20, self.y + 8)
            ]) # Left wing / 左翼
            pygame.draw.polygon(screen, wing_color, [
                (self.x + self.width_sprite - 20, self.y), (self.x + self.width_sprite, self.y + 10), (self.x + self.width_sprite - 20, self.y + 8)
            ]) # Right wing / 右翼
        else: # Wings down / 翅膀向下
            pygame.draw.polygon(screen, wing_color, [
                (self.x, self.y + 4), (self.x + 20, self.y + 14), (self.x + 20, self.y + 6)
            ]) # Left wing / 左翼
            pygame.draw.polygon(screen, wing_color, [
                (self.x + self.width_sprite - 20, self.y + 14), (self.x + self.width_sprite, self.y + 4), (self.x + self.width_sprite - 20, self.y + 6)
            ]) # Right wing / 右翼

# --- PowerUp Class ---
class PowerUp:
    """道具类 (像素艺术风格) / Power-up class (Pixel Art Style)"""
    game_instance = None # Class variable to hold the game instance / 类变量，用于保存游戏实例

    def __init__(self, x, powerup_type, particle_system, audio_manager):
        """初始化道具 / Initialize power-up"""
        self.x = x
        self.base_y = WINDOW_HEIGHT - GROUND_HEIGHT - 30 # Base height for power-ups / 道具的基础高度
        self.y = self.base_y
        self.width = 24 # Pixel art dimensions / 像素艺术尺寸
        self.height = 24
        self.type = powerup_type
        self.active = True
        self.animation_timer = 0 # For floating effect and glow / 用于浮动效果和发光
        self.particle_system = particle_system
        self.audio_manager = audio_manager

        self.effects_config = {
            "life": {"color": RED, "symbol_char": "♥", "glow_color": (255,100,100)},
            "invincible": {"color": BLUE, "symbol_char": "★", "glow_color": (100,100,255)},
            "score": {"color": YELLOW, "symbol_char": "◆", "glow_color": (255,255,100)}
        }
        self.config = self.effects_config[self.type]

    def update(self, game_speed):
        """更新道具状态 / Update power-up state"""
        self.x -= game_speed
        self.animation_timer += 0.1
        self.y = self.base_y + math.sin(self.animation_timer * 2) * 5 # Floating effect / 浮动效果

        if self.x + self.width < 0:
            self.active = False

    def get_rect(self):
        """获取道具的碰撞矩形 / Get power-up collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def on_pickup(self):
        """道具被拾取时的效果 / Effect when power-up is picked up"""
        self.active = False
        self.particle_system.add_pickup_effect(self.x + self.width // 2, self.y + self.height // 2, color=self.config["color"])
        self.audio_manager.play_sound('powerup')

    def draw(self, screen):
        """绘制道具 (像素艺术风格) / Draw the power-up (Pixel Art Style)"""
        if not self.active:
            return

        # Pulsating glow effect / 脉动发光效果
        glow_alpha = 100 + math.sin(self.animation_timer * 3) * 50
        glow_radius = self.width // 2 + 4 + math.sin(self.animation_timer * 3) * 2

        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*self.config["glow_color"], int(glow_alpha)),
                           (glow_radius, glow_radius), int(glow_radius))
        screen.blit(glow_surface, (int(self.x + self.width//2 - glow_radius), int(self.y + self.height//2 - glow_radius)))

        # Main Power-up body (pixel art - simple rect for now, can be replaced by sprite)
        # 主要道具主体 (像素艺术 - 目前为简单矩形，可替换为精灵图)
        pygame.draw.rect(screen, self.config["color"], (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, tuple(max(0,c-50) for c in self.config["color"]), (self.x+2, self.y+2, self.width-4, self.height-4)) # Inner shadow / 内部阴影

        # Symbol (using a simple font for the symbol character)
        # 符号 (使用简单字体显示符号字符)
        symbol_font_size = int(self.height * 0.7)
        symbol_font_to_use = None

        if PowerUp.game_instance and hasattr(PowerUp.game_instance, 'ui_font'):
            # Try to use a scaled version of the game's UI font if it's not too small
            # 如果游戏的UI字体不太小，则尝试使用其缩放版本
            # This is a heuristic; direct use or specific symbol font might be better
            # 这是一种启发式方法；直接使用或特定的符号字体可能更好
            if PowerUp.game_instance.ui_font.get_height() >= symbol_font_size * 0.8: # Check if base size is reasonable
                 try:
                     # Attempt to create a new font object with desired size from the game's font if path is known or it's a SysFont
                     # This part is tricky if game_instance.ui_font is from a file path not easily accessible here
                     # For simplicity, we'll use a new font object for the symbol if game's ui_font is not directly suitable.
                     # Pygame font objects don't have a 'name' or 'path' attribute easily, so recreating is safer.
                     symbol_font_to_use = pygame.font.Font(None, symbol_font_size) # Defaulting to new font for symbol
                 except:
                     symbol_font_to_use = pygame.font.Font(None, symbol_font_size) # Fallback
            else:
                 symbol_font_to_use = pygame.font.Font(None, symbol_font_size)
        else:
            symbol_font_to_use = pygame.font.Font(None, symbol_font_size) # Fallback if game_instance or ui_font not available

        if symbol_font_to_use is None: # Final fallback
            symbol_font_to_use = pygame.font.SysFont("sans", symbol_font_size)


        symbol_surface = symbol_font_to_use.render(self.config["symbol_char"], True, WHITE)
        symbol_rect = symbol_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(symbol_surface, symbol_rect)


# --- Game Class ---
class Game:
    """游戏主类 / Main game class"""

    def __init__(self):
        """初始化游戏 / Initialize the game"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.audio_manager = AudioManager()
        self.particle_system = ParticleSystem()
        self.background = Background(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.dinosaur = Dinosaur(70, WINDOW_HEIGHT - GROUND_HEIGHT - 56, self.audio_manager)

        self.obstacles = []
        self.fireballs = []
        self.powerups = []

        self.score = 0
        self.high_score = self.load_high_score()
        self.lives = 3
        self.game_speed = GAME_SPEED
        self.game_over = False
        self.paused = False

        self.obstacle_timer = 0
        self.obstacle_spawn_interval = 100
        self.powerup_timer = 0
        self.powerup_spawn_interval = random.randint(400, 800)

        self.keys_pressed_this_frame = set()
        self.keys_held = set()

        self.load_fonts()
        self.update_caption()
        self.clock = pygame.time.Clock()
        self.audio_manager.play_music()
        PowerUp.game_instance = self # Make game instance available to PowerUp class

    def update_caption(self):
        """更新窗口标题 / Update window caption"""
        pygame.display.set_caption(get_text("caption"))

    def load_fonts(self):
        """加载字体 / Load fonts"""
        font_path_pixel = "assets/fonts/PressStart2P-Regular.ttf"
        pixel_font_exists = os.path.exists(font_path_pixel)

        # --- 请在这里替换为您下载的中文字体文件名 ---
        # --- Please replace with your downloaded Chinese font filename here ---
        user_chinese_font_filename = "Microsoft_YaHei_Bold.ttf"  # 例如: "MaShanZheng-Regular.ttf"
        # 确保此字体文件放在 "assets/fonts/" 文件夹中
        # Make sure this font file is placed in the "assets/fonts/" folder
        font_path_user_cn = os.path.join("assets", "fonts", user_chinese_font_filename)


        score_size_default = 24
        ui_size_default = 18
        large_size_default = 48

        score_size_cjk_fallback = 30
        ui_size_cjk_fallback = 22
        large_size_cjk_fallback = 60

        if current_language == "CN":
            font_loaded_cn = False
            if os.path.exists(font_path_user_cn): # 检查用户提供的中文字体是否存在
                try:
                    self.score_font = pygame.font.Font(font_path_user_cn, score_size_default)
                    self.ui_font = pygame.font.Font(font_path_user_cn, ui_size_default)
                    self.large_font = pygame.font.Font(font_path_user_cn, large_size_default)
                    print(get_text("user_chinese_font_success").format(font_path=font_path_user_cn))
                    font_loaded_cn = True
                except pygame.error as e:
                    print(get_text("user_chinese_font_error").format(font_path=font_path_user_cn, error=e))
                    # If user font fails, font_loaded_cn remains False, will try system fonts

            if not font_loaded_cn:
                # 如果用户字体加载失败或不存在，则尝试系统字体
                cn_font_names_to_try = ["SimHei", "Microsoft YaHei", "WenQuanYi Zen Hei", "Noto Sans CJK SC"]
                system_font_loaded = False
                for font_name in cn_font_names_to_try:
                    try:
                        self.score_font = pygame.font.SysFont(font_name, score_size_default)
                        self.ui_font = pygame.font.SysFont(font_name, ui_size_default)
                        self.large_font = pygame.font.SysFont(font_name, large_size_default)
                        print(get_text("chinese_font_success").format(font_name=font_name))
                        system_font_loaded = True
                        break
                    except pygame.error:
                        continue

                if not system_font_loaded:
                    print(get_text("chinese_font_system_warning").format(font_names=", ".join(cn_font_names_to_try)))
                    self.score_font = pygame.font.Font(None, score_size_cjk_fallback)
                    self.ui_font = pygame.font.Font(None, ui_size_cjk_fallback)
                    self.large_font = pygame.font.Font(None, large_size_cjk_fallback)
        else:
            if pixel_font_exists:
                try:
                    self.score_font = pygame.font.Font(font_path_pixel, score_size_default)
                    self.ui_font = pygame.font.Font(font_path_pixel, ui_size_default)
                    self.large_font = pygame.font.Font(font_path_pixel, large_size_default)
                    print(get_text("font_loaded_success").format(font_name="PressStart2P-Regular.ttf"))
                except pygame.error as e:
                    print(f"{get_text('font_load_warning_specific').format(font_name='PressStart2P-Regular.ttf')} ({e})")
                    self.score_font = pygame.font.Font(None, score_size_cjk_fallback)
                    self.ui_font = pygame.font.Font(None, ui_size_cjk_fallback)
                    self.large_font = pygame.font.Font(None, large_size_cjk_fallback)
            else:
                print(get_text('font_load_warning_missing').format(font_name='PressStart2P-Regular.ttf'))
                self.score_font = pygame.font.Font(None, score_size_cjk_fallback)
                self.ui_font = pygame.font.Font(None, ui_size_cjk_fallback)
                self.large_font = pygame.font.Font(None, large_size_cjk_fallback)


    def load_high_score(self):
        """加载最高分 / Load high score"""
        try:
            if os.path.exists("highscore.txt"):
                with open("highscore.txt", "r") as f:
                    return int(f.read())
        except (IOError, ValueError):
            pass
        return 0

    def save_high_score(self):
        """保存最高分 / Save high score"""
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))
        except IOError:
            print(get_text("save_highscore_warning"))

    def spawn_obstacle(self):
        """生成障碍物 / Spawn obstacles"""
        if random.random() < 0.7:
            self.obstacles.append(Cactus(WINDOW_WIDTH, self.particle_system, self.audio_manager))
        else:
            self.obstacles.append(Pterodactyl(WINDOW_WIDTH, self.particle_system, self.audio_manager))
        self.obstacle_spawn_interval = max(30, 120 - int(self.game_speed * 3) - self.score // 1000)


    def spawn_powerup(self):
        """生成道具 / Spawn power-ups"""
        powerup_type = random.choice(["life", "invincible", "score"])
        self.powerups.append(PowerUp(WINDOW_WIDTH, powerup_type, self.particle_system, self.audio_manager))
        self.powerup_spawn_interval = random.randint(500, 1000)

    def shoot_fireball(self):
        """恐龙发射火球 / Dinosaur shoots fireball"""
        if not self.dinosaur.is_ducking:
            fireball_x = self.dinosaur.x + self.dinosaur.width -10
            fireball_y = self.dinosaur.y + self.dinosaur.height // 3
            self.fireballs.append(Fireball(fireball_x, fireball_y, self.audio_manager, self.particle_system))

    def check_collisions(self):
        """检查碰撞 / Check collisions"""
        dino_rect = self.dinosaur.get_rect()

        if not self.dinosaur.invincible:
            for obstacle in self.obstacles:
                if obstacle.active and dino_rect.colliderect(obstacle.get_rect()):
                    self.dinosaur.take_damage()
                    self.audio_manager.play_sound('hit')
                    self.lives -= 1
                    obstacle.active = False
                    self.particle_system.add_explosion(obstacle.x + obstacle.width//2, obstacle.y + obstacle.height//2, RED, count=5)
                    if self.lives <= 0:
                        self.game_over = True
                        self.audio_manager.play_sound('game_over')
                        self.audio_manager.stop_music()
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self.save_high_score()
                    else:
                        self.dinosaur.make_invincible(duration=90)
                    break

        for fireball in self.fireballs[:]:
            if not fireball.active: continue
            fireball_rect = fireball.get_rect()
            for obstacle in self.obstacles[:]:
                if obstacle.active and obstacle.can_be_destroyed_by_fireball and fireball_rect.colliderect(obstacle.get_rect()):
                    obstacle.on_destroy()
                    fireball.active = False
                    self.score += 50
                    break

        for powerup in self.powerups[:]:
            if powerup.active and dino_rect.colliderect(powerup.get_rect()):
                self.apply_powerup_effect(powerup.type)
                powerup.on_pickup()

    def apply_powerup_effect(self, powerup_type):
        """应用道具效果 / Apply power-up effects"""
        if powerup_type == "life":
            self.lives = min(5, self.lives + 1)
        elif powerup_type == "invincible":
            self.dinosaur.make_invincible()
        elif powerup_type == "score":
            self.score += 200

    def handle_input(self):
        """处理输入 / Handle input"""
        global current_language
        self.keys_pressed_this_frame.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                self.keys_pressed_this_frame.add(event.key)
                self.keys_held.add(event.key)

                if event.key == pygame.K_p:
                    self.paused = not self.paused # 首先切换暂停状态 / Toggle pause state first

                    if self.paused: # 如果游戏刚刚被暂停 / If game has just been paused
                        if pygame.mixer.get_init() and self.audio_manager.music_playing:
                           pygame.mixer.music.pause() # 暂停背景音乐 / Pause background music
                        self.audio_manager.play_sound('pause') # 仅在暂停时播放音效 / Play sound only when pausing
                    else: # 如果游戏刚刚被恢复 / If game has just been resumed
                        if pygame.mixer.get_init() and self.audio_manager.music_playing:
                           pygame.mixer.music.unpause() # 恢复背景音乐 / Unpause background music
                        self.audio_manager.stop_sound('pause') # 显式停止暂停音效 / Explicitly stop the pause sound

                elif event.key == pygame.K_l:
                    current_language = "CN" if current_language == "EN" else "EN"
                    self.load_fonts()
                    self.update_caption()
                    self.print_instructions()


                if self.game_over:
                    if event.key == pygame.K_r:
                        self.restart_game()
                elif not self.paused:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.dinosaur.jump()
                    elif event.key == pygame.K_x:
                        self.shoot_fireball()

            if event.type == pygame.KEYUP:
                self.keys_held.discard(event.key)

        if not self.game_over and not self.paused:
            if pygame.K_DOWN in self.keys_held or pygame.K_s in self.keys_held:
                self.dinosaur.duck()
            else:
                self.dinosaur.stop_duck()

        return True

    def update(self):
        """更新游戏状态 / Update game state"""
        if self.game_over or self.paused:
            self.particle_system.update()
            return

        self.game_speed += SPEED_INCREASE
        self.score += 1

        self.background.update(self.game_speed)
        self.dinosaur.update()
        self.particle_system.update()

        for fireball in self.fireballs[:]:
            fireball.update()
            if not fireball.active: self.fireballs.remove(fireball)

        for obstacle in self.obstacles[:]:
            obstacle.update(self.game_speed)
            if not obstacle.active: self.obstacles.remove(obstacle)

        for powerup in self.powerups[:]:
            powerup.update(self.game_speed)
            if not powerup.active: self.powerups.remove(powerup)

        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_spawn_interval:
            self.spawn_obstacle()
            self.obstacle_timer = 0

        self.powerup_timer +=1
        if self.powerup_timer >= self.powerup_spawn_interval:
            if random.random() < 0.4:
                self.spawn_powerup()
            self.powerup_timer = 0

        self.check_collisions()

    def draw_text(self, text, font, color, x, y, align="topleft"):
        """Helper to draw text with different alignments."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "topleft":
            text_rect.topleft = (x, y)
        elif align == "topright":
            text_rect.topright = (x, y)
        elif align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


    def draw_ui(self):
        """绘制用户界面 / Draw user interface"""
        self.draw_text(f"{get_text('score')}: {self.score}", self.score_font, DARK_GRAY, WINDOW_WIDTH - 20, 15, align="topright")
        self.draw_text(f"{get_text('hi_score')}: {self.high_score}", self.ui_font, GRAY, WINDOW_WIDTH - 20, 45, align="topright")

        lives_display_text = get_text('lives')
        lives_value_display = "♥ " * self.lives if self.lives > 0 else get_text("last_life")
        lives_color = RED if self.lives <=1 else DARK_GRAY
        self.draw_text(f"{lives_display_text}: {lives_value_display}", self.score_font, lives_color, 20, 15, align="topleft")

        if self.dinosaur.invincible:
            inv_time_left = self.dinosaur.invincible_timer // 60 + 1
            self.draw_text(f"{get_text('invincible')}: {inv_time_left}s", self.ui_font, BLUE, WINDOW_WIDTH // 2, 20, align="center")

        if self.score < 300:
            alpha = max(0, 255 - int(self.score * 0.85) )
            instructions = [
                get_text("jump_inst"),
                get_text("duck_inst"),
                get_text("shoot_inst"),
                get_text("pause_inst"),
                get_text("lang_inst")
            ]
            for i, inst_text in enumerate(instructions):
                try:
                    inst_surf = self.ui_font.render(inst_text, True, DARK_GRAY)
                    inst_surf.set_alpha(alpha)
                except:
                    inst_surf = self.ui_font.render(inst_text, True, tuple(max(0,c - alpha//2) if isinstance(c, int) else c for c in DARK_GRAY))
                self.screen.blit(inst_surf, (20, 60 + i * 25))


    def draw_game_over(self):
        """绘制游戏结束界面 / Draw game over screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*BLACK, 180))
        self.screen.blit(overlay, (0,0))

        self.draw_text(get_text("game_over"), self.large_font, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 70, align="center")
        self.draw_text(f"{get_text('final_score')}: {self.score}", self.score_font, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 -10, align="center")
        if self.score > 0 and self.score >= self.high_score :
             self.draw_text(get_text("new_high_score"), self.ui_font, YELLOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30, align="center")
        self.draw_text(get_text("restart"), self.ui_font, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70, align="center")

    def draw_pause(self):
        """绘制暂停界面 / Draw pause screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*DARK_GRAY, 150))
        self.screen.blit(overlay, (0,0))
        self.draw_text(get_text("paused"), self.large_font, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30, align="center")
        self.draw_text(get_text("resume"), self.ui_font, LIGHT_GRAY, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30, align="center")

    def draw(self):
        """绘制游戏所有内容 / Draw all game content"""
        self.background.draw(self.screen)

        self.dinosaur.draw(self.screen)

        for obstacle in self.obstacles:
            if obstacle.active: obstacle.draw(self.screen)

        for fireball in self.fireballs:
            if fireball.active: fireball.draw(self.screen)

        for powerup in self.powerups:
            if powerup.active: powerup.draw(self.screen)

        self.particle_system.draw(self.screen)
        self.draw_ui()

        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause()

        pygame.display.flip()

    def restart_game(self):
        """重新开始游戏 / Restart the game"""
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        self.dinosaur = Dinosaur(70, WINDOW_HEIGHT - GROUND_HEIGHT - 56, self.audio_manager)
        self.obstacles.clear()
        self.fireballs.clear()
        self.powerups.clear()
        self.particle_system.particles.clear()

        self.score = 0
        self.lives = 3
        self.game_speed = GAME_SPEED
        self.game_over = False
        self.paused = False
        self.obstacle_timer = 0
        self.obstacle_spawn_interval = 100
        self.powerup_timer = 0
        self.powerup_spawn_interval = random.randint(400, 800)
        self.background.time_factor = 0
        self.background.generate_clouds()
        self.background.generate_ground_decorations()
        self.background.generate_hills_layer(self.background.hills_mid, count=5, y_base_offset=20, height_range=(40,100), color_offset=-30, speed_multiplier=0.2)
        self.background.generate_hills_layer(self.background.hills_far, count=3, y_base_offset=50, height_range=(80,150), color_offset=-60, speed_multiplier=0.1)

        self.audio_manager.play_music()

    def print_instructions(self):
        """打印游戏说明到控制台 / Print game instructions to console"""
        print(f"\n--- {get_text('start_message_title')} ---")
        print("------------------------------------")
        print(get_text('controls_title'))
        print(f"- {get_text('jump_inst')}")
        print(f"- {get_text('duck_inst')}")
        print(f"- {get_text('shoot_inst')}")
        print(f"- {get_text('pause_inst')}")
        print(f"- {get_text('lang_inst')}")
        print(f"- R          : {get_text('restart')} ({get_text('game_over')})") # Clarified restart context
        print("------------------------------------")
        print(get_text('powerups_title'))
        print(f"- {get_text('powerup_life')}")
        print(f"- {get_text('powerup_invincible')}")
        print(f"- {get_text('powerup_score')}")
        print("------------------------------------")


    def run(self):
        """运行游戏主循环 / Run the main game loop"""
        running = True

        asset_paths = ["assets/sounds", "assets/music", "assets/fonts"]
        for path in asset_paths:
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                    print(f"{get_text('created_dir')} {path}")
                except OSError as e:
                    print(f"{get_text('create_dir_warning')} {path}: {e}")

        self.print_instructions()

        while running:
            running = self.handle_input()

            self.update()
            self.draw()

            self.clock.tick(60)

        self.save_high_score()
        pygame.quit()
        sys.exit()

# --- Main Execution ---
# --- 主执行 ---
if __name__ == "__main__":
    game = Game()
    game.run()