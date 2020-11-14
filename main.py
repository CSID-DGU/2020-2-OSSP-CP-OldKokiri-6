__author__ = "Shivam Shekhar"
made_by = "OldKokiri-6"

from src.dino import *
from src.cactus import *
from src.ptera import *
from src.ground import *
from src.cloud import *
from src.scoreboard import *
from db_interface import InterfDB

db = InterfDB("score.db")


def introscreen():
    pygame.mixer.music.stop()
    temp_dino = Dino(44, 47)
    temp_dino.isBlinking = True
    gameStart = False

    callout, callout_rect = load_image('call_out.png', 196, 45, -1)
    callout_rect.left = width * 0.05
    callout_rect.top = height * 0.4

    temp_ground, temp_ground_rect = load_sprite_sheet('ground.png', 15, 1, -1, -1, -1)
    temp_ground_rect.left = width / 20
    temp_ground_rect.bottom = height

    logo, logo_rect = load_image('logo.png', 240, 40, -1)
    logo_rect.centerx = width * 0.6
    logo_rect.centery = height * 0.6
    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        temp_dino.isJumping = True
                        temp_dino.isBlinking = False
                        temp_dino.movement[1] = -1 * temp_dino.jumpSpeed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    temp_dino.isJumping = True
                    temp_dino.isBlinking = False
                    temp_dino.movement[1] = -1 * temp_dino.jumpSpeed
                if event.type == pygame.VIDEORESIZE:  # 최소해상도
                    if (event.w < 600 and event.h < 150) or event.w < 600 or event.h < 150:
                        global resized_screen
                        resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)
            screen.blit(temp_ground[0], temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo, logo_rect)
                screen.blit(callout, callout_rect)
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
    counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

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
                    if pygame.sprite.collide_mask(playerDino, c):
                        c.kill()
                        life -= 1
                        if life == 0:
                            playerDino.isDead = True
                        # playerDino.isDead = True
                        if pygame.mixer.get_init() != None:
                            die_sound.play()

                for p in pteras:
                    p.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, p):
                        p.kill()
                        life -= 1
                        if life == 0:
                            playerDino.isDead = True
                        # playerDino.isDead = True
                        if pygame.mixer.get_init() != None:
                            die_sound.play()

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

                playerDino.update()
                cacti.update()
                pteras.update()
                clouds.update()
                new_ground.update()
                scb.update(playerDino.score)
                highsc.update(high_score)

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image, HI_rect)
                    cacti.draw(screen)
                    pteras.draw(screen)
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
                    db.query_db(f"insert into user(username, score) values ('nnn', '{playerDino.score}');")
                    db.commit()

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
                            board()
                            # introscreen()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        board()
                        # introscreen()

                    if event.type == pygame.VIDEORESIZE:  # 최소해상도 #버그있음
                        if (event.w < 600 and event.h < 150) or event.w < 600 or event.h < 150:
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
    result = db.query_db("select score from user order by score desc;")
    gameQuit = False

    while not gameQuit:

        if pygame.display.get_surface() is None:
            gameQuit = True

        else:
            screen.fill(background_col)

            ### username setting
            temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
            HI_image = pygame.Surface((22, int(11 * 6 / 5)))
            HI_rect = HI_image.get_rect()
            HI_image.fill(background_col)
            HI_image.blit(temp_images[10], temp_rect)
            temp_rect.left += temp_rect.width
            HI_image.blit(temp_images[11], temp_rect)
            ###

            for i, score in enumerate(result):
                board = Scoreboard(width * 0.5, height * (0.5 + 0.1 * i))
                board.update(score['score'])
                board.draw()

                ### username drawing
                HI_rect.top = height * (0.5 + 0.1 * i)
                HI_rect.left = width * 0.3
                screen.blit(HI_image, HI_rect)
                ###

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
                    if (event.w < 600 and event.h < 150) or event.w < 600 or event.h < 150:
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

    global resized_screen
    pygame.mixer.music.pause() # 일시정지상태가 되면 배경음악도 일시정지

    retbutton_image, retbutton_rect = load_image('replay_button.png', 35, 31, -1)
    resume_image, resume_rect = load_image('replay_button.png', 35, 31, -1)
    ###
    resized_retbutton_image, resized_retbutton_rect  = load_image('replay_button.png', 35*resized_screen.get_width()//600, 31*resized_screen.get_height()//200, -1)
    resized_resume_image, resized_resume_rect = load_image('replay_button.png', 35*resized_screen.get_width()//600, 31*resized_screen.get_height()//200, -1)
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
                    if (event.w < 600 and event.h < 150) or event.w < 600 or event.h < 150:
                        
                        resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

            screen.fill((200, 200, 200))
            retbutton_rect.centerx = width * 0.4
            retbutton_rect.top = height * 0.52
            resume_rect.centerx = width * 0.6
            resume_rect.top = height * 0.52
            ###
            resized_retbutton_rect.centerx = resized_screen.get_width() * 0.4
            resized_retbutton_rect.top = resized_screen.get_height() * 0.52
            resized_resume_rect.centerx = resized_screen.get_width() * 0.6
            resized_resume_rect.top = resized_screen.get_height() * 0.52
            resized_screen.blit(retbutton_image, resized_retbutton_rect)
            resized_screen.blit(resume_image, resized_resume_rect)
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


def main():
    db.init_db()
    isGameQuit = introscreen()
    if not isGameQuit:
        introscreen()


main()
