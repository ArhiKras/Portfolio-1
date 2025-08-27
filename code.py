import customtkinter as ctk
from tkinter import messagebox

def add_task():
    task = task_entry.get().strip()
    if task:
        backlog_list.insert("end", task + "\n")
        task_entry.delete(0, "end")
    else:
        messagebox.showwarning("Ошибка", "Введите название задачи!")

def move_task(source, target):
    try:
        # Получаем выделенный текст (задачу)
        if source.tag_ranges("sel"):
            start_index = source.index("sel.first")
            end_index = source.index("sel.last")
            task = source.get(start_index, end_index)
            source.delete(start_index, end_index)
            target.insert("end", task + "\n")
        else:
            # Если нет выделения, используем курсор
            cursor_pos = source.index("insert")
            line_start = cursor_pos.split('.')[0] + '.0'
            line_end = cursor_pos.split('.')[0] + '.end'
            task = source.get(line_start, line_end).strip()
            if task:
                source.delete(line_start, line_end)
                target.insert("end", task + "\n")
    except Exception:
        pass

def delete_task():
    for box in (backlog_list, progress_list, done_list):
        try:
            if box.tag_ranges("sel"):
                start_index = box.index("sel.first")
                end_index = box.index("sel.last")
                box.delete(start_index, end_index)
                break
            else:
                cursor_pos = box.index("insert")
                line_start = cursor_pos.split('.')[0] + '.0'
                line_end = cursor_pos.split('.')[0] + '.end'
                task = box.get(line_start, line_end).strip()
                if task:
                    box.delete(line_start, line_end)
                    break
        except Exception:
            continue

def create_task_box(parent, bg_color):
    """CTkTextbox с черной рамкой и закруглёнными углами без внутреннего фрейма"""
    box = ctk.CTkTextbox(parent,
                         height=200,
                         width=220,
                         corner_radius=15,
                         fg_color=bg_color,
                         border_width=2,
                         border_color="black",
                         font=("Arial", 12),
                         wrap="word")
    return box

# ---------- Интерфейс ----------
ctk.set_appearance_mode("light")  # светлая тема
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Scrum Task Board")
root.geometry("900x500")
root.minsize(700, 400)
root.configure(fg_color="#F5F5F5")  # вернули спокойный светлый фон

# Заголовок
label_title = ctk.CTkLabel(root, text="Введите задачу:", font=("Arial", 14, "bold"))
label_title.pack(pady=5)

task_entry = ctk.CTkEntry(root, width=400, corner_radius=15, font=("Arial", 12))
task_entry.pack(pady=5)

btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(pady=5)

add_task_button = ctk.CTkButton(btn_frame, text="Добавить задачу", command=add_task, corner_radius=20)
add_task_button.grid(row=0, column=0, padx=10)

delete_button = ctk.CTkButton(btn_frame, text="Удалить задачу", command=delete_task, corner_radius=20)
delete_button.grid(row=0, column=1, padx=10)

# ---------- Scrum-доска ----------
frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(expand=True, fill="both", pady=10)

titles = ["Backlog", "In Progress", "Done"]
colors = ["#D6EAF8", "#FCF3CF", "#D5F5E3"]  # спокойная цветовая гамма

for i, title in enumerate(titles):
    ctk.CTkLabel(frame, text=title, font=("Arial", 14, "bold")).grid(row=0, column=i, padx=20, pady=5)
    frame.grid_columnconfigure(i, weight=1)

# Создаем списки задач
backlog_list = create_task_box(frame, colors[0])
progress_list = create_task_box(frame, colors[1])
done_list = create_task_box(frame, colors[2])

backlog_list.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
progress_list.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")
done_list.grid(row=1, column=2, padx=20, pady=5, sticky="nsew")

frame.grid_rowconfigure(1, weight=1)

# ---------- Кнопки под колонками ----------
move_to_progress = ctk.CTkButton(frame, text="▶ В работу",
                                 command=lambda: move_task(backlog_list, progress_list),
                                 corner_radius=20)
move_to_progress.grid(row=2, column=0, pady=5)

move_to_done = ctk.CTkButton(frame, text="▶ Выполнено",
                             command=lambda: move_task(progress_list, done_list),
                             corner_radius=20)
move_to_done.grid(row=2, column=1, pady=5)

move_back_to_backlog = ctk.CTkButton(frame, text="◀ Вернуть",
                                     command=lambda: move_task(progress_list, backlog_list),
                                     corner_radius=20)
move_back_to_backlog.grid(row=3, column=1, pady=5)

move_back_to_progress = ctk.CTkButton(frame, text="◀ Вернуть",
                                      command=lambda: move_task(done_list, progress_list),
                                      corner_radius=20)
move_back_to_progress.grid(row=2, column=2, pady=5)

root.mainloop()