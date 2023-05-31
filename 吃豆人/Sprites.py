'''
Function:
	定义一些精灵类
'''
import random
import pygame

#角色类
class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, role_image_path, base_speed):
		pygame.sprite.Sprite.__init__(self)
		self.role_name = role_image_path.split('/')[1].split('.')[0]               #匹配名字以给敌人分配固定行走路径
		self.base_image = pygame.image.load(role_image_path).convert()
		self.image = self.base_image.copy()
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.base_speed = base_speed
		self.speed = [0, 0]
		self.is_move = False
		self.tracks = []                                   #属于敌人的运动列表，初始设空值，在关卡类中设置
		self.tracks_loc = [0, 0]
	#更新角色位置
	def update(self, wall_sprites, gate_sprites):
		if not self.is_move:
			return False
		x_pre = self.rect.left
		y_pre = self.rect.top
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		is_collide = pygame.sprite.spritecollide(self, wall_sprites, False)
		if gate_sprites is not None:
			if not is_collide:
				is_collide = pygame.sprite.spritecollide(self, gate_sprites, False)
		if is_collide:
			self.rect.left = x_pre            #撞墙则人物下一个位置保持原位，表示撞墙
			self.rect.top = y_pre
			return False
		return True

		# 改变速度方向
	def changeSpeed(self, direction):  # 改变运动方向
		if direction[0] < 0:
			self.image = pygame.transform.flip(self.base_image, True, False)  # 翻转
		elif direction[0] > 0:
			self.image = self.base_image.copy()
		elif direction[1] < 0:
			self.image = pygame.transform.rotate(self.base_image, 90)  # 转动方向
		elif direction[1] > 0:
			self.image = pygame.transform.rotate(self.base_image, -90)
		self.speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]  # 速度朝向，即运动方向改变
		return self.speed
	'''
	生成随机的方向(因为敌人使用随机策略实现效果不好，则弃用随机移动策略，本函数不使用)
	def randomDirection(self):
		return random.choice([[-0.5, 0], [0.5, 0], [0, 0.5], [0, -0.5]])
	'''

#墙类
class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y


#食物类
class Food(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color, bg_color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(bg_color)
		self.image.set_colorkey(bg_color)
		pygame.draw.ellipse(self.image, color, [0, 0, width, height])        #画小椭圆表示食物
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y