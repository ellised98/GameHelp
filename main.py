import pygame
import sys
import time
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
WINDOW_SIZE = (750,600)
win = pygame.display.set_mode((WINDOW_SIZE))
pygame.display.set_caption('RPG_V2')
moving_right = False
moving_left = False
moving_up = False
moving_down = False
player_location = [300,300]
dirt = pygame.image.load('tilesets/dirt.png')
grass = pygame.image.load('tilesets/grass.png')
water = pygame.image.load('tilesets/water.png')



true_scroll = [0,0]


def load_map(path):
	f = open(path + '.txt', 'r')
	data = f.read()
	f.close()
	data =data.split('\n')
	game_map = []
	for row in data:
		game_map.append(list(row))
	return game_map

game_map = load_map('map')

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
	global animation_frames
	animation_name = path.split('/')[-1]
	animation_frame_data = []
	n = 0
	for frame in frame_durations:
		animation_frame_id = animation_name + "_" + str(n)
		img_loc = path + '/' + animation_frame_id + '.png'
		animation_image = pygame.image.load(img_loc).convert()
		animation_image.set_colorkey((255,255,255))
		animation_frames[animation_frame_id] = animation_image.copy()
		for i in range(frame):
			animation_frame_data.append(animation_frame_id)
		n += 1
	return animation_frame_data

def change_action(action_var,frame,new_value):
	if action_var != new_value:
		action_var = new_value
		frame = 0
	return action_var,frame

player_action = 'idle'
player_frame = 0
player_flip = False

game_map = load_map('map')

animation_database = {}
animation_database ['walk'] = load_animation('charmove/walk', [7,7])
animation_database['idle'] = load_animation('charmove/idle', [7,7,40])
animation_database['walkup'] = load_animation('charmove/walkup', [7,7])
animation_database['walkdown'] = load_animation('charmove/walkdown', [7,7])

player_rect = pygame.Rect(200,200,68,72)

def collision_test(rect,tiles):
	hit_list = []
	for tile in tiles:
		if rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list

def move(rect,movement,tiles):
	collision_types = {'top':False,'bottom':False, 'right':False,'left':False}
	rect.x += movement[0]
	hit_list = collision_test(rect,tiles)
	for tile in hit_list:
		if movement[0] > 0:
			rect.right = tile.left
			collision_types['right'] = True
		elif movement[0] < 0:
			rect.left = tile.right
			collision_types['left'] = True
	rect.y += movement[1]
	hit_list = collision_test(rect,tiles)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile.top
			collision_types['bottom'] = True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collision_types['top'] = True
	return rect, collision_types

while True: # game loop
    win.fill((146,244,255)) # clear screen by filling it with blue

    true_scroll[0] += (player_rect.x-true_scroll[0]-341)/10
    true_scroll[1] += (player_rect.y-true_scroll[1]-264)/10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(win,(7,80,75),pygame.Rect(0,120,300,80))
    

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                win.blit(dirt,(x*75-scroll[0],y*75-scroll[1]))
            if tile == '2':
                win.blit(grass,(x*75-scroll[0],y*75-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    if moving_up == True:
    	player_movement[0] -=2
    if moving_down == True:
    	player_movement[0] += 2


    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'walk')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'walk')

    if player_movement [1] < 1:
    	player_flip = True
    	player_action,player_frame = change_action(player_action,player_frame,'walkdown')
    if player_movement [1] > 1:
    	player_flip = False
    	player_action,player_frame = change_action(player_action,player_frame,'walkup')
    player_rect,collisions = move(player_rect,player_movement,tile_rects)



    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    win.blit(pygame.transform.flip(player_img,player_flip, False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
            	moving_up == True
            if event.key == K_DOWN:
            	moving_down == True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
            	moving_up == False
            if event.key == K_DOWN:
            	moving_down == False
        
    
    pygame.display.update()
    clock.tick(60)
