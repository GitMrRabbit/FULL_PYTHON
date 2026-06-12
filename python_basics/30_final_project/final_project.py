"""
Урок 30: Финальный проект — Консольное приложение
===================================================

Мини-приложение "Менеджер задач" (Task Manager).
Объединяет: ООП, файлы, JSON, даты, comprehensions, type hints, исключения.

Возможности:
  - Добавление, удаление, редактирование задач
  - Фильтрация по статусу, приоритету, дате
  - Сохранение/загрузка в JSON
  - Поиск по ключевым словам
  - Статистика
"""

import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum


# =============================================================================
# МОДЕЛИ
# =============================================================================

class Priority(Enum):
    LOW = "низкий"
    MEDIUM = "средний"
    HIGH = "высокий"
    CRITICAL = "критический"


class Status(Enum):
    TODO = "к выполнению"
    IN_PROGRESS = "в работе"
    DONE = "выполнено"
    CANCELLED = "отменено"


@dataclass
class Task:
    """Модель задачи."""
    id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    due_date: str | None = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["priority"] = self.priority.name
        d["status"] = self.status.name
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        d = dict(d)  # Копия
        d["priority"] = Priority[d["priority"]]
        d["status"] = Status[d["status"]]
        return cls(**d)

    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.fromisoformat(self.due_date).date() < date.today()


# =============================================================================
# РЕПОЗИТОРИЙ
# =============================================================================

class TaskRepository:
    """Хранение и управление задачами (in-memory + JSON)."""

    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = Path(storage_path)
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> Task:
        if task.id == 0:
            task.id = self._next_id
            self._next_id += 1
        self._tasks[task.id] = task
        return task

    def get(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, task_id: int, **kwargs) -> Task | None:
        task = self._tasks.get(task_id)
        if not task:
            return None
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        return task

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def filter(self, status: Status | None = None,
               priority: Priority | None = None,
               tag: str | None = None) -> list[Task]:
        tasks = self.get_all()
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if tag:
            tasks = [t for t in tasks if tag in t.tags]
        return tasks

    def search(self, query: str) -> list[Task]:
        q = query.lower()
        return [t for t in self.get_all()
                if q in t.title.lower() or q in t.description.lower()]

    def get_stats(self) -> dict:
        tasks = self.get_all()
        total = len(tasks)
        by_status = {s: 0 for s in Status}
        for t in tasks:
            by_status[t.status] += 1
        overdue = sum(1 for t in tasks if t.is_overdue())
        return {
            "total": total,
            "by_status": {s.name: c for s, c in by_status.items()},
            "overdue": overdue,
        }

    def save(self) -> None:
        data = {
            "tasks": [t.to_dict() for t in self._tasks.values()],
            "next_id": self._next_id,
        }
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def load(self) -> None:
        if not self.storage_path.exists():
            return
        data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        self._next_id = data["next_id"]
        self._tasks = {
            t["id"]: Task.from_dict(t) for t in data["tasks"]
        }


# =============================================================================
# КОНСОЛЬНЫЙ ИНТЕРФЕЙС
# =============================================================================

class TaskManagerApp:
    """Консольное приложение."""

    def __init__(self):
        self.repo = TaskRepository()
        self.repo.load()
        self._commands = {
            "list": self.cmd_list,
            "add": self.cmd_add,
            "done": self.cmd_done,
            "delete": self.cmd_delete,
            "search": self.cmd_search,
            "stats": self.cmd_stats,
            "save": self.cmd_save,
            "help": self.cmd_help,
            "exit": self.cmd_exit,
        }

    def run(self):
        print("\n📋 МЕНЕДЖЕР ЗАДАЧ v1.0")
        print("Введите 'help' для списка команд, 'exit' для выхода.\n")
        while True:
            try:
                raw = input(">>> ").strip()
                if not raw:
                    continue
                parts = raw.split(maxsplit=1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if cmd in self._commands:
                    should_exit = self._commands[cmd](args)
                    if should_exit:
                        break
                else:
                    print(f"Неизвестная команда: {cmd}. Введите 'help'.")
            except KeyboardInterrupt:
                print("\nДо свидания!")
                break
            except Exception as e:
                print(f"[!] Ошибка: {e}")

    def cmd_help(self, _) -> None:
        print("""
Команды:
  list [status]     — Показать задачи (all/todo/in_progress/done)
  add               — Добавить задачу (интерактивно)
  done <id>         — Отметить задачу как выполненную
  delete <id>       — Удалить задачу
  search <запрос>   — Поиск по задачам
  stats             — Статистика
  save              — Сохранить в файл
  help              — Эта справка
  exit              — Выход (с сохранением)
        """.strip())

    def cmd_list(self, args: str) -> None:
        status = None
        if args:
            try:
                status = Status[args.upper()]
            except KeyError:
                print(f"Неизвестный статус: {args}")
                return
        tasks = self.repo.filter(status=status) if status else self.repo.get_all()
        if not tasks:
            print("Задач нет.")
            return
        for t in tasks:
            overdue = " 🔴" if t.is_overdue() else ""
            print(f"  [{t.id}] {t.status.value:12s} | {t.priority.value:10s} | "
                  f"{t.title[:40]}{overdue}")

    def cmd_add(self, _) -> None:
        title = input("  Название: ").strip()
        if not title:
            print("Название не может быть пустым.")
            return
        desc = input("  Описание: ").strip()
        task = Task(id=0, title=title, description=desc)
        self.repo.add(task)
        print(f"  [+] Задача #{task.id} добавлена!")

    def cmd_done(self, args: str) -> None:
        if not args.isdigit():
            print("Укажите ID задачи: done 5")
            return
        task = self.repo.update(int(args), status=Status.DONE)
        if task:
            print(f"  [✓] Задача #{task.id} отмечена выполненной!")
        else:
            print(f"  [!] Задача #{args} не найдена.")

    def cmd_delete(self, args: str) -> None:
        if not args.isdigit():
            print("Укажите ID задачи: delete 5")
            return
        if self.repo.delete(int(args)):
            print(f"  [✗] Задача #{args} удалена.")
        else:
            print(f"  [!] Задача #{args} не найдена.")

    def cmd_search(self, args: str) -> None:
        if not args:
            print("Укажите поисковый запрос: search python")
            return
        results = self.repo.search(args)
        if results:
            print(f"Найдено ({len(results)}):")
            for t in results:
                print(f"  [{t.id}] {t.title} — {t.description[:50]}")
        else:
            print("Ничего не найдено.")

    def cmd_stats(self, _) -> None:
        stats = self.repo.get_stats()
        print(f"Всего задач: {stats['total']}")
        print(f"Просрочено:  {stats['overdue']}")
        print("По статусам:")
        for status, count in stats["by_status"].items():
            print(f"  {status:12s}: {count}")

    def cmd_save(self, _) -> None:
        self.repo.save()
        print("  [✓] Сохранено!")

    def cmd_exit(self, _) -> bool:
        self.repo.save()
        print("Сохранено. До свидания!")
        return True


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()
