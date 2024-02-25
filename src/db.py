from typing import Dict, Any, List

import psycopg2
from .config import settings
import bcrypt


def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt(12))
    return hashed_bytes.decode("utf-8")


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


class SQL:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            f"""
            host={settings.POSTGRES_OUT_HOST}
            port={settings.POSTGRES_OUT_PORT}
            dbname={settings.POSTGRES_DB}
            user={settings.POSTGRES_USER}
            password={settings.POSTGRES_PASSWORD}
        """
        )
        self.cursor = self.conn.cursor()

    def reg_user(self, username: str, password: str) -> bool | int:
        password = hash_password(password)
        with self.conn:
            self.cursor.execute(
                "SELECT username FROM users WHERE username=%s", (username,)
            )
            result = self.cursor.fetchall()
            if not bool(len(result)):
                self.cursor.execute(
                    "INSERT INTO users (username, password, role_id) VALUES (%s, %s, %s) "
                    "RETURNING id",
                    (username, password, 1),
                )
                user_id = int(self.cursor.fetchall()[0][0])
                return user_id
        return False

    def login(self, username: str, password: str) -> bool | int:
        with self.conn:
            self.cursor.execute(
                "SELECT password, id FROM users WHERE username=%s", (username,)
            )
            result = self.cursor.fetchall()
            if bool(len(result)) and check_password(password, result[0][0]):
                return result[0][1]
        return False

    def create_task_list(self, task_list_name: str, user_id: int) -> (bool, str):
        with self.conn:
            self.cursor.execute(
                "SELECT id FROM task_lists WHERE name=%s and owner_id=%s",
                (
                    task_list_name,
                    user_id,
                ),
            )
            result = self.cursor.fetchall()
            if not bool(len(result)):
                self.cursor.execute(
                    "INSERT INTO task_lists (name, owner_id) VALUES (%s, %s)",
                    (
                        task_list_name,
                        user_id,
                    ),
                )
                return True, "Task list created successfully"
        return False, "Task list with this name already exists"

    def get_task_lists(self, user_id: int) -> (bool, Dict[Any, Any]):
        with self.conn:
            task_lists = dict()
            self.cursor.execute(
                "SELECT name FROM task_lists WHERE owner_id=%s", (user_id,)
            )
            result = self.cursor.fetchall()
            for index, element in enumerate(result):
                task_lists[index] = element[0]
            return True, task_lists

    def update_task_list(
        self, task_list_old_name: str, task_list_new_name: str, user_id: int
    ) -> (bool, str):
        with self.conn:
            self.cursor.execute(
                "SELECT id FROM task_lists WHERE name=%s and owner_id=%s",
                (
                    task_list_old_name,
                    user_id,
                ),
            )
            result = self.cursor.fetchall()
            if bool(len(result)):
                self.cursor.execute(
                    "UPDATE task_lists SET name=%s WHERE name=%s",
                    (task_list_new_name, task_list_old_name),
                )
                return True, task_list_new_name
        return False, "Task list with this name doesn't exists"

    def delete_task_list(self, task_list_name: str, user_id: int) -> (bool, str):
        with self.conn:
            self.cursor.execute(
                "SELECT id FROM task_lists WHERE name=%s and owner_id=%s",
                (
                    task_list_name,
                    user_id,
                ),
            )
            result = self.cursor.fetchall()
            if bool(len(result)):
                self.cursor.execute(
                    "DELETE FROM task_lists WHERE name=%s and owner_id=%s",
                    (task_list_name, user_id),
                )
                return True, "Successfully deleted task_list"
        return False, "Task list with this name doesn't exists"

    def check_task_list(self, task_list_name: str, user_id: int) -> int:
        with self.conn:
            self.cursor.execute(
                "SELECT id FROM task_lists WHERE name=%s and owner_id=%s",
                (
                    task_list_name,
                    user_id,
                ),
            )
            res = self.cursor.fetchall()
            if not bool(len(res)):
                return -1
            task_list_id = res[0][0]
            return task_list_id

    def create_task(
        self, task_list_name: str, task_name: str, description: str, user_id: int
    ) -> (bool, str):
        task_list_id = self.check_task_list(task_list_name, user_id)
        if task_list_id == -1:
            return False, "No such task list"
        with self.conn:
            self.cursor.execute(
                "SELECT id FROM tasks WHERE name=%s and list_id=%s",
                (
                    task_name,
                    task_list_id,
                ),
            )
            result = self.cursor.fetchall()
            if not bool(len(result)):
                self.cursor.execute(
                    "INSERT INTO tasks (name, description, list_id) VALUES (%s, %s, %s)",
                    (
                        task_name,
                        description,
                        task_list_id,
                    ),
                )
                return True, "Task created successfully"
        return False, "Task with this name already exists"

    def get_tasks(self, task_list_name: str, user_id: int) -> (bool, List[Any]):
        task_list_id = self.check_task_list(task_list_name, user_id)
        if task_list_id == -1:
            return False, ["No such task list"]
        with self.conn:
            tasks = []
            self.cursor.execute(
                "SELECT name, description FROM tasks WHERE list_id=%s", (task_list_id,)
            )
            result = self.cursor.fetchall()
            for element in enumerate(result):
                curr_task = dict()
                curr_task["name"] = element[1][0]
                curr_task["description"] = element[1][1]
                tasks.append(curr_task)
            return True, tasks

    def update_task(
        self,
        task_old_name: str,
        task_new_name: str,
        new_desc: str,
        task_list_name: str,
        user_id: int,
    ) -> (bool, str):
        task_list_id = self.check_task_list(task_list_name, user_id)
        if task_list_id == -1:
            return False, "No such task list"
        with self.conn:
            self.cursor.execute(
                "SELECT id FROM tasks WHERE list_id=%s and name=%s",
                (
                    task_list_id,
                    task_old_name,
                ),
            )
            result = self.cursor.fetchall()
            if bool(len(result)):
                self.cursor.execute(
                    "UPDATE tasks SET name=%s, description=%s WHERE list_id=%s and name=%s",
                    (
                        task_new_name,
                        new_desc,
                        task_list_id,
                        task_old_name,
                    ),
                )
                return True, task_new_name
        return False, "Task with this name doesn't exists"

    def delete_task(
        self, task_name: str, task_list_name: str, user_id: int
    ) -> (bool, str):
        task_list_id = self.check_task_list(task_list_name, user_id)
        if task_list_id == -1:
            return False, "No such task list"
        with self.conn:
            self.cursor.execute(
                "SELECT id FROM tasks WHERE list_id=%s and name=%s",
                (
                    task_list_id,
                    task_name,
                ),
            )
            result = self.cursor.fetchall()
            if bool(len(result)):
                self.cursor.execute(
                    "DELETE FROM tasks WHERE list_id=%s and name=%s",
                    (
                        task_list_id,
                        task_name,
                    ),
                )
                return True, "Successfully deleted task"
            return False, "No such task"

    def is_admin(self, user_id: int) -> bool:
        with self.conn:
            self.cursor.execute(
                "SELECT roles.role FROM users JOIN roles ON users.role_id=roles.id "
                "WHERE users.id = %s",
                (user_id,),
            )
            result = self.cursor.fetchall()[0][0]
            return result == "admin"

    def admin_get_task_lists(self):
        with self.conn:
            task_lists = dict()
            self.cursor.execute(
                "SELECT task_lists.name FROM task_lists JOIN users "
                "ON task_lists.owner_id=users.id"
            )
            result = self.cursor.fetchall()
            for index, element in enumerate(result):
                task_lists[index] = element[0]
            return True, task_lists

    def admin_get_tasks(self, task_list_name: str) -> (bool, List[Any]):
        with self.conn:
            self.cursor.execute(
                "SELECT id FROM task_lists WHERE name=%s", (task_list_name,)
            )
            res = self.cursor.fetchall()
            if not bool(len(res)):
                return False, ["No such task"]
            task_list_id = res[0][0]
            tasks = []
            self.cursor.execute(
                "SELECT name, description FROM tasks WHERE list_id=%s", (task_list_id,)
            )
            result = self.cursor.fetchall()
            for element in enumerate(result):
                curr_task = dict()
                curr_task["name"] = element[1][0]
                curr_task["description"] = element[1][1]
                tasks.append(curr_task)
            return True, tasks

    def store_csrf_token(self, user_id: int, csrf_token: str) -> None:
        with self.conn:
            self.cursor.execute("SELECT user_id FROM csrf WHERE user_id=%s", (user_id,))
            res = self.cursor.fetchall()
            if bool(len(res)):
                self.cursor.execute(
                    "UPDATE csrf SET csrf_token=%s WHERE user_id=%s",
                    (csrf_token, user_id),
                )
            else:
                self.cursor.execute(
                    "INSERT INTO csrf (user_id, csrf_token) VALUES (%s, %s)",
                    (user_id, csrf_token),
                )

    def get_csrf_by_id(self, user_id: int):
        with self.conn:
            self.cursor.execute(
                "SELECT csrf_token FROM csrf WHERE user_id=%s", (user_id,)
            )
            res = self.cursor.fetchone()
            return res[0]


db = SQL()
