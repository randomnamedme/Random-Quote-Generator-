import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
quotes = []  # список всех цитат
history = []  # история сгенерированных цитат
author_filter_var = ""  # выбранный автор для фильтра
topic_filter_var = ""  # выбранная тема для фильтра

# Глобальные виджеты (чтобы к ним обращаться из функций)
quote_label = None
author_label = None
history_listbox = None
author_filter_combo = None
topic_filter_combo = None
quote_entry = None
author_entry = None
topic_entry = None
window = None


# ========== ПРЕДОПРЕДЕЛЁННЫЕ ЦИТАТЫ ==========
def init_quotes():
    global quotes
    quotes = [
        {"text": "Быть или не быть, вот в чём вопрос", "author": "Шекспир", "topic": "философия"},
        {"text": "Я мыслю, следовательно, существую", "author": "Декарт", "topic": "философия"},
        {"text": "Код — это поэзия", "author": "Неизвестный", "topic": "программирование"},
        {"text": "Жизнь — как коробка шоколада", "author": "Форрест Гамп", "topic": "мотивация"},
        {"text": "Учись или уходи", "author": "Мистер Мияги", "topic": "мотивация"},
        {"text": "Python > Java", "author": "Все гики", "topic": "программирование"},
        {"text": "Хакируй это!", "author": "Аноним", "topic": "хакинг"},
        {"text": "Сначала сделай, потом делай хорошо", "author": "Народная мудрость", "topic": "мотивация"},
        {"text": "Google — твой лучший друг", "author": "Программист", "topic": "программирование"},
    ]


# ========== РАБОТА С JSON ==========
def save_history():
    """Сохраняет историю в файл JSON"""
    global history
    try:
        with open("quote_history.json", "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
        print("История сохранена!")  # для отладки
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")


def load_history():
    """Загружает историю из файла JSON"""
    global history
    if os.path.exists("quote_history.json"):
        try:
            with open("quote_history.json", "r", encoding="utf-8") as file:
                history = json.load(file)
            print(f"Загружено {len(history)} цитат из истории")
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            history = []
    else:
        history = []
        print("Файл истории не найден, начинаем с пустой истории")


# ========== ОБНОВЛЕНИЕ ИСТОРИИ С ФИЛЬТРАМИ ==========
def update_history_display():
    """Обновляет список истории с учётом фильтров"""
    global history_listbox, author_filter_var, topic_filter_var

    # Очищаем список
    history_listbox.delete(0, tk.END)

    # Применяем фильтры
    filtered = history.copy()

    # Фильтр по автору
    if author_filter_var and author_filter_var != "Все":
        filtered = [q for q in filtered if q['author'] == author_filter_var]

    # Фильтр по теме
    if topic_filter_var and topic_filter_var != "Все":
        filtered = [q for q in filtered if q['topic'] == topic_filter_var]

    # Показываем результат
    if filtered:
        for quote in filtered:
            # Красиво форматируем
            text_preview = quote['text'][:40] + "..." if len(quote['text']) > 40 else quote['text']
            display_text = f"{quote['date']} | {quote['author']} | {quote['topic']} | \"{text_preview}\""
            history_listbox.insert(tk.END, display_text)
    else:
        history_listbox.insert(tk.END, "😢 Нет цитат в истории или по фильтру ничего не найдено")


def update_filters():
    """Обновляет выпадающие списки для фильтров"""
    global author_filter_combo, topic_filter_combo, quotes

    # Собираем уникальных авторов и темы
    authors = sorted(set([q['author'] for q in quotes]))
    topics = sorted(set([q['topic'] for q in quotes]))

    # Обновляем комбобоксы
    author_filter_combo['values'] = ["Все"] + authors
    topic_filter_combo['values'] = ["Все"] + topics


# ========== ГЛАВНЫЕ ФУНКЦИИ ==========
def generate_quote():
    """Генерирует случайную цитату"""
    global quotes, history, quote_label, author_label

    if not quotes:
        messagebox.showwarning("Ой!", "Нет ни одной цитаты! Добавь сначала ❤️")
        return

    # Выбираем случайную цитату
    random_quote = random.choice(quotes)

    # Отображаем
    quote_label.config(text=f"✨ \"{random_quote['text']}\" ✨")
    author_label.config(text=f"— {random_quote['author']} ({random_quote['topic']})")

    # Добавляем в историю
    history_entry = {
        "text": random_quote['text'],
        "author": random_quote['author'],
        "topic": random_quote['topic'],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history.append(history_entry)

    # Сохраняем и обновляем
    save_history()
    update_history_display()


def add_quote():
    """Добавляет новую цитату от пользователя"""
    global quote_entry, author_entry, topic_entry, quotes

    # Получаем текст из полей
    text = quote_entry.get("1.0", tk.END).strip()
    author = author_entry.get().strip()
    topic = topic_entry.get().strip()

    # ПРОВЕРКА НА ПУСТЫЕ СТРОКИ (как просили в задании!)
    if not text:
        messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
        return
    if not author:
        messagebox.showerror("Ошибка", "Укажи автора цитаты!")
        return
    if not topic:
        messagebox.showerror("Ошибка", "Укажи тему цитаты!")
        return

    # Добавляем новую цитату
    new_quote = {"text": text, "author": author, "topic": topic}
    quotes.append(new_quote)

    # Очищаем поля ввода
    quote_entry.delete("1.0", tk.END)
    author_entry.delete(0, tk.END)
    topic_entry.delete(0, tk.END)

    # Обновляем фильтры
    update_filters()

    messagebox.showinfo("Успех! 🎉", f"Цитата добавлена!\nВсего цитат: {len(quotes)}")


def apply_author_filter(event=None):
    """Применяет фильтр по автору"""
    global author_filter_var, author_filter_combo
    author_filter_var = author_filter_combo.get()
    update_history_display()


def apply_topic_filter(event=None):
    """Применяет фильтр по теме"""
    global topic_filter_var, topic_filter_combo
    topic_filter_var = topic_filter_combo.get()
    update_history_display()


def reset_filters():
    """Сбрасывает все фильтры"""
    global author_filter_var, topic_filter_var, author_filter_combo, topic_filter_combo
    author_filter_var = "Все"
    topic_filter_var = "Все"
    author_filter_combo.set("Все")
    topic_filter_combo.set("Все")
    update_history_display()


def clear_history():
    """Очищает всю историю"""
    global history
    if messagebox.askyesno("Подтверждение", "Точно удалить всю историю? 😢"):
        history = []
        save_history()
        update_history_display()
        messagebox.showinfo("Готово!", "История очищена!")


def delete_last_quote():
    """Удаляет последнюю цитату из истории"""
    global history
    if history:
        if messagebox.askyesno("Подтверждение", f"Удалить последнюю цитату?\n\"{history[-1]['text'][:50]}...\""):
            history.pop()
            save_history()
            update_history_display()
            messagebox.showinfo("Готово!", "Последняя цитата удалена!")
    else:
        messagebox.showwarning("Пусто", "История и так пустая!")


# ========== СОЗДАНИЕ ИНТЕРФЕЙСА ==========
def create_interface():
    global window, quote_label, author_label, history_listbox
    global author_filter_combo, topic_filter_combo
    global quote_entry, author_entry, topic_entry

    # Главное окно
    window = tk.Tk()
    window.title("🎲 Random Quote Generator - Твой личный цитатник")
    window.geometry("800x700")
    window.config(bg="#1a1a2e")

    # Заголовок
    title_label = tk.Label(window, text="🌟 ГЕНЕРАТОР СЛУЧАЙНЫХ ЦИТАТ 🌟",
                           font=("Arial", 16, "bold"), bg="#1a1a2e", fg="#e94560")
    title_label.pack(pady=10)

    # === РАМКА С ЦИТАТОЙ ===
    quote_frame = tk.Frame(window, bg="#16213e", relief=tk.RAISED, bd=3)
    quote_frame.pack(pady=15, padx=20, fill=tk.X)

    quote_label = tk.Label(quote_frame, text="🔥 Нажми кнопку, чтобы получить вдохновение! 🔥",
                           font=("Comic Sans MS", 13, "italic"), wraplength=700,
                           bg="#16213e", fg="#e2e2e2")
    quote_label.pack(pady=20, padx=20)

    author_label = tk.Label(quote_frame, text="", font=("Arial", 11, "bold"),
                            bg="#16213e", fg="#f5a623")
    author_label.pack(pady=(0, 15))

    # === КНОПКА ГЕНЕРАЦИИ ===
    generate_btn = tk.Button(window, text="🎲 СГЕНЕРИРОВАТЬ ЦИТАТУ 🎲",
                             command=generate_quote, font=("Arial", 12, "bold"),
                             bg="#e94560", fg="white", padx=20, pady=10,
                             activebackground="#c73b54", cursor="hand2")
    generate_btn.pack(pady=10)

    # === ДОБАВЛЕНИЕ СВОЕЙ ЦИТАТЫ ===
    add_frame = tk.LabelFrame(window, text="📝 Добавить свою цитату",
                              bg="#1a1a2e", fg="#e2e2e2", font=("Arial", 10, "bold"))
    add_frame.pack(pady=10, padx=20, fill=tk.X)

    # Текст цитаты
    tk.Label(add_frame, text="Текст:", bg="#1a1a2e", fg="#e2e2e2").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    quote_entry = tk.Text(add_frame, height=3, width=60, font=("Arial", 10))
    quote_entry.grid(row=0, column=1, padx=5, pady=5)

    # Автор
    tk.Label(add_frame, text="Автор:", bg="#1a1a2e", fg="#e2e2e2").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    author_entry = tk.Entry(add_frame, width=40, font=("Arial", 10))
    author_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Тема
    tk.Label(add_frame, text="Тема:", bg="#1a1a2e", fg="#e2e2e2").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    topic_entry = tk.Entry(add_frame, width=40, font=("Arial", 10))
    topic_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Кнопка добавления
    add_btn = tk.Button(add_frame, text="➕ Добавить в коллекцию", command=add_quote,
                        bg="#0f3460", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
    add_btn.grid(row=3, column=0, columnspan=2, pady=10)

    # === ФИЛЬТРАЦИЯ ===
    filter_frame = tk.LabelFrame(window, text="🔍 Фильтровать историю",
                                 bg="#1a1a2e", fg="#e2e2e2", font=("Arial", 10, "bold"))
    filter_frame.pack(pady=10, padx=20, fill=tk.X)

    tk.Label(filter_frame, text="По автору:", bg="#1a1a2e", fg="#e2e2e2").grid(row=0, column=0, padx=5, pady=5)
    author_filter_combo = ttk.Combobox(filter_frame, state="readonly", width=20)
    author_filter_combo.grid(row=0, column=1, padx=5, pady=5)
    author_filter_combo.bind("<<ComboboxSelected>>", apply_author_filter)

    tk.Label(filter_frame, text="По теме:", bg="#1a1a2e", fg="#e2e2e2").grid(row=0, column=2, padx=5, pady=5)
    topic_filter_combo = ttk.Combobox(filter_frame, state="readonly", width=20)
    topic_filter_combo.grid(row=0, column=3, padx=5, pady=5)
    topic_filter_combo.bind("<<ComboboxSelected>>", apply_topic_filter)

    # Кнопка сброса
    reset_btn = tk.Button(filter_frame, text="🔄 Сбросить фильтры", command=reset_filters,
                          bg="#533483", fg="white", cursor="hand2")
    reset_btn.grid(row=0, column=4, padx=10, pady=5)

    # === ИСТОРИЯ ===
    history_frame = tk.LabelFrame(window, text="📜 История (последние цитаты)",
                                  bg="#1a1a2e", fg="#e2e2e2", font=("Arial", 10, "bold"))
    history_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Скроллбар
    scroll = tk.Scrollbar(history_frame)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    history_listbox = tk.Listbox(history_frame, yscrollcommand=scroll.set,
                                 font=("Consolas", 9), height=10,
                                 bg="#0f3460", fg="#e2e2e2", selectbackground="#e94560")
    history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    scroll.config(command=history_listbox.yview)

    # === КНОПКИ УПРАВЛЕНИЯ ===
    button_frame = tk.Frame(window, bg="#1a1a2e")
    button_frame.pack(pady=10)

    clear_btn = tk.Button(button_frame, text="🗑️ Очистить всю историю", command=clear_history,
                          bg="#c0392b", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
    clear_btn.pack(side=tk.LEFT, padx=5)

    delete_last_btn = tk.Button(button_frame, text="⏪ Удалить последнюю", command=delete_last_quote,
                                bg="#f39c12", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
    delete_last_btn.pack(side=tk.LEFT, padx=5)

    # Статус бар
    status_label = tk.Label(window, text=f"📚 Всего цитат в базе: {len(quotes)}",
                            bg="#1a1a2e", fg="#95a5a6", font=("Arial", 9))
    status_label.pack(side=tk.BOTTOM, pady=5)

    # Обновляем статус при добавлении цитат (хитрость: будем обновлять в add_quote)
    def update_status():
        status_label.config(text=f"📚 Всего цитат в базе: {len(quotes)}")
        window.after(1000, update_status)  # обновляем каждую секунду

    update_status()


# ========== ЗАПУСК ==========
def main():
    """Главная функция запуска программы"""
    # Инициализируем данные
    init_quotes()
    load_history()

    # Создаём интерфейс
    create_interface()

    # Обновляем фильтры после создания интерфейса
    update_filters()

    # Показываем историю
    update_history_display()

    # Запускаем главный цикл
    window.mainloop()


# Запускаем программу
if __name__ == "__main__":
    main()