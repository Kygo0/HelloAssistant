import tkinter as tk

root = tk.Tk()
tk.Label(root, text="Some text").pack(padx=10, pady=10)
tk.Button(root, text="Quit", command=root.destroy).pack(padx=10, pady=10)


def on_destroy(event):
    if event.widget != root:
        return
    print("just closed")


root.bind("<Destroy>", on_destroy)
root.mainloop()
