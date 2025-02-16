"""slide_templates

Revision ID: 967ec7dff643
Revises: d7878db9e4cf
Create Date: 2025-01-26 10:09:43.503704

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "967ec7dff643"
down_revision = "d7878db9e4cf"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE slide_templates (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            slug VARCHAR(20) UNIQUE NOT NULL,
            data_structure TEXT,
            data JSONB NOT NULL,
            created_at timestamp with time zone default now() not null,
            updated_at timestamp with time zone default now() not null
        );
    """
    )
    op.execute(
        """
        create trigger templates_updated_at_trg
            before update
            on slide_templates
            for each row
        execute procedure base.set_updated_at();
    """
    )


def downgrade():
    op.execute("drop trigger templates_updated_at_trg on slide_templates;")
    op.execute("drop table slide_templates;")
