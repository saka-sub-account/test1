import numpy as np
import pygame

# 画像ファイルのパス
PATH_BLANK = '/Users/saka/Downloads/project_simplewalk/kusa (1).png'
PATH_samurai = '/Users/saka/Downloads/project_simplewalk/samusamu.png'
PATH_CRYSTAL = '/Users/saka/Downloads/project_simplewalk/crys2 (1) (1).png'

# 環境の設定
FIELD_LENGTH = 4
CRYSTAL_POS = 2
REWARD_FAIL = -1.0
REWARD_MOVE = -0.1
REWARD_CRYSTAL = 5.0

# Pygameの初期化
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Corridor Task")

# 画像の読み込み
img_blank = pygame.image.load(PATH_BLANK).convert_alpha()
img_robot = pygame.image.load(PATH_samurai).convert_alpha()
img_crystal = pygame.image.load(PATH_CRYSTAL).convert_alpha()
UNIT_SIZE = img_robot.get_width()

# 環境の状態
robot_pos = 0
crystal_pos = CRYSTAL_POS
done = False
robot_state = 'normal'

# メインループ
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # 右に進む
                next_pos = robot_pos + 1
                if next_pos >= FIELD_LENGTH:
                    # 右端で進もうとした
                    reward = REWARD_FAIL
                    done = True
                    robot_state = 'fail'
                else:
                    # 右端より前で進んだ
                    robot_pos = next_pos
                    reward = REWARD_MOVE
                    done = False
                    robot_state = 'normal'
            elif event.key == pygame.K_d:
                # 拾う
                if robot_pos == crystal_pos:
                    # クリスタルの場所で拾った
                    reward = REWARD_CRYSTAL
                    done = True
                    robot_state = 'success'
                else:
                    # クリスタル以外の場所で拾った
                    reward = REWARD_FAIL
                    done = True
                    robot_state = 'fail'
            else:
                continue

            # 状態の更新
            if done:
                robot_pos = 0
                crystal_pos = np.random.randint(FIELD_LENGTH)
                done = False
                robot_state = 'normal'

    # 描画
    screen.fill((255, 255, 255))

    # 床の描画
    for i in range(FIELD_LENGTH):
        screen.blit(img_blank, (i * UNIT_SIZE, 0))

    # クリスタルの描画
    if robot_state != 'success':
        screen.blit(img_crystal, (crystal_pos * UNIT_SIZE, 0))

    # キャラの描画
    if robot_state == 'fail':
        img_robot.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
    elif robot_state == 'success':
        img_robot.fill((0, 255, 0), special_flags=pygame.BLEND_RGB_MULT)
    screen.blit(img_robot, (robot_pos * UNIT_SIZE, 0))

    pygame.display.flip()

# 終了処理
pygame.quit()