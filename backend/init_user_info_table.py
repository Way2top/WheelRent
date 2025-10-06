from app_simple import app, db, UserInfo

with app.app_context():
    # 创建所有表（如果不存在）
    db.create_all()
    print('UserInfo table created successfully!')

    # 检查是否已存在表
    if db.engine.dialect.has_table(db.engine, 'user_info'):
        print('UserInfo table already exists in the database.')
    else:
        print('Error: UserInfo table was not created properly.')

    # 显示表结构信息
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    if 'user_info' in inspector.get_table_names():
        print('\nUserInfo table columns:')
        for column in inspector.get_columns('user_info'):
            print(f"- {column['name']} ({column['type']}){'' if not column['nullable'] else ' (nullable)'}")