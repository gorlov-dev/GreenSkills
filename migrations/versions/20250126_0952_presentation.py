"""presentation

Revision ID: d7878db9e4cf
Revises: 0f8863741a32
Create Date: 2025-01-26 09:52:31.405515

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d7878db9e4cf"
down_revision = "0f8863741a32"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE presentations (
            id SERIAL PRIMARY KEY,
            owner_id INT NOT NULL REFERENCES users(id),
            title TEXT,
            publication_code VARCHAR(20) UNIQUE,
            created_at timestamp with time zone default now() not null,
            updated_at timestamp with time zone default now() not null
        );
    """
    )
    op.execute(
        """
        create trigger presentations_updated_at_trg
            before update
            on presentations
            for each row
        execute procedure base.set_updated_at();
    """
    )


def downgrade():
    op.execute("drop trigger presentations_updated_at_trg on presentations;")
    op.execute("drop table presentations;")
