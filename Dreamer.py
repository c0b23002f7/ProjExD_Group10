import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Hiroin:
    """
    ヒロインに関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    imgs = {
        (+5, 0): pg.image.load("fig/file.png"),  # 初期画像を指定してください
        (-1, 0): pg.image.load("fig/file(0).png"),
        (+1, 0): pg.image.load("fig/file(1).png")
    }

    

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.gravity = 0.5
        self.is_jumping = False
        self.jump_speed = 20
    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/file({num}).png"), 0, 2.0)
        self.rect = self.image.get_rect()
        self.rect.center = self.rct.center
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if key_lst[pg.K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.jump_speed = 15
        if self.is_jumping:
            self.rct.y -= self.jump_speed
            self.jump_speed -= self.gravity
            if self.rct.bottom >= 500:  # 地面に到達した場合
                self.rct.bottom = 500
                self.is_jumping = False
                self.jump_speed = 15
        self.rct.move_ip(sum_mv)
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)
        
        screen.blit(self.img, self.rct)
def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((1100, 650))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/24535830.jpg") #背景画像
    # bg_img2 = pg.transform.flip(bg_img, True, False) #背景画像
    hl_img = Hiroin((100, 400))

    show_hl_img = False
    # hl_img = pg.image.load("file.png")
    # hl_img = pg.transform.flip(hl_img, True, False)
    # kk_rect = hl_img.get_rect() #こうかとんrectの抽出
    # kk_rect.center = 300, 200
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                show_hl_img = not show_hl_img
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        if show_hl_img:
            hl_img.update(key_lst, screen)
        #     if event.type == pg.QUIT: return

        # x = tmr%3200
        # screen.blit(bg_img, [-x, 0]) #背景画像を表すsurfase
        # screen.blit(bg_img2, [-x+1600, 0])
        # screen.blit(bg_img, [-x+3200, 0]) #背景画像を表すsurfase
        # screen.blit(bg_img2, [-x+4800, 0])
        
        # kye_lst = pg.key.get_pressed()
        # if kye_lst[pg.K_UP]: #上矢印を押したとき
        #     a = -1
        #     b = -1
        # elif kye_lst[pg.K_DOWN]:
        #     a = -1
        #     b = +1
        # elif kye_lst[pg.K_LEFT]:
        #     a = -1
        #     b = 0
        # elif kye_lst[pg.K_RIGHT]:
        #     a = +2
        #     b = 0
        # else:
        #     a = -1
        #     b = 0
        # kk_rect.move_ip(a, b)
        # screen.blit(hl_img, kk_rect) #kk_imageをkk_rectの設定に従って貼り付け
        pg.display.update()
        # tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()