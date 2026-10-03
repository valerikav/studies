from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

result = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd")
result.raise_for_status()
data = result.json()
print(data[0])
print(data[0]['image'])
print(data[0]['name'])
print(data[0]['symbol'].upper())
print(f'{data[0]['current_price']} $')

root = Tk()
root.title('Cryptocurrency')
root.geometry('600x500')
frame1 = Frame(root)
frame2 = Frame(root)
frame1.pack(pady=10)
frame2.pack()
screen = Label(frame1, text='Курсы криптовалют', font = ('Arial Black', 12))
screen.pack()

rows = 10
images_refs = []
for i in range(rows):
    number = Label(frame2, text=f'{i + 1}', font='arial 10', anchor='w', width=3)
    number.grid(row=i*2, column=0, sticky="w")

    url = data[i]['image']
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.thumbnail((25, 25))
    imgtk = ImageTk.PhotoImage(img)
    icon = Label(frame2, image=imgtk)
    icon.grid(row=i*2, column=1, sticky="w")
    images_refs.append(imgtk)

    row_text = Text(frame2, height=1, width=25,
                    borderwidth=0, highlightthickness=0,
                    background=frame2.cget("bg"),
                    cursor="arrow", wrap="none")
    row_text.grid(row=i*2, column=2, sticky="w")
    row_text.tag_configure("name", font=("Arial", 10, "bold"), foreground="black")
    row_text.tag_configure("symbol", font=("Arial", 10), foreground="gray")
    row_text.insert("end", data[i]['name'], "name")
    row_text.insert("end", " ", "name")
    row_text.insert("end", data[i]['symbol'].upper(), "symbol")
    row_text.config(state="disabled")

    current_price = Label(frame2, text=f"{data[i]['current_price']} $",
                          font='arial 10', anchor='e')
    current_price.grid(row=i*2, column=3, sticky="e", padx=(0, 10))

    separator = Frame(frame2, height=1, bg="grey")
    separator.grid(row=i * 2 + 1, column=0, columnspan=4, sticky="ew", pady=2)

root.mainloop()