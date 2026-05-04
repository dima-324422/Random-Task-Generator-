    # История задач (загружается при старте)
    self.history = []
    self.load_history()

    # --- Создание виджетов ---
    self.create_widgets()

def create_widgets(self):
    # Рамка для кнопки генерации
    frame_generate = tk.Frame(self.root)
    frame_generate.pack(pady=10)

    self.btn_generate = tk.Button(
        frame_generate,
        text="Сгенерировать задачу",
        font=("Arial", 12),
        command=self.generate_task
    )
    self.btn_generate.pack()

    # Рамка для добавления новой задачи
    frame_add = tk.LabelFrame(self.root, text="Добавить новую задачу", padx=10, pady=5)
    frame_add.pack(pady=10, fill="x")

    tk.Label(frame_add, text="Задача:").grid(row=0, column=0, sticky="e")
    self.entry_task = tk.Entry(frame_add, width=30)
    self.entry_task.grid(row=0, column=1, padx=5)

    tk.Label(frame_add, text="Категория:").grid(row=1, column=0, sticky="e")
    self.category_var = tk.StringVar(value="учёба")
    category_menu = ttk.Combobox(frame_add, textvariable=self.category_var, 
                                values=list(TASKS.keys()), state="readonly", width=27)
    category_menu.grid(row=1, column=1, padx=5)

    btn_add = tk.Button(frame_add, text="Добавить", command=self.add_new_task)
    btn_add.grid(row=2, column=0, columnspan=2, pady=5)

    # Рамка для истории и фильтрации
    frame_history = tk.LabelFrame(self.root, text="История задач", padx=10, pady=5)
    frame_history.pack(pady=10, fill="both", expand=True)

    # Фильтр по категории
    filter_frame = tk.Frame(frame_history)
    filter_frame.pack(pady=5)
    
    tk.Label(filter_frame, text="Фильтр:").pack(side="left")
    self.filter_var = tk.StringVar(value="все")
    filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                              values=["все"] + list(TASKS.keys()), state="readonly", width=15)
    filter_menu.pack(side="left", padx=5)
    
    btn_apply_filter = tk.Button(filter_frame, text="Применить", command=self.apply_filter)
    btn_apply_filter.pack(side="left")

    # Виджет для отображения истории (Listbox с полосой прокрутки)
    scrollbar = tk.Scrollbar(frame_history)
    scrollbar.pack(side="right", fill="y")

    self.history_display = tk.Listbox(
        frame_history,
        yscrollcommand=scrollbar.set,
        height=15,
        font=("Arial", 10),
        selectmode=tk.SINGLE
    )
    self.history_display.pack(fill="both", expand=True)
    scrollbar.config(command=self.history_display.yview)

    # Кнопки сохранения и загрузки
    btn_frame = tk.Frame(self.root)
    btn_frame.pack(pady=10)
    
    btn_save = tk.Button(btn_frame, text="Сохранить историю", command=self.save_history)
    btn_save.pack(side="left", padx=5)
    
    btn_load = tk.Button(btn_frame, text="Загрузить историю", command=self.load_history_gui)
    btn_load.pack(side="left", padx=5)
    
# --- Логика приложения ---
def generate_task(self):
    """Генерирует случайную задачу из всех категорий."""
    all_tasks = [task for sublist in TASKS.values() for task in sublist]
    task = random.choice(all_tasks)
    
    # Добавляем в историю и обновляем отображение
    self.history.append(task)
    self.update_history_display()

def add_new_task(self):
    """Добавляет новую задачу в словарь TASKS."""
    new_task = self.entry_task.get().strip()
    
    if not new_task:
        messagebox.showwarning("Ошибка", "Поле задачи не может быть пустым!")
        return

    category = self.category_var.get()
    
    if category not in TASKS:
        TASKS[category] = []
        
    TASKS[category].append(new_task)
    
    # Очищаем поле ввода и обновляем меню категорий (если добавлена новая категория)
    self.entry_task.delete(0, tk.END)
    
def update_history_display(self):
    """Обновляет виджет Listbox в соответствии с текущим фильтром."""
    self.history_display.delete(0, tk.END)
    
    selected_filter = self.filter_var.get()
    
    for task in self.history:
        if selected_filter == "все":
            self.history_display.insert(tk.END, task)
        else:
            # Проверяем, принадлежит ли задача выбранной категории
            if task in TASKS.get(selected_filter, []):
                self.history_display.insert(tk.END, task)

def apply_filter(self):
    """Применяет выбранный фильтр к истории."""
    self.update_history_display()

def save_history(self):
    """Сохраняет историю в файл JSON."""
    try:
        with open("history.json", "w") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "История сохранена в файл history.json")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", str(e))

def load_history(self):
    """Загружает историю при старте приложения (без окна)."""
    try:
        if os.path.exists("history.json"):
            with open("history.json", "r") as f:
                self.history = json.load(f)
            self.update_history_display()
            print("История успешно загружена при старте.")
        else:
            print("Файл истории не найден. Будет создан при первом сохранении.")
            self.history = []
            self.update_history_display()
            
            # Создаем пустой файл для удобства Git (опционально)
            with open("history.json", "w") as f:
                json.dump([], f)
            
    except Exception as e:
        messagebox.showerror("Ошибка загрузки", f"Ошибка при автозагрузке: {e}")
        self.history = []

def load_history_gui(self):
    """Загружает историю по нажатию кнопки (с обновлением интерфейса)."""
    try:
        with open("history.json", "r") as f:
            self.history = json.load(f)
        self.update_history_display()
        messagebox.showinfo("Успех", "История загружена из файла history.json")
        
        # Сохраняем пустой список в файл, если он был пустым или отсутствовал (для Git)
        if not os.path.exists("history.json"):
            with open("history.json", "w") as f:
                json.dump([], f)
            
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл history.json не найден. Сначала сохраните историю.")
        # Создаем пустой файл для удобства Git (опционально)
        with open("history.json", "w") as f:
            json.dump([], f)
        
