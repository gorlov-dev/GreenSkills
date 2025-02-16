"""base

Revision ID: 6ed3f8c9ff47
Revises: 
Create Date: 2025-01-11 18:34:30.984466

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '6ed3f8c9ff47'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('create schema base;')
    op.execute('''
        create function base.set_updated_at() returns trigger
            language plpgsql
        as
        $$DECLARE
              _NEW record;
            BEGIN
                _NEW := NEW;
                _NEW.updated_at = now();
                RETURN _NEW;
            END;
        $$;    
            ''')


def downgrade():
    op.execute('drop function base.set_updated_at();')
    op.execute('drop schema base;')
