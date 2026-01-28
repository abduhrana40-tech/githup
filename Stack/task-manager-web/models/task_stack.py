from datetime import datetime
from extensions import db


class Stack(db.Model):
    __tablename__ = 'stacks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_operations = db.Column(db.Integer, default=0)

    tasks = db.relationship('Task', backref='stack', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Stack {self.name}>"


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    stack_id = db.Column(db.Integer, db.ForeignKey('stacks.id'), nullable=False)
    task = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default='')
    status = db.Column(db.String(30), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TaskStack:
    """DB-backed TaskStack wrapper providing previous interface."""

    def __init__(self, stack_id='default'):
        self.stack_name = stack_id
        stack = Stack.query.filter_by(name=stack_id).first()
        if not stack:
            stack = Stack(name=stack_id)
            db.session.add(stack)
            db.session.commit()
        self._stack = stack

    def push(self, task_name, description=""):
        t = Task(stack_id=self._stack.id, task=task_name, description=description)
        db.session.add(t)
        self._stack.total_operations = (self._stack.total_operations or 0) + 1
        db.session.commit()
        return t.to_dict()

    def pop(self):
        task = Task.query.filter_by(stack_id=self._stack.id).order_by(Task.created_at.desc()).first()
        if not task:
            return None
        result = task.to_dict()
        db.session.delete(task)
        self._stack.total_operations = (self._stack.total_operations or 0) + 1
        db.session.commit()
        return result

    def peek(self):
        task = Task.query.filter_by(stack_id=self._stack.id).order_by(Task.created_at.desc()).first()
        return task.to_dict() if task else None

    def display_all(self):
        tasks = Task.query.filter_by(stack_id=self._stack.id).order_by(Task.created_at.desc()).all()
        return [t.to_dict() for t in tasks]

    def update(self, task_id, new_task_name, new_description=None):
        task = Task.query.filter_by(id=task_id, stack_id=self._stack.id).first()
        if not task:
            return None
        old = task.task
        task.task = new_task_name
        if new_description is not None:
            task.description = new_description
        task.updated_at = datetime.utcnow()
        self._stack.total_operations = (self._stack.total_operations or 0) + 1
        db.session.commit()
        return {'old': old, 'new': new_task_name}

    def search(self, task_id):
        t = Task.query.filter_by(id=task_id, stack_id=self._stack.id).first()
        return t.to_dict() if t else None

    def update_status(self, task_id, status):
        valid_statuses = ["pending", "in_progress", "completed"]
        if status not in valid_statuses:
            return False
        t = Task.query.filter_by(id=task_id, stack_id=self._stack.id).first()
        if not t:
            return False
        t.status = status
        t.updated_at = datetime.utcnow()
        db.session.commit()
        return True

    def is_empty(self):
        return Task.query.filter_by(stack_id=self._stack.id).count() == 0

    def size(self):
        return Task.query.filter_by(stack_id=self._stack.id).count()

    def clear(self):
        Task.query.filter_by(stack_id=self._stack.id).delete()
        db.session.commit()

    def get_stats(self):
        total = self.size()
        pending = Task.query.filter_by(stack_id=self._stack.id, status='pending').count()
        inprog = Task.query.filter_by(stack_id=self._stack.id, status='in_progress').count()
        completed = Task.query.filter_by(stack_id=self._stack.id, status='completed').count()
        return {
            'total_tasks': total,
            'pending_tasks': pending,
            'in_progress_tasks': inprog,
            'completed_tasks': completed,
            'total_operations': self._stack.total_operations or 0,
            'created_at': self._stack.created_at.isoformat() if self._stack.created_at else None
        }

    @staticmethod
    def get_all_stacks():
        stacks = Stack.query.order_by(Stack.created_at.asc()).all()
        return [{'id': s.name, 'name': s.name.capitalize(), 'task_count': len(s.tasks), 'created_at': s.created_at.isoformat()} for s in stacks]

