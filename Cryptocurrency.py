from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time


def run_update():
    update_price()
    root.after(60000, run_update)


def update_price():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
        result = requests.get(url, timeout=10)
        result.raise_for_status()
        data = result.json()
    except Exception as e:
        status.config(text=f"Ошибка: {e}", fg="red")
        return

    for i, row in enumerate(labels):

        try:
            img_url = data[i]['image']
            response = requests.get(img_url, timeout=5)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img.thumbnail((25, 25))
            imgtk = ImageTk.PhotoImage(img)
            row["icon"].config(image=imgtk)
            row["imgtk"] = imgtk
        except Exception as e:
            print(f"Ошибка иконки {i}: {e}")

        row["name_text"].config(state="normal")
        row["name_text"].delete("1.0", "end")
        row["name_text"].insert("end", data[i]['name'], "name")
        row["name_text"].insert("end", " ", "name")
        row["name_text"].insert("end", data[i]['symbol'].upper(), "symbol")
        row["name_text"].config(state="disabled")

        row["price"].config(text=f"{data[i]['current_price']} $")

    status.config(text=f"Обновлено в {time.strftime('%H:%M:%S')}", fg="gray")


root = Tk()
root.title('Cryptocurrency')
root.geometry('500x500')

frame1 = Frame(root)
frame2 = Frame(root)
frame1.pack(pady=10)
frame2.pack()


headline = Label(frame1, text='Курсы криптовалют', font=('Arial Black', 12), fg='DimGrey')
headline.pack(pady=10)

Label(frame2, text='#', font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w")
Label(frame2, text='Монета', font=("Arial", 8, "bold")).grid(row=0, column=1, sticky="w")
Label(frame2, text='Цена', font=("Arial", 8, "bold")).grid(row=0, column=3, sticky="e")

labels = []
rows = 10

for i in range(rows):
    number = Label(frame2, text=f'{i + 1}', font='arial 10', anchor='w', width=3)
    number.grid(row=(i + 1) * 2, column=0, sticky="w")

    icon = Label(frame2)
    icon.grid(row=(i + 1) * 2, column=1, sticky="w")

    name_text = Text(frame2, height=1, width=25,
                     borderwidth=0, highlightthickness=0,
                     background=frame2.cget("bg"),
                     cursor="arrow", wrap="none")
    name_text.grid(row=(i + 1) * 2, column=2, sticky="w")
    name_text.tag_configure("name", font=("Arial", 10, "bold"), foreground="black")
    name_text.tag_configure("symbol", font=("Arial", 10), foreground="grey")
    name_text.config(state="disabled")

    price = Label(frame2, text="", font='arial 10', anchor='e')
    price.grid(row=(i + 1) * 2, column=3, sticky="e")

    separator = Frame(frame2, height=1, bg="grey")
    separator.grid(row=i * 2 + 1, column=0, columnspan=4, sticky="ew", pady=2)

    labels.append({
        "number": number,
        "icon": icon,
        "name_text": name_text,
        "price": price,
        "separator": separator,
        "imgtk": None,
    })

status = Label(root, text="", font=("Arial", 9), fg="gray")
status.pack(pady=20)

run_update()

root.mainloop()