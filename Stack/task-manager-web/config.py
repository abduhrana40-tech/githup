import os
from datetime import timedelta

class Config:
    """إعدادات التطبيق"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'stack-task-manager-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = True
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # إعدادات واجهة المستخدم
    APP_NAME = "نظام إدارة المهام - Stack"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "تطبيق ويب لإدارة المهام باستخدام بنية Stack"
    
    # الألوان الرئيسية للتطبيق
    THEME_COLORS = {
        'primary': '#2C3E50',
        'secondary': '#3498DB',
        'success': '#27AE60',
        'danger': '#E74C3C',
        'warning': '#F39C12',
        'info': '#17A2B8',
        'light': '#ECF0F1',
        'dark': '#2C3E50'
    }
