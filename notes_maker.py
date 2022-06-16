import pygame
from pygame.locals import *
import sys
import time
import timing_csv

debug = 0
default_width = 1600
default_height = 900
width = 0
height = 0
topbar_height = 0
topbar_font_size = 0
circle_size = 0
fps_num = 30
music_volume = 0.3
sound_volume = 1

generate_speed = 2000

notes_array = []
target_array = []
result_array = []
autoplay = 0
screen = ""
close_button = ""
judge_circle = ""
music_ch1 = ""
folder_name = "/Users/tokurakento/Desktop/timinggame/"


def game_init(music_title):
    global screen
    global topbar_height
    global width
    global height
    global topbar_font_size
    global circle_size
    global judge_circle
    global music_ch1

    pygame.init()
    screen = pygame.display.set_mode(
        (default_width, default_height), FULLSCREEN)    # 大きさ800*450の画面を生成
    width = pygame.display.get_surface().get_width()
    height = pygame.display.get_surface().get_height()
    topbar_height = width//20
    topbar_font_size = int(topbar_height*0.6)
    circle_size = height//16
    pygame.mixer.init(frequency=44100)    # 初期設定
    pygame.display.set_caption("NOTES MAKER")              # タイトルバーに表示する文字
    judge_circle = pygame.Rect(width-circle_size*2, (height-topbar_height)/2,
                               circle_size, circle_size)  # creates a rect object
    music_ch1 = pygame.mixer.Sound(
        folder_name+"wav/excerrent.wav")     # 音楽ファイルの読み込み
    music_ch1.set_volume(sound_volume)
    pygame.mixer.music.load(
        folder_name+"mp3/"+music_title+".mp3")     # 音楽ファイルの読み込み
    pygame.mixer.music.set_volume(music_volume)              # 音楽の再生回数(1回)


def draw_stage(music_title, passed_time):
    screen.fill((0, 0, 0))                                    # 画面を黒色に塗りつぶし
    set_game_topbar(music_title)
    message = str(round(passed_time, 1))
    text = pygame.font.Font(None, 40).render(
        message, True, (255, 255, 255))   # 描画する文字列の設定
    screen.blit(text, [width/2-len(message) *
                40/4, height//3])  # 文字列の表示位置
    pygame.draw.ellipse(screen, (255, 255, 255), judge_circle, height//200)
    pygame.draw.ellipse(screen, (0, 0, 200),
                        (circle_size*1, (height-topbar_height)/2, circle_size, circle_size), height//200)
    draw_notes(passed_time)
    pygame.display.update()     # 画面を更新


def draw_notes(passed_time):
    # print(notes_array)
    global notes_array
    offset = circle_size*0.1
    for i in notes_array:
        pygame.draw.ellipse(screen, (255, 255, 255),
                            (circle_size*1-(i-passed_time-generate_speed)/generate_speed*(width-circle_size*3),
                             (height-topbar_height)/2, circle_size, circle_size))
        pygame.draw.ellipse(screen, (155, 190, 255),
                            (circle_size*1-(i-passed_time-generate_speed)/generate_speed*(width-circle_size*3)+offset,
                             (height-topbar_height)/2+offset, circle_size*0.8, circle_size*0.8))


def set_game_topbar(music_title):
    circle_size_per = 0.7
    circle_r = int(topbar_height*circle_size_per)
    circle_marge = (topbar_height-circle_r)//2
    global close_button
    close_button = pygame.Rect(width - circle_r-circle_marge, circle_marge,
                               circle_r, circle_r)  # creates a rect object
    pygame.draw.ellipse(screen, (255, 100, 100), close_button)


def game_start(music_title):
    global notes_array
    notes_array.clear()
    music_list = timing_csv.music_list
    game_init(music_title)    # Pygameを初期化
    # play_music(music_title)
    play_game(music_title)


def play_game(music_title):
    global target_array
    target_array = timing_csv.get_notes_array(music_title)
    end_time = 900000
    fps_clock = pygame.time.Clock()
    base_time = time.time()*1000
    music_start_flag = 0
    while 1:
        fps_clock.tick(fps_num)
        passed_time = time.time()*1000-base_time-generate_speed
        # print(passed_time)
        # passed_time = pygame.mixer.music.get_pos()
        if music_start_flag == 0 and passed_time >= 0:
            pygame.mixer.music.play(1)
            music_start_flag = 1
        if passed_time > end_time+generate_speed*2:
            pygame.mixer.music.fadeout(3000)
            time.sleep(3)
            system_end()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    system_end()
                if judge_circle.collidepoint(event.pos):
                    notes_judge(passed_time)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    notes_judge(passed_time)
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                system_end()
        generate_notes(music_title, passed_time)
        erase_notes(passed_time)
        draw_stage(music_title, passed_time)


def notes_judge(passed_time):
    global result_array
    global music_ch1
    music_ch1.stop()
    print(round(passed_time, 1))
    result_array.append(round(passed_time, 1))
    music_ch1.play(0)              # 音楽の再生回数(1回)


def generate_notes(music_title, passed_time):
    global notes_array
    # print(target_array)
    for i in target_array:
        if (i-generate_speed) >= passed_time:
            return
        notes_array.append(target_array[0])
        target_array.pop(0)


def erase_notes(passed_time):
    global notes_array
    for i in notes_array:
        # オートプレイ
        if (i) <= passed_time:
            notes_array.pop(0)
            if(debug):
                music_ch1.stop()
                music_ch1.play(0)              # 音楽の再生回数(1回)


def fix_result_array(start_notes_time, music_bpm):
    return
    # print(result_array)
    # bpm_time = 60*1000//music_bpm//2
    # result_array[0] = start_notes_time
    # for i in range(1, len(result_array)-1):
    #     error = result_array[i]-result_array[i-1]
    #     errer_per = error//bpm_time
    #     fixed_data = result_array[i]+errer_per*bpm_time
    #     result_array[i] = fixed_data
    # print(result_array)


def system_end():
    pygame.mixer.music.stop()               # 再生の終了
    fix_result_array(285, 110)
    pygame.quit()       # Pygameの終了(画面閉じられる)
    sys.exit()


if __name__ == "__main__":
    debug = 1
    game_start("Catch the Moment")
