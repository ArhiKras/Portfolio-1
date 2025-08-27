import customtkinter as ctk
from tkinter import messagebox # всплывающие окна с сообщениями

from code import add_task, add_task_button, delete_button, create_task_box

# интерфейс: выбор темы из библиотеки customtkinter
ctk.set_appearance_mode("light") # главная тема
ctk.set_default_color_theme("blue") # цвет кнопок

# параметры окна
root = ctk.CTk()
root.title("Scrum")
root.geometry("900x500")
root.minsize(700,400)
root.configure(fg_color="#F5F5F5") # замена дефолтной темы light на #F5F5F5

# заголовок
label_title = ctk.CTkLabel(root, text="Введите задачу:", font=("Arial", 14, Bold))
label_title.pack(pady=5)

# поле ввода
task_entry = ctk.CTkEntry(root, width=400, corner_radius=15, font=("Arial", 12))
task_entry.pack(pady=5)

# контейнер для кнопок поля ввода
btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(pady=5)

# кнопки поля ввода
add_task_button = ctk.CTkButton(btn_frame, text="Добавить задачу", corner_radius=20,)
add_task_button.pack(row=0, column=0, padx=10)

delete_button = ctk.CTkButton(btn_frame, text="Удалить задачу", corner_radius=20,)
delete_button.pack(row=0, column=1, padx=10)

# контейнер для списков/досок
frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(expand=True, fill="both", pady=10) # аргументы для расширения и заполнения

titles = ["Свободные", "В процессе", "Выполненные"]
colors = ["#D6EAF8", "#FCF3CF", "#D5F5E3"]

for i, title in enumerate(titles): # enumerate - получает индекс и значение для каждого заголовка
    ctk.CTkLabel(frame, text=title, font=("Arial", 14, "bold")).grid(row=0, column=i, padx=20, pady=5)
    frame.grid_columnconfigure(i, weight=1) # колонки равной ширины

# списки
free_list = create_task_box(frame, colors[0])
process_list = create_task_box(frame, colors[1])
done_list = create_task_box(frame, colors[2])

free_list.grid(row=1, column=0, padx=20, pady=5, sticky="nsew") # sticky="nsew" - растягивает во все стороны при изменении размера окна
process_list.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")
done_list.grid(row=1, column=2, padx=20, pady=5, sticky="nsew")

frame.grid_rowconfigure(1, weight=1) # позволяет строке растягиваться

# кнопки под списками
move_to_process = ctk.CTkButton(frame, text="▶ В работу", corner_radius=20,
                                command=lambda: move_task(free_list, process_list)) # анонимная функция для перемещения
move_to_process.grid(row=2, column=0, pady=5)

move_to_done = ctk.CTkButton(frame, text="▶ Выполнено", corner_radius=20,
                            command=lambda: move_task(process_list, done_list))
move_to_done.grid(row=2, column=1, pady=5)

move_back_to_free = ctk.CTkButton(frame, text="◀ Вернуть", corner_radius=20,
                                  command=lambda: move_task(process_list, free_list))
move_back_to_free.grid(row=3, column=1, pady=5)

move_back_to_process = ctk.CTkButton(frame, text="◀ Вернуть", corner_radius=20,
                                     command=lambda: move_task(done_list, process_list))
move_back_to_process.grid(row=2, column=2, pady=5)

root.mainloop()






