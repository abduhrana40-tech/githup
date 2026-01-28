from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from config import Config
from datetime import datetime
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)

# تهيئة امتدادات (SQLAlchemy)
db.init_app(app)

# Jinja2 filters: تحويل ISO string إلى datetime ثم تنسيق التاريخ للعرض
def _fromisoformat(value):
    try:
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value
    except Exception:
        return value

def _datetimeformat(value, fmt="%d %b %Y %H:%M"):
    try:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value.strftime(fmt)
    except Exception:
        return value

# تسجيل الفلاتر في بيئة Jinja
app.jinja_env.filters['fromisoformat'] = _fromisoformat
app.jinja_env.filters['datetimeformat'] = _datetimeformat


# جعل `TaskStack` متاحاً داخل كل قوالب Jinja كمتغير عام
@app.context_processor
def inject_taskstack():
    # استيراد هنا لتجنب الحلقات عند تهيئة db
    from models.task_stack import TaskStack
    return {'TaskStack': TaskStack}


# إنشاء الجداول إن لم تكن موجودة
# استيراد نماذج DB لضمان تسجيل الجداول في MetaData قبل إنشاء الجداول
import models.task_stack  # noqa: F401
from models.task_stack import TaskStack

with app.app_context():
    db.create_all()

# مهام افتراضية لبدء التطبيق
DEFAULT_TASKS = [
    {
        "name": "دراسة هياكل البيانات",
        "description": "مراجعة مفاهيم Stack و Queue و Linked List"
    },
    {
        "name": "إنهاء المشروع النهائي",
        "description": "استكمال تطبيق نظام إدارة المهام"
    },
    {
        "name": "تحضير العرض التقديمي",
        "description": "تحضير عرض عن مشروع Stack"
    },
    {
        "name": "مراجعة الاختبار النهائي",
        "description": "مراجعة أسئلة الامتحان"
    }
]

@app.before_request
def initialize_session():
    """تهيئة الجلسة بالمهام الافتراضية عند أول دخول"""
    # وضع السمة الحالية في الجلسة إن لم تكن موجودة
    if 'theme' not in session:
        session['theme'] = 'light'

    # تأكد من وجود المكدس الافتراضي في DB، وإذا كان فارغاً أضف المهام الافتراضية مرة واحدة
    from models.task_stack import TaskStack
    default_stack = TaskStack('default')
    if default_stack.size() == 0:
        for task in DEFAULT_TASKS:
            default_stack.push(task['name'], task['description'])

    # ضبط المكدس الحالي في الجلسة إن لم يكن موجوداً
    if 'current_stack' not in session:
        session['current_stack'] = 'default'
    session['initialized'] = True

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    stack = TaskStack(session.get('current_stack', 'default'))
    stats = stack.get_stats()
    
    # الحصول على أحدث 3 مهام
    recent_tasks = stack.display_all()[:3]
    
    return render_template('index.html', 
                         stats=stats,
                         recent_tasks=recent_tasks,
                         current_stack=session.get('current_stack', 'default'))

@app.route('/tasks')
def view_tasks():
    """عرض جميع المهام"""
    stack_id = request.args.get('stack', session.get('current_stack', 'default'))
    session['current_stack'] = stack_id
    
    stack = TaskStack(stack_id)
    tasks = stack.display_all()
    stats = stack.get_stats()
    all_stacks = TaskStack.get_all_stacks()
    
    return render_template('tasks.html', 
                         tasks=tasks,
                         stats=stats,
                         current_stack=stack_id,
                         all_stacks=all_stacks)

@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    """إضافة مهمة جديدة"""
    if request.method == 'POST':
        task_name = request.form.get('task_name', '').strip()
        description = request.form.get('description', '').strip()
        stack_id = request.form.get('stack_id', session.get('current_stack', 'default'))
        
        if not task_name:
            flash('اسم المهمة مطلوب!', 'danger')
            return redirect(url_for('add_task'))
        
        stack = TaskStack(stack_id)
        new_task = stack.push(task_name, description)
        
        flash(f'تمت إضافة المهمة "{task_name}" بنجاح!', 'success')
        return redirect(url_for('view_tasks', stack=stack_id))
    
    # GET request
    all_stacks = TaskStack.get_all_stacks()
    return render_template('add_task.html', all_stacks=all_stacks)

@app.route('/update-task/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    """تحديث مهمة"""
    stack_id = session.get('current_stack', 'default')
    stack = TaskStack(stack_id)
    task = stack.search(task_id)
    
    if not task:
        flash('المهمة غير موجودة!', 'danger')
        return redirect(url_for('view_tasks'))
    
    if request.method == 'POST':
        new_name = request.form.get('task_name', '').strip()
        new_description = request.form.get('description', '').strip()
        
        if not new_name:
            flash('اسم المهمة مطلوب!', 'danger')
            return redirect(url_for('update_task', task_id=task_id))
        
        result = stack.update(task_id, new_name, new_description)
        
        if result:
            flash(f'تم تحديث المهمة بنجاح!', 'success')
        else:
            flash('حدث خطأ أثناء تحديث المهمة!', 'danger')
        
        return redirect(url_for('view_tasks'))
    
    # GET request
    return render_template('update_task.html', task=task)

@app.route('/delete-task', methods=['POST'])
def delete_task():
    """حذف المهمة من الأعلى (Pop)"""
    stack_id = request.form.get('stack_id', session.get('current_stack', 'default'))
    stack = TaskStack(stack_id)
    
    if stack.is_empty():
        flash('المكدس فارغ!', 'warning')
        return redirect(url_for('view_tasks', stack=stack_id))
    
    deleted_task = stack.pop()
    
    if deleted_task:
        flash(f'تم حذف المهمة "{deleted_task["task"]}" بنجاح!', 'success')
    else:
        flash('حدث خطأ أثناء حذف المهمة!', 'danger')
    
    return redirect(url_for('view_tasks', stack=stack_id))

@app.route('/delete-specific-task/<int:task_id>', methods=['POST'])
def delete_specific_task(task_id):
    """حذف مهمة محددة (لأغراض الإدارة)"""
    stack_id = session.get('current_stack', 'default')
    stack = TaskStack(stack_id)
    
    # للأسف، في Stack حقيقي لا يمكن حذف إلا من الأعلى
    # لكن لأغراض الإدارة سنقوم بمحاكاة هذه العملية
    tasks = stack.display_all()
    
    # البحث عن المهمة وحذفها (هذه ليست عملية Stack قياسية)
    found = False
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            # هذه عملية غير قياسية في Stack، للعرض فقط
            flash('ملاحظة: هذه العملية غير قياسية في Stack، يتم الحذف من الأعلى فقط', 'warning')
            
            # في الواقع، يجب إعادة بناء Stack
            all_tasks = stack.display_all()
            all_tasks = [t for t in all_tasks if t['id'] != task_id]
            
            # تفريغ وإعادة بناء
            stack.clear()
            for t in reversed(all_tasks):  # إعادة بناء بنفس الترتيب
                stack.push(t['task'], t.get('description', ''))
            
            found = True
            flash(f'تم إزالة المهمة بنجاح!', 'success')
            break
    
    if not found:
        flash('المهمة غير موجودة!', 'danger')
    
    return redirect(url_for('view_tasks'))

@app.route('/update-status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    """تحديث حالة المهمة"""
    stack_id = session.get('current_stack', 'default')
    stack = TaskStack(stack_id)
    
    new_status = request.form.get('status')
    if stack.update_status(task_id, new_status):
        flash(f'تم تحديث حالة المهمة إلى {new_status}!', 'success')
    else:
        flash('حدث خطأ في تحديث الحالة!', 'danger')
    
    return redirect(url_for('view_tasks'))

@app.route('/create-stack', methods=['POST'])
def create_stack():
    """إنشاء Stack جديد"""
    stack_name = request.form.get('stack_name', '').strip().lower()
    
    if not stack_name:
        flash('اسم المكدس مطلوب!', 'danger')
        return redirect(url_for('index'))
    
    from models.task_stack import Stack
    if Stack.query.filter_by(name=stack_name).first():
        flash('المكدس موجود بالفعل!', 'warning')
    else:
        TaskStack(stack_name)  # هذا سينشئ المكدس تلقائياً
        flash(f'تم إنشاء المكدس "{stack_name}" بنجاح!', 'success')
    
    return redirect(url_for('view_tasks', stack=stack_name))

@app.route('/clear-stack', methods=['POST'])
def clear_stack():
    """تفريغ Stack بالكامل"""
    stack_id = request.form.get('stack_id', session.get('current_stack', 'default'))
    stack = TaskStack(stack_id)
    
    if stack.is_empty():
        flash('المكدس فارغ بالفعل!', 'warning')
    else:
        stack.clear()
        flash('تم تفريغ المكدس بالكامل!', 'success')
    
    return redirect(url_for('view_tasks', stack=stack_id))

@app.route('/api/stats')
def api_stats():
    """API للحصول على إحصائيات"""
    stack_id = request.args.get('stack', session.get('current_stack', 'default'))
    stack = TaskStack(stack_id)
    
    return jsonify({
        'success': True,
        'stats': stack.get_stats(),
        'top_task': stack.peek(),
        'stack_size': stack.size()
    })

@app.route('/api/tasks')
def api_tasks():
    """API للحصول على المهام"""
    stack_id = request.args.get('stack', session.get('current_stack', 'default'))
    stack = TaskStack(stack_id)
    
    return jsonify({
        'success': True,
        'tasks': stack.display_all(),
        'total': stack.size()
    })

@app.route('/api/push', methods=['POST'])
def api_push():
    """API لإضافة مهمة"""
    data = request.json
    stack_id = data.get('stack', session.get('current_stack', 'default'))
    
    stack = TaskStack(stack_id)
    task = stack.push(data['task'], data.get('description', ''))
    
    return jsonify({
        'success': True,
        'message': 'تمت إضافة المهمة',
        'task': task
    })

@app.route('/api/pop', methods=['POST'])
def api_pop():
    """API لحذف مهمة من الأعلى"""
    data = request.json
    stack_id = data.get('stack', session.get('current_stack', 'default'))
    
    stack = TaskStack(stack_id)
    task = stack.pop()
    
    if task:
        return jsonify({
            'success': True,
            'message': 'تم حذف المهمة',
            'task': task
        })
    else:
        return jsonify({
            'success': False,
            'message': 'المكدس فارغ'
        }), 400

@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    """تبديل السمة بين فاتحة وداكنة"""
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    
    return jsonify({
        'success': True,
        'theme': new_theme
    })

@app.errorhandler(404)
def page_not_found(e):
    """معالجة صفحة غير موجودة"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """معالجة خطأ في الخادم"""
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
