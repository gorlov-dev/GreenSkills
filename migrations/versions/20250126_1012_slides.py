"""slides

Revision ID: c3b74732fb96
Revises: 967ec7dff643
Create Date: 2025-01-26 10:12:03.320367

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c3b74732fb96"
down_revision = "967ec7dff643"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE slides (
            id SERIAL PRIMARY KEY,
            template_id INT NOT NULL REFERENCES slide_templates(id),
            presentation_id INT NOT NULL REFERENCES presentations(id),
            title TEXT,
            data JSONB NOT NULL,
            created_at timestamp with time zone default now() not null,
            updated_at timestamp with time zone default now() not null
        );
    """
    )
    op.execute(
        """
        create trigger slides_updated_at_trg
            before update
            on slides
            for each row
        execute procedure base.set_updated_at();
    """
    )


def downgrade():
    op.execute("drop trigger slides_updated_at_trg on slides;")
    op.execute("drop table slides;")
