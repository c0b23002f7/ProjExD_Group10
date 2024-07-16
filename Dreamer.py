import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class HP:
    def __init__(self, x, y, max_hp, width=400, height=30):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.width = width
        self.height = height

    def draw(self, screen):
        # HPバーの表示
        fill = (self.current_hp / self.max_hp) * self.width
        fill_rect = pg.Rect(self.x, self.y, fill, self.height)
        border_rect = pg.Rect(self.x, self.y, self.width, self.height)

        if self.current_hp <= 20:
            pg.draw.rect(screen, (255, 0, 0), fill_rect)
        else:
            pg.draw.rect(screen, (0, 255, 0), fill_rect)

        pg.draw.rect(screen, (0, 0, 0), border_rect, 2)

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0

    def heal(self, amount):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp


class Hiroin:
    # キー移動に対する移動量
    delta = {
        pg.K_LEFT: (-10, 0),
        pg.K_RIGHT: (10, 0),
        pg.K_UP: (0, -10),  # 上方向への移動を追加
        pg.K_DOWN: (0, 10),  # 下方向への移動を追加
    }
    # 画像のロード
    imgs = {
        (5, 0): pg.transform.rotozoom(pg.image.load("fig/file.png"), 0, 0.6),      # 初期状態(正面)
        (-10, 0): pg.transform.rotozoom(pg.image.load("fig/file(0).png"), 0, 0.6), # 左向き
        (10, 0): pg.transform.rotozoom(pg.image.load("fig/file(1).png"), 0, 0.6),   # 右向き
        (0, -10): pg.transform.rotozoom(pg.image.load("fig/file(2).png"), 0, 0.6),   #上向き
        (0, 10): pg.transform.rotozoom(pg.image.load("fig/file.png"), 0, 0.6), #下向き
    }

    def __init__(self, xy: tuple[int, int]):
        self.img = __class__.imgs[(5, 0)]  # 初期画像の設定
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.gravity = 0.5       # 重力の設定
        self.can_heal = True     # healが可能かどうかのフラグ

    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/file({num}).png"), 0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.rct.center
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        prev_rect = self.rct.copy()

        self.rct.move_ip(sum_mv)

        if self.rct.left < 0:
            self.rct.left = 0
        elif self.rct.right > screen.get_width():
            self.rct.right = screen.get_width()

        
        if self.rct.top < 0:
            self.rct.top = 0
        elif self.rct.bottom > screen.get_height():
            self.rct.bottom = screen.get_height()

        # 移動が成功した場合、前回の位置を更新
        if self.rct.topleft == prev_rect.topleft:
            self.rct.topleft = prev_rect.topleft

        # 移動方向に応じた画像の更新
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)

        screen.blit(self.img, self.rct)

    def heal(self, amount):
        if self.can_heal:
            self.current_hp += amount
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0



class Mika:
    delta = {  # 押下キーと移動量の辞書
        pg.K_LEFT: (-10, 0),
        pg.K_RIGHT: (+10, 0),
        pg.K_UP: (0, -10),   # 上方向への移動を追加
        pg.K_DOWN: (0, 10),  # 下方向への移動を追加
    }

    imgs = {
        (+5, 0): pg.transform.rotozoom(pg.image.load("fig/mika.png"), 0, 0.4),   # 初期画像を指定してください
        (-10, 0): pg.transform.rotozoom(pg.image.load("fig/mika(0).png"), 0, 0.4),
        (+10, 0): pg.transform.rotozoom(pg.image.load("fig/mika(1).png"), 0, 0.4),
        (0, -10): pg.transform.rotozoom(pg.image.load("fig/mika(2).png"), 0, 0.4),   #上向き
        (0, 10): pg.transform.rotozoom(pg.image.load("fig/mika.png"), 0, 0.4), #下向き
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.max_hp = 100         # 最大HP
        self.current_hp = 100     # 現在のHP

    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/file({num}).png"), 0, 4.0)
        self.rect = self.image.get_rect()
        self.rect.center = self.rct.center
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        prev_rect = self.rct.copy()

        self.rct.move_ip(sum_mv)

        if self.rct.left < 0:
            self.rct.left = 0
        elif self.rct.right > screen.get_width():
            self.rct.right = screen.get_width()

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)
        
        if self.rct.top < 0:
            self.rct.top = 0
        elif self.rct.bottom > screen.get_height():
            self.rct.bottom = screen.get_height()

        # 移動が成功した場合、前回の位置を更新
        if self.rct.topleft == prev_rect.topleft:
            self.rct.topleft = prev_rect.topleft

        screen.blit(self.img, self.rct)

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0



class Frame:
    def __init__(self, frame_x=20, frame_y=570, frame_width=120, frame_height=120):
        self.frame_x = frame_x  # 枠の始点x軸
        self.frame_y = frame_y  # 枠の始点y軸
        self.frame_width = frame_width  # 横幅
        self.frame_height = frame_height  # 縦幅
        self.hiroin_img = pg.transform.rotozoom(pg.image.load("fig/hiroin_file(3).png"), 0, 0.8)
        self.mika_img = pg.transform.rotozoom(pg.image.load("fig/mika_file(3).png"), 0, 0.6)

    def draw(self, screen, show_hiroin: bool, show_mika: bool):
        # キャラの表示
        chara_rect = pg.Surface((self.frame_width, self.frame_height))
        pg.draw.rect(chara_rect, (0, 0, 0), pg.Rect(self.frame_x, self.frame_y, self.frame_width, self.frame_height))  # 対応するsurface , 色, 表示幅(初期値x, 初期値y, 幅)

        if show_hiroin:
            hiroin_img_rect = self.mika_img.get_rect(center=(self.frame_width // 2, self.frame_height // 2))
            chara_rect.blit(self.mika_img, hiroin_img_rect)
        elif show_mika:
            mika_img_rect = self.hiroin_img.get_rect(center=(self.frame_width // 2, self.frame_height // 2))
            chara_rect.blit(self.hiroin_img, mika_img_rect)

        screen.blit(chara_rect, (self.frame_x, self.frame_y))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((1200, 700))
    clock = pg.time.Clock()
    # 背景画像をロードして、ウインドウのサイズにリサイズ
    back_img = pg.image.load("fig/24535830.jpg")
    back_img = pg.transform.scale(back_img, (1200, 700))
    
    # 初期キャラクターと位置を設定
    char_pos = (100, 500)
    hiroin = Hiroin(char_pos)
    mika = Mika(char_pos)
    frame = Frame()
    show_hiroin = True
    show_mika = False

    player_hp = HP(50, 50, 100)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_2 and show_hiroin:
                    show_hiroin = False
                    show_mika = True
                    char_pos = hiroin.rct.center  # 現在の位置を保存
                    mika.rct.center = char_pos    # 位置を引き継ぐ
                elif event.key == pg.K_3 and show_mika:
                    show_mika = False
                    show_hiroin = True
                    char_pos = mika.rct.center   # 現在の位置を保存
                    hiroin.rct.center = char_pos  # 位置を引き継ぐ
                elif event.key == pg.K_d:
                    if show_hiroin:
                        player_hp.take_damage(10)
                elif event.key == pg.K_h:
                    if show_hiroin:
                        player_hp.heal(10)

        screen.blit(back_img, [0, 0])  # 背景画像を表すsurface

        key_lst = pg.key.get_pressed()
        if show_hiroin:
            hiroin.update(key_lst, screen)
        elif show_mika:
            mika.update(key_lst, screen)

        player_hp.draw(screen)
        frame.draw(screen, show_hiroin, show_mika)
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
