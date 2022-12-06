import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from operator import itemgetter


def main_screen():


    root = tk.Tk()
    root.title("Login")
    style = ttk.Style(root)
    style.theme_names()
    style.theme_use("winnative")
    root.geometry('1000x700')
    root.pack_propagate(False)
    root.resizable(0, 0)
    filename = "employees_with_info.csv"
    col_l = ["First Name", "Last Name", "Address", "City", "State"]

    style_tree = ttk.Style()
    style_button = ttk.Style()
    style_tree.configure("t_style.Treeview", font=('calibri', 14), rowheight=25)
    style_tree.configure("t_style.Treeview.Heading",  font=('calibri', 16), background="thistle2")

    frame1 = tk.LabelFrame(root, text="Excel Data")
    frame1.place(height=500, width=1000)

    file_frame = tk.LabelFrame(root, text="Search Fields")
    file_frame.place(height=150, width=500, rely=0.75, relx=.25)

    clicked = tk.StringVar()
    clicked.set(str(col_l[0]))
    drop = tk.OptionMenu(file_frame, clicked, *col_l)
    drop.config(width=15, font=("calibri", 14), background="orange2", activebackground="DarkGoldenrod2")
    drop.place(rely=.35, relx=.5)
    drop['menu'].config(font=('calibri', 12), bg='DarkGoldenrod2')

    entry_s = tk.Entry(file_frame)
    entry_s.config(font=("calibri", 14), width=15)
    entry_s.place(rely=0.4, relx=0.15)

    tv1 = ttk.Treeview(frame1, style="t_style.Treeview")
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly)
    treescrollx.pack(side="bottom", fill="x")
    treescrolly.pack(side="right", fill="y")

    nf = pd.read_csv(filename)
    df = nf.loc[:, ["first_name", "last_name", "address", "city", "state"]]
    df = df.sort_values(by="first_name")



    tv1["column"] = col_l
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)

    def s_data(*args):
        clear_data()
        le = len(entry_s.get())
        # print(le)
        count = 0
        tv1.tag_configure('odd_row', background="white")
        tv1.tag_configure('even_row', background="light blue")
        if le == 0:
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                if count % 2 == 0:
                    tv1.insert("", "end", values=row, tags=("even_row", ))
                else:
                    tv1.insert("", "end", values=row, tags=("odd_row", ))
                count += 1
        else:
            # print("in here woot")
            s_key = col_l.index(str(clicked.get()))
            s_list = []
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                val = row[s_key]
                if entry_s.get().lower() == val[0:le].lower():
                    s_list.append(row)
            # print(s_list)
            s_list = sorted(s_list, key=itemgetter(s_key))
            for row in s_list:
                if count % 2 == 0:
                    tv1.insert("", "end", values=row, tags=("even_row",))
                else:
                    tv1.insert("", "end", values=row, tags=("odd_row",))
                count += 1

    entry_s.bind("<KeyRelease>", s_data)

    def clear_data():
        tv1.delete(*tv1.get_children())

    root.mainloop()


if __name__ == "__main__":
    main_screen()

