from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time
import threading


# Создание заголовков и строк таблицы
def create_rows():
    global rows_created

    # Создание заголовков
    Label(frame2, text='#',
          font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w")
    Label(frame2, text='Монета',
          font=("Arial", 8, "bold")).grid(row=0, column=1, sticky="w")
    Label(frame2, text='Цена',
          font=("Arial", 8, "bold")).grid(row=0, column=3, sticky="e")

    for i in range(rows):
        # Создание 10 номеров для таблицы
        number = Label(frame2, text=f'{i + 1}',
                       font=("Arial", 10), anchor='w', width=3)
        number.grid(row=(i + 1) * 2, column=0, sticky="w")

        # Создание ячейки для иконки валюты
        icon = Label(frame2)
        icon.grid(row=(i + 1) * 2, column=1, sticky="w")

        # Создание ячейки для названия и символа валюты
        name_text = Text(frame2, height=1, width=25,
                         borderwidth=0, highlightthickness=0,
                         background=frame2.cget("bg"),
                         cursor="arrow", wrap="none")
        name_text.grid(row=(i + 1) * 2, column=2, sticky="w")
        name_text.tag_configure("name", font=("Arial", 10, "bold"),
                                foreground="black")
        name_text.tag_configure("symbol", font=("Arial", 10),
                                foreground="grey")
        name_text.config(state="disabled")

        # Создание ячейки для цены валюты
        price = Label(frame2, text="", font=("Arial", 10), anchor='e')
        price.grid(row=(i + 1) * 2, column=3, sticky="e")

        # Создание разделителя между строками (для придания вида таблицы)
        separator = Frame(frame2, height=1, bg="grey")
        separator.grid(row=i * 2 + 1, column=0, columnspan=4,
                           sticky="ew", pady=2)

        labels.append({
            "number": number,
            "icon": icon,
            "name_text": name_text,
            "price": price,
            "separator": separator,
            "imgtk": None,
        })

    rows_created = True


# Фоновый поток
def fetch_all_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    result = requests.get(url, timeout=10)
    result.raise_for_status()
    data = result.json()

    images = []
    for i in range(rows):
        try:
            r = requests.get(data[i]['image'], timeout=5)
            r.raise_for_status()
            img = Image.open(BytesIO(r.content))
            img.thumbnail((25, 25))
            images.append(img)
        except Exception as e:
            print(f"Ошибка иконки {i}: {type(e).__name__}: {e}")
            images.append(None)

    return data, images


# Главный поток
def apply_data(data, images):
    if not rows_created:
        create_rows()

    for i, row in enumerate(labels):
        if images[i] is not None:
            imgtk = ImageTk.PhotoImage(images[i])
            row["icon"].config(image=imgtk)
            row["imgtk"] = imgtk
        else:
            row["icon"].config(image="")
            row["imgtk"] = None

        row["name_text"].config(state="normal")
        row["name_text"].delete("1.0", "end")
        row["name_text"].insert("end", data[i]['name'], "name")
        row["name_text"].insert("end", " ", "name")
        row["name_text"].insert("end", data[i]['symbol'].upper(), "symbol")
        row["name_text"].config(state="disabled")

        row["price"].config(text=f"{data[i]['current_price']} $")

    status.config(text=f"Обновлено в {time.strftime('%H:%M:%S')}", fg="gray")


# Ошибка обновления
def show_error(e):
    status.config(text="Не удалось обновить данные.", fg="red")
    print(f"[ERROR] {type(e).__name__}: {e}")


# Обновление в отдельном потоке
def update_price():
    status.config(text="Обновление…", fg="gray")

    def worker():
        try:
            data, images = fetch_all_data()
            root.after(0, lambda: apply_data(data, images))
        except Exception as e:
            root.after(0, lambda err=e: show_error(err))

    threading.Thread(target=worker, daemon=True).start()


# Обновление данных таблицы каждые 45 секунд
def run_update():
    update_price()
    root.after(45000, run_update)


labels = []
# Вывод топ-10 криптовалют
rows = 10

# Заголовки и строки таблицы еще не созданы
rows_created = False

# Создание графического интерфейса
root = Tk()
img = Image.open("icon.png")
icon_photo = ImageTk.PhotoImage(img)
root.iconphoto(True, icon_photo)
root.title('CoinGoin')
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
root_w = 500
root_h = 500
root.geometry(f'{root_w}x{root_h}+{screen_w // 2 - root_w // 2}'
              f'+{screen_h // 2 - root_h // 2}')
frame1 = Frame(root)
frame2 = Frame(root)
frame1.pack(pady=10)
frame2.pack()

headline = Label(frame1, text='Курсы криптовалют',
                 font=('Arial Black', 12), fg='DimGrey')
headline.pack(pady=10)

status = Label(root, text="", font=("Arial", 9), fg="gray")
status.pack(pady=20)

run_update()
root.mainloop()