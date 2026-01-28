// script.js

document.addEventListener('DOMContentLoaded', function() {
    // تهيئة أدوات التلميح
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // تحديث الوقت الحالي
    function updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ar-SA');
        const dateString = now.toLocaleDateString('ar-SA', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        const timeElement = document.getElementById('currentTime');
        if (timeElement) {
            timeElement.innerHTML = `<i class="bi bi-clock"></i> ${dateString} - ${timeString}`;
        }
    }

    // تحديث الوقت كل ثانية
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);

    // تأثيرات للمهام عند التحميل
    const stackItems = document.querySelectorAll('.stack-item-visual');
    stackItems.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('stack-push');
        }, index * 100);
    });

    // معالجة حذف المهام
    const deleteButtons = document.querySelectorAll('.delete-specific-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.dataset.taskId;
            const taskName = this.dataset.taskName;
            
            if (confirm(`هل أنت متأكد من حذف المهمة "${taskName}"؟\n\nملاحظة: هذه العملية ليست قياسية في Stack.`)) {
                // إظهار تأثير الحذف
                const row = this.closest('tr');
                if (row) {
                    row.classList.add('stack-pop');
                    setTimeout(() => {
                        // هنا سيتم إرسال النموذج بالفعل
                    }, 500);
                }
            }
        });
    });

    // تحسين تجربة النماذج
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading-spinner"></span> جاري المعالجة...';
            }
        });
    });

    // تأثيرات عند تمرير الماوس على البطاقات
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 20px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        });
    });

    // تحديث ديناميكي للإحصائيات
    function updateStackStats() {
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // تحديث العناصر المختلفة
                    const statsElements = {
                        'totalTasks': data.stats.total_tasks,
                        'pendingTasks': data.stats.pending_tasks,
                        'inProgressTasks': data.stats.in_progress_tasks,
                        'completedTasks': data.stats.completed_tasks
                    };

                    for (const [key, value] of Object.entries(statsElements)) {
                        const element = document.getElementById(key);
                        if (element) {
                            // تأثير الترقيم
                            const current = parseInt(element.textContent);
                            if (current !== value) {
                                animateCount(element, current, value);
                            }
                        }
                    }

                    // تحديث المهمة العلوية
                    if (data.top_task) {
                        const topTaskElement = document.getElementById('topTask');
                        if (topTaskElement) {
                            topTaskElement.textContent = data.top_task.task;
                        }
                    }
                }
            })
            .catch(error => console.error('Error updating stats:', error));
    }

    // دالة للعد المتحرك
    function animateCount(element, start, end) {
        const duration = 500; // مدة الحركة بالمللي ثانية
        const range = end - start;
        const stepTime = Math.abs(Math.floor(duration / range));
        let current = start;
        
        const timer = setInterval(() => {
            current += (range > 0 ? 1 : -1);
            element.textContent = current;
            
            if (current === end) {
                clearInterval(timer);
            }
        }, stepTime);
    }

    // تحديث الإحصائيات كل 30 ثانية
    if (document.querySelector('[id*="Tasks"]')) {
        setInterval(updateStackStats, 30000);
    }

    // تنبيهات WebSocket (محاكاة)
    function checkForNewOperations() {
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.stats.total_operations > window.lastOperationCount) {
                    window.lastOperationCount = data.stats.total_operations;
                    
                    // إظهار إشعار
                    showNotification('عملية جديدة', 'تم إجراء عملية جديدة على المكدس');
                }
            });
    }

    // دالة لعرض الإشعارات
    function showNotification(title, message) {
        // التحقق من دعم الإشعارات
        if (!("Notification" in window)) {
            return;
        }

        // طلب الإذن
        if (Notification.permission === "granted") {
            new Notification(title, { body: message, icon: '/static/images/icon.png' });
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    new Notification(title, { body: message, icon: '/static/images/icon.png' });
                }
            });
        }
    }

    // تهيئة متغيرات
    if (typeof window.lastOperationCount === 'undefined') {
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.lastOperationCount = data.stats.total_operations;
                }
            });
    }

    // التحقق من العمليات كل دقيقة
    setInterval(checkForNewOperations, 60000);

    // إضافة تأثيرات للرموز
    const icons = document.querySelectorAll('.bi');
    icons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // تحسين إمكانية الوصول
    document.addEventListener('keydown', function(e) {
        // اختصارات لوحة المفاتيح
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case '1':
                    e.preventDefault();
                    window.location.href = '/';
                    break;
                case '2':
                    e.preventDefault();
                    window.location.href = '/tasks';
                    break;
                case '3':
                    e.preventDefault();
                    window.location.href = '/add-task';
                    break;
                case 'p':
                    e.preventDefault();
                    document.querySelector('[data-bs-target="#popModal"]')?.click();
                    break;
            }
        }
    });

    // إظهار رسالة اختصارات لوحة المفاتيح
    console.log(`
    === اختصارات لوحة المفاتيح ===
    Ctrl+1: الرئيسية
    Ctrl+2: عرض المهام
    Ctrl+3: إضافة مهمة
    Ctrl+P: حذف من الأعلى (Pop)
    `);
});

// دالة لنسخ النص
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // إظهار رسالة نجاح
        const toast = document.createElement('div');
        toast.className = 'position-fixed bottom-0 end-0 p-3';
        toast.innerHTML = `
            <div class="toast show" role="alert">
                <div class="toast-header bg-success text-white">
                    <strong class="me-auto">تم النسخ</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    تم نسخ النص إلى الحافظة
                </div>
            </div>
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    });
}

// دالة لمشاركة المهمة
function shareTask(taskId, taskName) {
    if (navigator.share) {
        navigator.share({
            title: `المهمة: ${taskName}`,
            text: `انظر إلى هذه المهمة في نظام إدارة المهام`,
            url: `${window.location.origin}/tasks#task-${taskId}`
        });
    } else {
        copyToClipboard(`${window.location.origin}/tasks#task-${taskId}`);
    }
}

// تأثيرات التحميل
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.innerHTML = '<span class="loading-spinner"></span> جاري التحميل...';
    element.disabled = true;
    
    return function() {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// تصفية المهام
function filterTasks(status) {
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const statusBadge = row.querySelector('.badge');
        if (status === 'all' || (statusBadge && statusBadge.textContent.includes(status))) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
