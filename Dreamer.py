import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko= True
    if obj_rct.left < 0 or 1150 < obj_rct.right:
        yoko = False
    return yoko

class Hiroin:
    """
    ヒロインに関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_LEFT: (-10, 0),
        pg.K_RIGHT: (+10, 0),
    }

    imgs = {
        (+5, 0): pg.image.load("fig/file.png"),  # 初期画像を指定してください
        (-10, 0): pg.image.load("fig/file(0).png"),
        (+10, 0): pg.image.load("fig/file(1).png")
    }

    

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.gravity = 1
        self.is_jumping = False
        self.jump_speed = 15
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
            if self.rct.bottom >= 700:  # 地面に到達した場合
                self.rct.bottom = 700
                self.is_jumping = False
                self.jump_speed = 15
        self.rct.move_ip(sum_mv)
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)
        
        screen.blit(self.img, self.rct)

        yoko= check_bound(self.rct)
        if not yoko:
            self.rct.left = max(0, min(self.rct.left, 1200 - self.rct.width))

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)

        screen.blit(self.img, self.rct)

class Mika:
    """
    Mikaに関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_LEFT: (-10, 0),
        pg.K_RIGHT: (+10, 0),
    }

    imgs = {
        (+5, 0): pg.image.load("fig/mika.png"),  # 初期画像を指定してください
        (-10, 0): pg.image.load("fig/mika(0).png"),
        (+10, 0): pg.image.load("fig/mika(1).png")
    }

    

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.gravity = 1
        self.is_jumping = False
        self.jump_speed = 15
    def change_img(self, num: int, screen: pg.Surface):
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/mika({num}).png"), 0, 2.0)
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
            if self.rct.bottom >= 740:  # 地面に到達した場合
                self.rct.bottom = 740
                self.is_jumping = False
                self.jump_speed = 15
        self.rct.move_ip(sum_mv)
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)
        
        screen.blit(self.img, self.rct)


        yoko= check_bound(self.rct)
        if not yoko:
            self.rct.left = max(0, min(self.rct.left, 1200 - self.rct.width))
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs.get(tuple(sum_mv), self.img)

        screen.blit(self.img, self.rct)
def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((1200, 700))
    clock = pg.time.Clock()
    bg_img = pg.image.load("fig/24535830.jpg")  # 背景画像
    hl_img = Hiroin((100, 630))
    mk_img = Mika((100, 600))
    show_hl_img = False
    show_mk_img = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
            #     if event.key == pg.K_RETURN:
            #         show_hl_img = not show_hl_img
                if event.key == pg.K_2:
                    show_hl_img = True
                    show_mk_img = False
                elif event.key == pg.K_3:
                    show_mk_img = True
                    show_hl_img = False

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        if show_hl_img:
            hl_img.update(key_lst, screen)
        elif show_mk_img:
            mk_img.update(key_lst, screen)

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()