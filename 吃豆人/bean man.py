'''
Function:
	吃豆人小游戏
'''
import sys
import pygame
import Levels
from button import playbutton

#定义一些必要的参数
#颜色参数
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)
SPRINGGREEN = (0, 255, 127)
ORANGE = (255,165,0)
base_speed = [30, 30]
#资源路径参数（采用文件当前路径与资源路径链接的方式）
BGMPATH = 'sounds/bg.mp3'
ICONPATH = 'images/icon.png'
FONTPATH = 'font/ALGER.TTF'
HEROPATH = 'images/pacman.png'
BlinkyPATH = 'images/Blinky.png'
ClydePATH = 'images/Clyde.png'
InkyPATH = 'images/Inky.png'
PinkyPATH = 'images/Pinky.png'

SCORE = 0
#开始某一关游戏
def start(level, screen, font, SCORE = 0):
	clock = pygame.time.Clock()
	wall_sprites = level.setupWalls(SPRINGGREEN)
	gate_sprites = level.setupGate(WHITE)
	hero_sprites, ghost_sprites = level.setupPlayers(HEROPATH, [BlinkyPATH, ClydePATH, InkyPATH, PinkyPATH], base_speed)
	food_sprites = level.setupFood(BLUE, WHITE)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(-1)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					for a in hero_sprites:
						a.changeSpeed([-1, 0])       #人物朝向x坐标负方向，即左方，后面方向切换方法相同
						a.move = True             #设置移动标志，实现持续按下按键后持续移动
				elif event.key == pygame.K_RIGHT:
					for a in hero_sprites:
						a.changeSpeed([1, 0])
						a.move = True
				elif event.key == pygame.K_UP:
					for a in hero_sprites:
						a.changeSpeed([0, -1])
						a.move = True
				elif event.key == pygame.K_DOWN:
					for a in hero_sprites:
						a.changeSpeed([0, 1])
						a.move = True
			elif event.type == pygame.KEYUP:              #抬起按键时不再移动
				if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
					a.move = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mousex,mousey = pygame.mouse.get_pos()
		screen.fill(BLACK)
		for a in hero_sprites:
			a.update(wall_sprites, gate_sprites)
		hero_sprites.draw(screen)
		for a in hero_sprites:
			food_eaten = pygame.sprite.spritecollide(a, food_sprites, True)            #若人物碰到食物，则删除食物（吃掉），并由food_eaten来计数
		SCORE += len(food_eaten)
		wall_sprites.draw(screen)
		gate_sprites.draw(screen)
		food_sprites.draw(screen)
		challenge(SCORE, base_speed, screen, font)
		for ghost in ghost_sprites:
			# 幽灵随机运动(有点鬼畜)
			'''
			res = ghost.update(wall_sprites, None)
			while not res:
				ghost.changeSpeed(ghost.randomDirection())
				res = ghost.update(wall_sprites, None)
			'''
			# 指定幽灵运动路径(与网上关卡的敌人运动策略配合使用)
			if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:                        #控制敌人行进列表里的每一步用多少次
				ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
				ghost.tracks_loc[1] += 1
			else:
				if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
					ghost.tracks_loc[0] += 1
				elif ghost.role_name == 'Clyde':
					ghost.tracks_loc[0] = 2
				else:
					ghost.tracks_loc[0] = 0
				ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
				ghost.tracks_loc[1] = 0
			if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
				ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
			else:
				if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
					loc0 = ghost.tracks_loc[0] + 1                       #通过此标志(loc0)来控制敌人行进列表里的下一步使用
				else:
					loc0 = 0
				ghost.changeSpeed(ghost.tracks[loc0][0: 2])
			ghost.update(wall_sprites, None)
		ghost_sprites.draw(screen)
		score_text = font.render("Score: %s" % SCORE, True, RED)
		screen.blit(score_text, [10, 10])
		if len(food_sprites) == 0:
			is_clearance = True
			break
		if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
			is_clearance = False
			break
		pygame.display.flip()
		clock.tick(10)

	return is_clearance

def challenge(SCORE,base_speed,screen, font):
	if SCORE%10 == 0:                                 #发现调整速度后会出现角色卡在地图的情况，故不适用速度自动切换
		if base_speed[0] < 31:
			base_speed[0] = 30
			if base_speed[1] < 31:
				base_speed[1] = 30
	if SCORE < 130:
		if SCORE%8 == 1:
			text = font.render("Something changed!", True, RED)
			screen.blit(text, [200, 10])
		elif SCORE%8 == 2:
			text = font.render("Something changed!", True, RED)
			screen.blit(text, [200, 10])
		elif SCORE%8 == 3:
			text = font.render("Something changed!", True, RED)
			screen.blit(text, [200, 10])
	elif SCORE > 100 and SCORE <= 130:
		text = font.render("Almost", True, RED)
		screen.blit(text, [200, 10])
	elif SCORE > 130 and SCORE <= 180:
		text = font.render("You're gonna make it!", True, ORANGE)
		screen.blit(text, [200, 10])
	elif SCORE > 180:
		text = font.render("We are the champion!", True, YELLOW)
		screen.blit(text, [200, 10])

def checkbutton(playbutton,mousex,mousey):
		buttonactive = playbutton.rect.collidepoint(mousex,mousey)
		if buttonactive:
			return False
		else:
			return True
#显示文字
def showText(screen, font, is_clearance):
	clock = pygame.time.Clock()
	msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
	positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
	surface = pygame.Surface((400, 200))
	surface.set_alpha(10)
	surface.fill((128, 128, 128))
	screen.blit(surface, (100, 200))
	texts = [font.render(msg, True, WHITE),font.render('Press ENTER to continue or play again.', True, WHITE),
			 font.render('Press ESCAPE to quit.', True, WHITE)]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
						main()
				elif event.key == pygame.K_ESCAPE:
					sys.exit()
		for idx, (text, position) in enumerate(zip(texts, positions)):                           #通过拉链函数将文本内容和位置联系起来输出
			screen.blit(text, position)
		pygame.display.flip()
		clock.tick(10)




#主函数
def main():
	pygame.init()
	icon_image = pygame.image.load(ICONPATH)
	pygame.display.set_icon(icon_image)
	screen = pygame.display.set_mode([606, 606])
	pygame.display.set_caption('吃豆人')
	pygame.mixer.init()
	pygame.mixer.music.load(BGMPATH)
	pygame.mixer.music.play(-1, 0.0)
	pygame.font.init()
	font_small = pygame.font.Font(FONTPATH, 18)
	font_big = pygame.font.Font(FONTPATH, 24)
	level = Levels.Level1()
	is_clearance = start(level, screen, font_small, SCORE)
	showText(screen, font_big, is_clearance)

	

#测试
main()