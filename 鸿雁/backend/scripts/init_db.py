#!/usr/bin/env python3
"""初始化数据库：创建表、创建默认管理员"""
import os
import sys
import bcrypt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from app.database import SessionLocal, engine, Base
from app.models import User  # noqa: F401


def main():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print('所有表创建完成')

    db = SessionLocal()

    # 创建管理员
    admin = db.query(User).filter(User.student_id == 'admin').first()
    if not admin:
        hashed = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')
        admin = User(
            student_id='admin',
            full_name='系统管理员',
            password_hash=hashed,
            role='admin',
            email='admin@hongyan.edu.cn',
        )
        db.add(admin)
        db.commit()
        print('创建管理员: admin / admin123')
    else:
        print('管理员已存在')

    db.close()
    print('数据库初始化完成')


if __name__ == '__main__':
    main()
