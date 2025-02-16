"""user

Revision ID: 0f8863741a32
Revises: 6ed3f8c9ff47
Create Date: 2025-01-11 18:51:07.501092

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0f8863741a32"
down_revision = "6ed3f8c9ff47"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            login VARCHAR(255) NOT NULL UNIQUE,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE,
            is_active BOOLEAN NOT NULL DEFAULT FALSE,
            created_at timestamp with time zone default now() not null,
            updated_at timestamp with time zone default now() not null
        );
    """
    )
    op.execute(
        """
        create trigger users_updated_at_trg
            before update
            on users
            for each row
        execute procedure base.set_updated_at();
    """
    )


def downgrade():
    op.execute("drop trigger users_updated_at_trg on users;")
    op.execute("drop table users;")
