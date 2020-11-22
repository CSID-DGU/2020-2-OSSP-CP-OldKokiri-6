__author__ = "Shivam Shekhar"
made_by = "OldKokiri-6"

from src.dino import *
from src.cactus import *
from src.ptera import *
from src.ground import *
from src.cloud import *
from src.scoreboard import *
from src.item import *
from src.heart import *
import db.db_interface as dbi

db = dbi.InterfDB("db/score.db")

def introscreen():
    global resized_screen
    pygame.mixer.music.stop()
    temp_dino = Dino(44, 47)
    temp_dino.isBlinking = True
    gameStart = False
    '''
    callout, callout_rect = load_image('call_out.png', 196, 45, -1)
    callout_rect.left = width * 0.05
    callout_rect.top = height * 0.4
    '''
    temp_ground, temp_ground_rect = load_sprite_sheet('ground.png', 15, 1, -1, -1, -1)
    temp_ground_rect.left = width / 20
    temp_ground_rect.bottom = height

    logo, logo_rect = load_image('logo.png', 180, 30, -1)
    logo_rect.centerx = width * 0.22
    logo_rect.centery = height * 0.3

    Background, Background_rect = load_image('introscreenBG.png', 600, 200, -1)
    Background_rect.left = width*0
    Background_rect.bottom = height

    #introscreen refactoring
    #between_btn = 50 #버튼간격 
    between_btn = 0.25
     
    r_btn_gamestart, r_btn_gamestart_rect = load_image('btn_start.png', 240*rwidth//width, 60*rheight//height, -1); btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 240, 60, -1)
    r_btn_board, r_btn_board_rect = load_image('btn_board.png', 240*rwidth//width, 60*rheight//height, -1); btn_board, btn_board_rect = load_image('btn_board.png', 240, 60, -1)
    r_btn_credit, r_btn_credit_rect = load_image('btn_credit.png', 240*rwidth//width, 60*rheight//height, -1); btn_credit, btn_credit_rect = load_image('btn_credit.png', 240, 60, -1)
    
    btn_gamestart_rect.centerx, btn_board_rect.centerx, btn_credit_rect.centerx = width * 0.72, width * 0.72, width * 0.72
    btn_gamestart_rect.centery, btn_board_rect.centery, btn_credit_rect.centery = height * 0.33, height * (0.33+between_btn), height * (0.33+2*between_btn)

    r_btn_gamestart_rect.centerx, r_btn_board_rect.centerx, r_btn_credit_rect.centerx = rwidth * 0.72, rwidth * 0.72, rwidth * 0.72
    r_btn_gamestart_rect.centery, r_btn_board_rect.centery, r_btn_credit_rect.centery = rheight * 0.33, rheight * (0.33+between_btn), rheight * (0.33+2*between_btn)

    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                '''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        temp_dino.isJumping = True
                        temp_dino.isBlinking = False
                        temp_dino.movement[1] = -1 * temp_dino.jumpSpeed
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    temp_dino.isJumping = True
                    temp_dino.isBlinking = False
                    temp_dino.movement[1] = -1 * temp_dino.jumpSpeed
                '''
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if r_btn_gamestart_rect.collidepoint(x, y):
                            temp_dino.isJumping = True
                            temp_dino.isBlinking = False
                            temp_dino.movement[1] = -1 * temp_dino.jumpSpeed

                        if r_btn_board_rect.collidepoint(x, y):
                            board()

                if event.type == pygame.VIDEORESIZE:  # 최소해상도
                    if (event.w < width and event.h < height) or event.w < width or event.h < height:
                        resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)
            screen.blit(temp_ground[0], temp_ground_rect)
            screen.blit(Background, Background_rect)
            screen.blit(btn_gamestart, btn_gamestart_rect)
            screen.blit(btn_board, btn_board_rect)
            screen.blit(btn_credit, btn_credit_rect)
            
            if temp_dino.isBlinking:
                screen.blit(logo, logo_rect)
                #screen.blit(callout, callout_rect)
            temp_dino.draw()   
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), (0, 0))
            pygame.display.update()

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True
            gameplay()

    pygame.quit()
    quit()


def gameplay():
    pygame.mixer.music.play(-1) # 배경음악 실행
    global high_score
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    ###
    life = 3
    ###
    paused = False
    playerDino = Dino(44, 47)
    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    heart = HeartIndicator(life)
    counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items

    retbutton_image, retbutton_rect = load_image('replay_button.png', 35, 31, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 190, 11, -1)

    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
    HI_image = pygame.Surface((22, int(11 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.1
    HI_rect.left = width * 0.73

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if playerDino.rect.bottom == int(0.98 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and playerDino.rect.bottom == int(0.98 * height):
                            # (mouse left button, wheel button, mouse right button)
                            playerDino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        playerDino.isDucking = False

                    if event.type == pygame.VIDEORESIZE:  # 최소해상도
                        if (event.w < 600 and event.h < 150) or event.w < 600 or event.h < 150:
                            global resized_screen
                            resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

            if not paused:
                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > 500:
                            playerDino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, p):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > 500:
                            playerDino.collision_immune = False

                if not playerDino.isSuper:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(playerDino, s):
                            playerDino.collision_immune = True
                            playerDino.isSuper = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                else:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(playerDino, s):
                            playerDino.collision_immune = True
                            playerDino.isSuper = True
                            s.kill()
                            item_time = pygame.time.get_ticks()

                    if pygame.time.get_ticks() - item_time > 2000:
                        playerDino.collision_immune = False
                        playerDino.isSuper = False

                for l in life_items:
                    l.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, l):
                        life += 1
                        l.kill()

                if len(cacti) < 2:
                    if len(cacti) == 0:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(gamespeed, 40, 40))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(gamespeed, 40, 40))

                if len(pteras) == 0 and random.randrange(0, 200) == 10 and counter > 500:
                    for l in last_obstacle:
                        if l.rect.right < width * 0.8:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(gamespeed, 46, 40))

                if len(clouds) < 5 and random.randrange(0, 300) == 10:
                    Cloud(width, random.randrange(height / 5, height / 2))

                if len(shield_items) == 0 and random.randrange(0, 200) == 10 and counter > 300:
                    for l in last_obstacle:
                        if l.rect.right < width * 0.8:
                            last_obstacle.empty()
                            last_obstacle.add(ShieldItem(gamespeed, 46, 40))

                if len(life_items) == 0 and random.randrange(0, 300) == 10 and counter > 400:
                    for l in last_obstacle:
                        if l.rect.right < width * 0.8:
                            last_obstacle.empty()
                            last_obstacle.add(LifeItem(gamespeed, 40, 40))

                playerDino.update()
                cacti.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                new_ground.update()
                scb.update(playerDino.score)
                highsc.update(high_score)
                heart.update(life)

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    heart.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image, HI_rect)
                    cacti.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), (0, 0))
                    pygame.display.update()
                clock.tick(FPS)

                if playerDino.isDead:
                    gameOver = True
                    pygame.mixer.music.stop() #죽으면 배경음악 멈춤
                    if playerDino.score > high_score:
                        high_score = playerDino.score
                    '''
                    db.query_db(f"insert into user(username, score) values ('nnn', '{playerDino.score}');")
                    db.commit()
'''
                if counter % 700 == 699:  # 게임스피드 조작부분(gamespeed아래에 메뉴창 뜨게하는 코드 추가할 것)
                    new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameQuit = True
                            typescore()
                            db.query_db(f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                            db.commit()
                            board()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        typescore()
                        db.query_db(f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                        db.commit()
                        board()

                    if event.type == pygame.VIDEORESIZE:  # 최소해상도 #버그있음
                        if (event.w < width and event.h < height) or event.w < width or event.h < height:
                            resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

            highsc.update(high_score)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image, gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), (0, 0))
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


def board():
    gameQuit = False
    results = db.query_db("select username, score from user order by score desc;")

    while not gameQuit:

        if pygame.display.get_surface() is None:
            gameQuit = True

        else:
            screen.fill(background_col)

            for i, result in enumerate(results):
                name_inform_surface = font.render("Name", True, black)
                score_inform_surface = font.render("Score", True, black)
                score_surface = font.render(str(result['score']), True, black)
                txt_surface = font.render(result['username'], True, black)

                screen.blit(name_inform_surface, (width * 0.3, height * 0.30))
                screen.blit(score_inform_surface, (width * 0.5, height * 0.30))
                screen.blit(score_surface, (width * 0.5, height * (0.45 + 0.1 * i)))
                screen.blit(txt_surface, (width*0.3, height * (0.45 + 0.1 * i)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        gameQuit = True
                        introscreen()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    gameQuit = True
                    introscreen()

                if event.type == pygame.VIDEORESIZE:  # 최소해상도 #버그있음
                    if (event.w < width and event.h < height) or event.w < width or event.h < height:
                        global resized_screen
                        resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), (0, 0))

            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


def pausing():
    gameQuit = False
    pause_pic, pause_pic_rect = load_image('pause_pic.png', 240, 50, -1)
    pause_pic_rect.centerx = width * 0.5
    pause_pic_rect.centery = height * 0.2

    global resized_screen
    pygame.mixer.music.pause() # 일시정지상태가 되면 배경음악도 일시정지

    retbutton_image, retbutton_rect = load_image('main_button.png', 35, 31, -1)
    resume_image, resume_rect = load_image('continue_button.png', 35, 31, -1)
    ###
    resized_retbutton_image, resized_retbutton_rect = load_image('main_button.png', 35*resized_screen.get_width()//600, 31*resized_screen.get_height()//200, -1)
    resized_resume_image, resized_resume_rect = load_image('continue_button.png', 35*resized_screen.get_width()//600, 31*resized_screen.get_height()//200, -1)
    ###
    while not gameQuit:
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            gameQuit = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause() # pausing상태에서 다시 esc누르면 배경음악 일시정지 해제
                        return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if resized_retbutton_rect.collidepoint(x, y):
                            introscreen()

                        if resized_resume_rect.collidepoint(x, y):
                            pygame.mixer.music.unpause() # pausing상태에서 오른쪽의 아이콘 클릭하면 배경음악 일시정지 해제

                            return False

                if event.type == pygame.VIDEORESIZE:
                    if (event.w < width and event.h < height) or event.w < width or event.h < height:

                        resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

            screen.fill((250, 200, 200))
            screen.blit(pause_pic, pause_pic_rect)
            retbutton_rect.centerx = width * 0.4
            retbutton_rect.top = height * 0.52
            resume_rect.centerx = width * 0.6
            resume_rect.top = height * 0.52
            ###
            resized_retbutton_rect.centerx = rwidth * 0.4
            resized_retbutton_rect.top = rheight * 0.52
            resized_resume_rect.centerx = rwidth * 0.6
            resized_resume_rect.top = rheight * 0.52
            ###
            screen.blit(retbutton_image, retbutton_rect)
            screen.blit(resume_image, resume_rect)
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                (0, 0))
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def typescore():
    done = False
    active = True

    letternum_restriction=3
    screen = pygame.display.set_mode((600, 200))
    clock = pygame.time.Clock()
    input_box = pygame.Rect(250, 100, 300, 40)
    #color_inactive = pygame.Color('lightskyblue3')
    color = pygame.Color('dodgerblue2')

    text = ''
    text2 = font.render("플레이어 이름을 입력해주세요", True, (28,0,0))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                # if len(text)==letternum_restriction:
                #     done = True

            if event.type == pygame.KEYDOWN:
                #if active:
                if event.key == pygame.K_RETURN:
                    global gamername
                    gamername=text.upper()
                    done=True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if event.unicode.isalpha()==True:
                        if len(text)<letternum_restriction:
                            text += event.unicode

        screen.fill((255,255 ,255))
        txt_surface = font.render(text.upper(), True, color)
        width = max(100, txt_surface.get_width()+10)
        input_box.w = width

        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(text2,(80,50))

        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


def main():
    db.init_db()
    isGameQuit = introscreen()
    if not isGameQuit:
        introscreen()

if __name__ == "__main__":
    main()
