import sqlite3
from .creational_patterns import Student, Category, Course


class StudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, name):
        statement = f"SELECT id, name FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        id, name = result
        if result:
            return Student(name)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, category = item
            category = Category(name, category)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name, category FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        found = self.cursor.fetchone()
        if found:
            id, name, category = found
            result = Category(name, category)
            result.id = id
            return result
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CourseMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'course'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, type_, name, category_id = item
            course = Course(type_, name, category_id)
            course.id = id
            result.append(course)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Course(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, name):
        statement = f"SELECT id, type_, name, category_id FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        id, type_, name, category_id = result
        if result:
            return Course(type_, name, category_id)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_category_id(self, id):
        statement = f"SELECT * FROM {self.tablename} WHERE category_id=?"
        self.cursor.execute(statement, (id,))
        result = []
        for item in self.cursor.fetchall():
            id, type_, name, category = item
            course = Course(type_, name, category)
            course.id = id
            result.append(course)
        return result

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (type_, name, category_id) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.type_, obj.name, obj.category_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        if isinstance(obj, Course):
            return CourseMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
