"""Create explicit demo users and synthetic data. Never runs at application startup."""
import os
import secrets

from .auth import hash_password
from .db import Store


ACCOUNTS = [('admin@alpha.test','alpha','admin'), ('analyst@alpha.test','alpha','analyst'),
            ('viewer@alpha.test','alpha','viewer'), ('reviewer@alpha.test','alpha','admin'),
            ('admin@beta.test','beta','admin')]


def seed_users(store, password):
    if len(password) < 16:
        raise ValueError('Demo password must be at least 16 characters')
    for email, tenant, role in ACCOUNTS:
        if not store.one('SELECT id FROM users WHERE email=?', (email,)):
            store.execute('INSERT INTO users VALUES (?,?,?,?,?)',
                          (email.split('@')[0] + '-' + tenant, email, hash_password(password), tenant, role))


def seed_data(store):
    return None


def main():
    store = Store(os.getenv('DATABASE_PATH', 'data/application.db'))
    if store.one('SELECT id FROM users LIMIT 1'):
        print('Users already exist. Seeding does not reset existing passwords.')
        seed_data(store)
        return
    password = os.getenv('DEMO_PASSWORD') or secrets.token_urlsafe(20)
    seed_users(store, password)
    seed_data(store)
    print('Demo accounts: ' + ', '.join(a[0] for a in ACCOUNTS))
    print('Demo password (local only): ' + password)


if __name__ == '__main__':
    main()
