import tkinter as tk
import time
import random
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter

color = [[(255, 177, 177), (255, 220, 220)],
         [(177, 255, 177), (220, 255, 220)],
         [(255, 140, 70), (255, 222, 170)],
         [(255, 255, 160), (255, 255, 200)],
         [(255, 160, 255), (255, 200, 255)],
         [(160, 255, 255), (200, 255, 255)]]

file_lrc = input('Your lyrics file (.lrc):\n')
# file_song = 'song.mp3'
fontfile = input('Your font file:\n')
# player = "D:\\Softwares\\PotPlayer\\PotPlayerMini64.exe"


def enter(event):
    win.attributes('-fullscreen', True)


def quit(event):
    win.attributes('-fullscreen', False)


def show_label(event):
    win.overrideredirect(False)


def hide_label(event):
    win.overrideredirect(True)


def draw_letter(image, letter, x, y, c, font, method):
    draw = ImageDraw.Draw(image)
    draw.text((x, y), letter, fill=color[c][method], font=font)
    xs = draw.textlength(letter, font=font)
    return x+xs


def cut(text):
    if len(text) > 25:
        count = 0
        former_count = -1
        out_text = ''
        word = ''
        for l in text:
            if l == ' ':
                if count >= 25:
                    out_text += '\n'
                    count = count - former_count - 1
                former_count = count
                out_text += word
                out_text += ' '
                word = ''
            else:
                word += l
            count += 1
        out_text += word
    else:
        out_text = text
    while out_text[-1] == '\n':
        out_text = out_text[:-1]
    return out_text


def get_size(image, text):
    font = ImageFont.truetype(fontfile, size=400)
    draw = ImageDraw.Draw(image)
    x0, y0, x1, y1 = draw.multiline_textbbox((0, 0), text, font=font, spacing=0, align='center')
    xs = x1 - x0
    ys = y1 - y0
    new_size_x = int((w - 100) / xs * 400)
    new_size_y = int((h - 100) / ys * 400)
    return min(400, new_size_x, new_size_y)


def write_line(y, text, font, image, method, c):
    draw = ImageDraw.Draw(image)
    xs = draw.textlength(text, font=font)
    x = w / 2 - xs / 2
    for i in range(len(text)):
        x = draw_letter(image, text[i], x, y, c[i], font, method)
    return 0


def write_lines(text):
    text = cut(text)

    image = Image.new('RGB', (w, h), color=(0, 0, 0))
    size = get_size(image, text)
    font = ImageFont.truetype(fontfile, size=size)

    draw = ImageDraw.Draw(image)
    _, y0, _, y1 = draw.multiline_textbbox((0, 0), text, font=font, align='center')
    ys = y1 - y0
    yc = h / 2 - ys / 2 - y0
    text_list = text.split('\n')
    ny = len(text_list)
    dy = ys / ny

    c = []
    for i in range(ny):
        c.append([])
        for j in range(len(text_list[i])):
            c[i].append(random.randint(0, 5))

    for i in range(ny):
        write_line(yc + dy * i, text_list[i], font, image, 0, c[i])

    image = image.filter(ImageFilter.GaussianBlur(10))

    for i in range(ny):
        write_line(yc + dy * i, text_list[i], font, image, 0, c[i])

    image = image.filter(ImageFilter.GaussianBlur(10))

    for i in range(ny):
        write_line(yc + dy * i, text_list[i], font, image, 1, c[i])

    return image


def play_song():
    subprocess.run([player, file_song])


def play_lyrics():
    f = open(file_lrc, "r", encoding='utf-8')
    flag = False
    label = tk.Label(win)
    label.pack()
    time_start = time.time()
    for line in f.readlines():
        if not flag:
            if '[00:' in line:
                flag = True
                time_start = time.time()
        if flag:
            show_time = float(line[1:3]) * 60 + float(line[4:9])
            while True:
                if (time.time() - time_start) > show_time:
                    break
            img = ImageTk.PhotoImage(write_lines(cut(line[10:-1])))
            label.config(imag=img)
            win.update()


win = tk.Tk()
# win.overrideredirect(True)
w = win.winfo_screenwidth()
h = win.winfo_screenheight()
win.geometry("%dx%d" % (w, h))
win.bind('<Return>', enter)
win.bind('<Escape>', quit)
win.bind('<Button-1>', show_label)
win.bind('<Button-3>', hide_label)
play_lyrics()
win.mainloop()


# def main():
#     p1 = multiprocessing.Process(target=play_song)
#     p2 = multiprocessing.Process(target=play_lyrics)
#     p1.start()
#     p2.start()
#
#
# if __name__ == '__main__':
#     main()
    # win.mainloop()




