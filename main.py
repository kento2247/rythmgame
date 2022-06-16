import pygame
from pygame.locals import *
import sys
import time
import timing_csv


autoplay = 0
generate_speed = 1500
fps_num = 30
music_volume = 0.3
sound_volume = 1

display_res = 80
default_width = 16*display_res
default_height = 9*display_res
width = 0
height = 0
topbar_height = 0
topbar_font_size = 0
circle_size = 0

default_generate_speed = 1500
default_game_life = 20
game_life = 0
game_combo = 0
game_score = 0
excerrent_tm = 50
good_tm = 150
ignore_tm = 300

autoplay = 0
music_ch1 = ""
music_ch2 = ""
music_ch3 = ""
notes_array = []
target_array = []
top_button_pos = []
game_status = ""
judge_message = ""
screen = ""
home_button = ""
judge_circle = ""
# copy and past your working directory path
folder_name = "/Users/---/---/---/"


def game_init(param):
    param_init()
    pygame.init()
    audio_init()
    screen_init()


def param_init():
    global notes_array
    global game_life
    global game_combo
    global game_score
    global game_status
    game_life = default_game_life
    game_combo = 0
    game_score = 0
    notes_array.clear()
    if not autoplay:
        game_status = "PLAYER"
    else:
        game_status = "AUTO"


def audio_init():
    global music_ch1
    global music_ch2
    global music_ch3
    pygame.mixer.init(frequency=44100)    # 初期設定
    music_ch1 = pygame.mixer.Sound(
        folder_name+"wav/excerrent.wav")     # 音楽ファイルの読み込み
    music_ch2 = pygame.mixer.Sound(
        folder_name+"wav/good.wav")     # 音楽ファイルの読み込み
    music_ch3 = pygame.mixer.Sound(
        folder_name+"wav/miss.wav")     # 音楽ファイルの読み込み
    music_ch1.set_volume(sound_volume)
    music_ch2.set_volume(sound_volume)
    music_ch3.set_volume(sound_volume)


def screen_init():
    global screen
    global topbar_height
    global width
    global height
    global topbar_font_size
    global circle_size
    global judge_circle
    screen = pygame.display.set_mode(
        (default_width, default_height), FULLSCREEN)
    # screen = pygame.display.set_mode( (default_width, default_height))
    width = pygame.display.get_surface().get_width()
    height = pygame.display.get_surface().get_height()
    topbar_height = width//20
    topbar_font_size = int(topbar_height*0.6)
    circle_size = height//16
    pygame.display.set_caption("RHYTHM GAME")              # タイトルバーに表示する文字
    judge_circle = pygame.Rect(width-circle_size*2, (height-topbar_height)/2,
                               circle_size, circle_size)  # creates a rect object
    # width = default_width
    # height = default_height


def draw_stage(music_title, passed_time):
    judge_message_size = width//20
    screen.fill((0, 0, 0))                                    # 画面を黒色に塗りつぶし
    set_game_topbar(music_title)
    pygame.draw.ellipse(screen, (255, 255, 255), judge_circle, height//200)
    pygame.draw.ellipse(screen, (0, 0, 200),
                        (circle_size*1, (height-topbar_height)/2, circle_size, circle_size), height//200)
    draw_notes(passed_time)
    text = pygame.font.Font(None, judge_message_size).render(
        judge_message, True, (255, 255, 255))   # 描画する文字列の設定
    screen.blit(text, [(width-len(judge_message) *
                judge_message_size//2)//2, height/3])  # 文字列の表示位置
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
    # screen_sizeで最適化
    line_width = width//80
    line_bold = width//160
    pygame.draw.rect(screen, (255, 255, 255), Rect(
        0, 0, width, topbar_height))    # 四角形を描画
    font = pygame.font.Font(None, topbar_font_size)               # フォントの設定
    text_size = font.size(music_title)
    text = font.render(music_title, True, (0, 0, 0))   # 描画する文字列の設定
    screen.blit(text, [(width//3-text_size[0])//2,
                (topbar_height-text_size[1])//2])  # 文字列の表示位置
    pygame.draw.line(screen, (0, 95, 0), (width//3-line_width*2,
                     topbar_height), (width//3+line_width, 0), line_bold)   # 直線の描画
    pygame.draw.line(screen, (0, 95, 0), (width//3*2-line_width,
                     topbar_height), (width/3*2+line_width, 0), line_bold)   # 直線の描画
    # 描画する文字列の設定
    message = str(game_combo)+"  COMBO / SCORE= " + str(game_score)
    text_size = font.size(message)
    text = font.render(message, True, (0, 0, 0))
    screen.blit(text, [width//3+(width//3-text_size[0])//2,
                (topbar_height-text_size[1])//2])  # 文字列の表示位置
    message = "LIFE=  "+str(game_life)+" / "+game_status
    text_size = font.size(message)
    text = font.render(message, True, (0, 0, 0))   # 描画する文字列の設定
    screen.blit(text, [width//3*2+(width//3-text_size[0])//2,
                (topbar_height-text_size[1])//2])  # 文字列の表示位置
    circle_size_per = 0.7
    circle_r = int(topbar_height*circle_size_per)
    circle_marge = (topbar_height-circle_r)//2
    global home_button
    home_button = pygame.Rect(width - circle_r-circle_marge, circle_marge,
                              circle_r, circle_r)  # creates a rect object
    pygame.draw.ellipse(screen, (255, 80, 80), home_button)


def set_topbar(topbar_list):
    line_bold = width//160
    pygame.draw.rect(screen, (255, 255, 255), Rect(
        0, 0, width, topbar_height))    # 四角形を描画
    font = pygame.font.Font(None, topbar_font_size)               # フォントの設定
    global top_button_pos
    top_button_pos.clear()
    for i in range(3):
        rect_area = pygame.Rect(width//3*i, 0, width//3*(i+1), topbar_height)
        top_button_pos.append(rect_area)
        message = topbar_list[i][1]
        text_size = font.size(message)
        text = font.render(message, True, (0, 0, 0))
        screen.blit(text, [width//3*i+(width//3-text_size[0]) //
                    2, (topbar_height-text_size[1])//2])  # 文字列の表示位置
    pygame.draw.line(screen, (0, 95, 0), (width//3,
                     topbar_height), (width//3, 0), line_bold)   # 直線の描画
    pygame.draw.line(screen, (0, 95, 0), (width//3*2,
                     topbar_height), (width/3*2, 0), line_bold)   # 直線の描画
    # 描画する文字列の設定
    circle_size_per = 0.7
    circle_r = int(topbar_height*circle_size_per)
    circle_marge = (topbar_height-circle_r)//2
    global home_button
    home_button = pygame.Rect(width - circle_r-circle_marge, circle_marge,
                              circle_r, circle_r)  # creates a rect object
    pygame.draw.ellipse(screen, (255, 80, 80), home_button)


def game_start():
    music_list = timing_csv.music_list
    param = []
    game_init(param)    # Pygameを初期化
    index_num = 0
    while 1:
        menu_input = move_scene(index_num)
        page_num = menu_input[0]
        command_str = menu_input[1]
        index_num = menu_input[2]
        if command_str == "game":
            track_num = index_num
            break
        elif command_str == "move":
            if index_num == -1:
                index_num = page_num-1
                if index_num < 0:
                    system_end()
        else:
            print(f"error: unexpected command_str >> {command_str}")
            system_end()
    if track_num == -1 or track_num > len(music_list):
        system_end()
    music_title = music_list[track_num]
    pygame.mixer.music.load(
        folder_name+"mp3/"+music_title+".mp3")     # 音楽ファイルの読み込み
    pygame.mixer.music.set_volume(music_volume)              # 音楽の再生回数(1回)
    count_down(3)
    play_game(music_title)


def count_down(start_num):
    font_size = height//10
    font = pygame.font.Font(None, font_size)               # フォントの設定
    global music_ch1
    for i in range(start_num):
        music_ch1.play(0)              # 音楽の再生回数(1回)
        screen.fill((0, 0, 0))
        message = str(start_num - i)
        text_size = font.size(message)
        text = font.render(
            message, True, (255, 255, 255))   # 描画する文字列の設定
        screen.blit(text, [(width-text_size[0])//2,
                    (height-text_size[1])//2])  # 文字列の表示位置
        pygame.display.update()     # 画面を更新
        time.sleep(1)


def play_game(music_title):
    global target_array
    target_array = timing_csv.get_notes_array(music_title)
    end_time = target_array[-1]
    base_time = time.time()*1000
    music_start_flag = 0
    fps_clock = pygame.time.Clock()
    judge_rect = pygame.Rect(0, topbar_height,
                             width, height-topbar_height)  # creates a rect object
    while (1):
        fps_clock.tick(fps_num)
        passed_time = time.time()*1000-base_time-generate_speed
        if music_start_flag == 0 and passed_time >= 0:
            pygame.mixer.music.play(1)
            music_start_flag = 1
        if passed_time > end_time+generate_speed*2:
            pygame.mixer.music.fadeout(3000)
            time.sleep(3)
            game_start()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()               # 再生の終了
                    pygame.quit()       # Pygameの終了(画面閉じられる)
                    game_start()
                if judge_rect.collidepoint(event.pos):
                    notes_judge(passed_time)
                if judge_circle.collidepoint(event.pos):
                    notes_judge(passed_time)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if autoplay:
                        system_end()
                    else:
                        notes_judge(passed_time)
                # if event.key == K_SPACE:
                #     print(f"{passed_time}")
                if event.key == K_ESCAPE:
                    system_end()
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                system_end()
        generate_notes(music_title, passed_time)
        erase_notes(passed_time)
        draw_stage(music_title, passed_time)


def notes_judge(passed_time):
    global notes_array
    global game_score
    global game_life
    global game_combo
    global music_ch1
    global music_ch2
    global music_ch3
    global judge_message

    if len(notes_array) == 0:
        return
    error = abs(notes_array[0]-passed_time)
    if error > ignore_tm:
        return
    music_ch1.stop()
    music_ch2.stop()
    music_ch3.stop()
    if error < good_tm:
        if error < excerrent_tm:
            game_score += 100
            judge_message = "EXCERRENT"
            music_ch1.play(0)              # 音楽の再生回数(1回)
        elif error < good_tm:
            judge_message = "GOOD"
            music_ch2.play(0)              # 音楽の再生回数(1回)
            game_score += 50
        game_combo += 1
    else:
        judge_message = "miss"
        music_ch3.play(0)              # 音楽の再生回数(1回)
        game_combo = 0
        game_life -= 1

    notes_array.pop(0)
    if game_life == 0:
        gameover()


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
        if autoplay:
            if (i) <= passed_time:
                notes_judge(passed_time)
        # 実際の環境
        else:
            if (i+ignore_tm-100) <= passed_time:
                notes_judge(passed_time)


def gameover():
    pygame.mixer.music.stop()
    font_size_1 = height//10
    message = "GAME OVER"
    font = pygame.font.Font(None, font_size_1)
    text_size = font.size(message)
    text = font.render(message, True, (255, 255, 255))   # 描画する文字列の設定
    screen.blit(text, [(width-text_size[0])//2, height/3*2])  # 文字列の表示位置
    font_size_2 = height//20
    font = pygame.font.Font(None, font_size_2)
    message = "PUSH ANY KEY"
    text_size = font.size(message)
    text = font.render(
        message, True, (255, 255, 255))   # 描画する文字列の設定
    screen.blit(text, [(width-text_size[0])//2,
                height/3*2+font_size_1])  # 文字列の表示位置
    pygame.display.update()     # 画面を更新
    while 1:
        for event in pygame.event.get():
            game_start()


def system_end():
    pygame.mixer.music.stop()               # 再生の終了
    pygame.quit()       # Pygameの終了(画面閉じられる)
    sys.exit()


def home_menu():
    music_list = timing_csv.music_list
    scene_id = 0
    font_size = height//15
    text_x_marge = width//200
    rect_marge = [width//80, height//450]
    target_x = rect_marge[0]
    target_y = []
    list_height = font_size+rect_marge[1]
    max_menu_num = (height-topbar_height)//list_height
    menu_pos_array = []
    screen.fill((0, 0, 0))                                    # 画面を黒色に塗りつぶし
    for i in range(max_menu_num):
        target_y.append(topbar_height+(rect_marge[1]+list_height)*i)
        rect_area = pygame.Rect(target_x, target_y[i],
                                width-target_x, list_height)  # creates a rect object
        menu_pos_array.append(rect_area)

    font = pygame.font.Font(None, font_size)
    while 1:
        topbar_list = [
            [-1, ">> end game"], [0, "home"], [1, "setting"]
        ]
        set_topbar(topbar_list)
        pygame.draw.ellipse(screen, (255, 80, 80), home_button)
        message = ""
        for i in range(max_menu_num):
            pygame.draw.rect(screen, (100, 100, 100), menu_pos_array[i])
            if i > len(music_list)-1:
                message = " >> end game"
            else:
                message = " # "+music_list[i]
            text = font.render(
                message, True, (255, 255, 255))   # 描画する文字列の設定
            text_size = font.size(message)
            screen.blit(
                text, [target_x+text_x_marge, target_y[i]+(list_height-text_size[1])//2])

        pygame.display.update()  # 描画処理を実行
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                system_end()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    system_end()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    game_start()
                for i in menu_pos_array:
                    if i.collidepoint(event.pos):
                        return [scene_id, "game", menu_pos_array.index(i)]
                # 判定バグるから逆順に
                top_button_pos.reverse()
                for i in top_button_pos:
                    if i.collidepoint(event.pos):
                        top_button_pos.reverse()
                        button_pos_index = top_button_pos.index(i)
                        # print(f"{event.pos}>>range {i}")
                        # print(f"{i.collidepoint(event.pos)}, {button_pos_index}")
                        return [scene_id, "move", topbar_list[button_pos_index][0]]


def setting_menu():
    # system_end()
    scene_id = 1
    font_size = height//15
    rect_marge = [width//80, height//450]
    target_x = rect_marge[0]
    target_x_1 = target_x+(width-target_x)//2
    target_x_2 = target_x+(width-target_x)*9//10
    target_x_width = (width-target_x)//10
    target_y = []
    list_height = font_size+rect_marge[1]
    max_menu_num = (height-topbar_height)//list_height
    menu_pos_array = []
    data_pos_array = []

    global autoplay
    global music_volume
    global sound_volume
    global fps_num
    global generate_speed
    data_array = [
        ["Auto Play", autoplay, 1, 0, 1],
        ["Music Volume", int(music_volume*100), 10, 0, 100],
        ["Effect Volume", int(sound_volume*100), 10, 0, 100],
        ["FPS", fps_num, 5, 15, 90],
        ["Generate Speed", generate_speed, 100, 500, 2500],
    ]
    screen.fill((0, 0, 0))                                    # 画面を黒色に塗りつぶし
    for i in range(max_menu_num):
        target_y.append(topbar_height+(rect_marge[1]+list_height)*i)
        rect_area = pygame.Rect(target_x, target_y[i],
                                width-target_x, list_height)  # creates a rect object
        pygame.draw.rect(screen, (100, 100, 100), rect_area)
        menu_pos_array.append(rect_area)
        rect_area_1 = pygame.Rect(target_x_1, target_y[i],
                                  target_x_width, list_height)  # creates a rect object
        rect_area_2 = pygame.Rect(target_x_2, target_y[i],
                                  target_x_width, list_height)  # creates a rect object
        data_pos_array.append([rect_area_1, rect_area_2])
        if i > len(data_array)-1:
            data_array.append(["-", 0, 0, 0, 0])

    font = pygame.font.Font(None, font_size)
    while 1:
        autoplay = data_array[0][1]
        music_volume = data_array[1][1]/100
        sound_volume = data_array[2][1]/100
        fps_num = data_array[3][1]
        generate_speed = data_array[4][1]
        for i in range(max_menu_num):
            target_y.append(topbar_height+(rect_marge[1]+list_height)*i)
            rect_area = pygame.Rect(target_x, target_y[i],
                                    width-target_x, list_height)  # creates a rect object
            pygame.draw.rect(screen, (100, 100, 100), rect_area)
            menu_pos_array.append(rect_area)
            rect_area_1 = pygame.Rect(target_x_1, target_y[i],
                                      target_x_width, list_height)  # creates a rect object
            rect_area_2 = pygame.Rect(target_x_2, target_y[i],
                                      target_x_width, list_height)  # creates a rect object
            data_pos_array.append([rect_area_1, rect_area_2])
            if i > len(data_array)-1:
                data_array.append(["-", 0, 0, 0, 0])
        topbar_list = [
            [-1, "< back"], [0, "home"], [1, ""]
        ]
        set_topbar(topbar_list)
        pygame.draw.ellipse(screen, (255, 100, 100), home_button)
        for i in range(max_menu_num):
            message = data_array[i][0]
            text_size = font.size(message)
            area_width = target_x_width * 5
            x_marge = (area_width-text_size[0])//2
            y_marge = (list_height-text_size[1])//2
            text = font.render(message, True, (255, 255, 255))   # 描画する文字列の設定
            screen.blit(text, [target_x+x_marge, target_y[i]+y_marge])

            message = "<"
            text_size = font.size(message)
            area_width = target_x_width
            x_marge = (area_width-text_size[0])//2
            y_marge = (list_height-text_size[1])//2
            text = font.render(message, True, (255, 255, 255))   # 描画する文字列の設定
            screen.blit(text, [target_x_1+x_marge, target_y[i]+y_marge])

            message = str(data_array[i][1])
            text_size = font.size(message)
            area_width = target_x_width * 3
            x_marge = (area_width-text_size[0])//2
            y_marge = (list_height-text_size[1])//2
            text = font.render(message, True, (255, 255, 255))   # 描画する文字列の設定
            screen.blit(text, [target_x+target_x_width *
                        6+x_marge, target_y[i]+y_marge])

            message = ">"
            text_size = font.size(message)
            area_width = target_x_width
            x_marge = (area_width-text_size[0])//2
            y_marge = (list_height-text_size[1])//2
            text = font.render(message, True, (255, 255, 255))   # 描画する文字列の設定
            screen.blit(text, [target_x_2+x_marge, target_y[i]+y_marge])

        pygame.display.update()  # 描画処理を実行
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                system_end()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    system_end()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    game_start()
                pushed_flag = 0
                for y in data_pos_array:
                    if pushed_flag:
                        break
                    for x in y:
                        if x.collidepoint(event.pos):
                            pos_y = data_pos_array.index(y)
                            pos_x = data_pos_array[pos_y].index(x)
                            # if data_array[pos_y][0] == "< back":
                            #     return [scene_id, "move", -1]
                            now_num = data_array[pos_y][1]
                            change_num = data_array[pos_y][2]*(2*pos_x-1)
                            changed_num = now_num+change_num
                            num_range = [data_array[pos_y]
                                         [3], data_array[pos_y][4]]
                            if num_range[0] <= changed_num <= num_range[1]:
                                data_array[pos_y][1] = changed_num
                                # print(
                                # f"auto{autoplay},m_vol{music_volume},auto{sound_volume},fps{fps_num},n_speed{generate_speed}")
                            pushed_flag = 1
                            # print(
                            #     f"pushed: y = {pos_y}, x = {pos_x}. {data_array[pos_y][pos_x]}")
                            # system_end()
                top_button_pos.reverse()
                for i in top_button_pos:
                    if i.collidepoint(event.pos):
                        top_button_pos.reverse()
                        button_pos_index = top_button_pos.index(i)
                        # print(f"{event.pos}>>range {i}")
                        # print(f"{i.collidepoint(event.pos)}, {button_pos_index}")
                        return [scene_id, "move", topbar_list[button_pos_index][0]]


def move_scene(scene_id):
    if scene_id == 0:
        return home_menu()
    if scene_id == 1:
        return setting_menu()
    if scene_id == 2:
        return system_end()


if __name__ == "__main__":
    autoplay = 0
    game_start()
