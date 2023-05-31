'''
Function:
	吃豆人小游戏
参考了网上的一些做法，进行修改优化后形成结果
'''
import sys
import pygame
import Levels


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
#资源路径参数（采用文件当前路径与资源路径链接的方式）
BGMPATH = 'sounds/bg.mp3'
ICONPATH = 'images/icon.png'
FONTPATH = 'font/ALGER.TTF'
HEROPATH = 'images/pacman.png'
BlinkyPATH = 'images/Blinky.png'
ClydePATH = 'images/Clyde.png'
InkyPATH = 'images/Inky.png'
PinkyPATH = 'images/Pinky.png'


#开始某一关游戏#
def startLevelGame(level, screen, font):
	clock = pygame.time.Clock()
	SCORE = 0
	wall_sprites = level.setupWalls(SKYBLUE)
	gate_sprites = level.setupGate(WHITE)
	hero_sprites, ghost_sprites = level.setupPlayers(HEROPATH, [BlinkyPATH, ClydePATH, InkyPATH, PinkyPATH])
	food_sprites = level.setupFood(YELLOW, WHITE)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(-1)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					for hero in hero_sprites:
						hero.changeSpeed([-1, 0])       #人物朝向x坐标负方向，即左方，后面方向切换方法相同
						hero.is_move = True             #设置移动标志，实现持续按下按键后持续移动
				elif event.key == pygame.K_RIGHT:
					for hero in hero_sprites:
						hero.changeSpeed([1, 0])
						hero.is_move = True
				elif event.key == pygame.K_UP:
					for hero in hero_sprites:
						hero.changeSpeed([0, -1])
						hero.is_move = True
				elif event.key == pygame.K_DOWN:
					for hero in hero_sprites:
						hero.changeSpeed([0, 1])
						hero.is_move = True
			if event.type == pygame.KEYUP:              #抬起按键时不再移动
				if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
					hero.is_move = False
		screen.fill(BLACK)
		for hero in hero_sprites:
			hero.update(wall_sprites, gate_sprites)
		hero_sprites.draw(screen)
		for hero in hero_sprites:
			food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)            #若人物碰到食物，则删除食物（吃掉），并由food_eaten来计数
		SCORE += len(food_eaten)
		wall_sprites.draw(screen)
		gate_sprites.draw(screen)
		food_sprites.draw(screen)
		for ghost in ghost_sprites:
			# 幽灵随机运动(有点鬼畜)
			'''
			res = ghost.update(wall_sprites, None)
			while not res:
				ghost.changeSpeed(ghost.randomDirection())
				res = ghost.update(wall_sprites, None)
			'''
			# 指定幽灵运动路径
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


#显示文字
def showText(screen, font, is_clearance):
	clock = pygame.time.Clock()
	if not is_clearance
		msg = 'Game Over!' 
	else 
		msg = 'Congratulations, you won!'
	if not is_clearance
		positions = [[235, 233], [65, 303], [170, 333]] 
	else 
		positions = [[145, 233], [65, 303], [170, 333]]
	surface = pygame.Surface((400, 200))
	surface.set_alpha(10)
	surface.fill((128, 128, 128))
	screen.blit(surface, (100, 200))
	texts = [font.render(msg, True, WHITE),
			 font.render('Press ENTER to continue or play again.', True, WHITE),
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
	is_clearance = startLevelGame(level, screen, font_small)
	showText(screen, font_big, is_clearance)

	

#测试
main()
