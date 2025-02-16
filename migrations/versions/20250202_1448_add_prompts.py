"""add prompts

Revision ID: 0b2b106265f7
Revises: c3b74732fb96
Create Date: 2025-02-02 14:48:41.990366

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0b2b106265f7"
down_revision = "c3b74732fb96"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
    ALTER TABLE presentations 
               ADD COLUMN prompt TEXT,
               ADD COLUMN version INT DEFAULT 1 NOT NULL;
    """
    )
    op.execute(
        """
    ALTER TABLE slides 
               DROP COLUMN title,
               ADD COLUMN position INT DEFAULT 1,
               ADD COLUMN prompt TEXT,
               ADD COLUMN version INT DEFAULT 1 NOT NULL;
    """
    )


def downgrade():
    op.execute(
        """
    ALTER TABLE presentations 
                DROP COLUMN prompt,
                DROP COLUMN version;
    """
    )
    op.execute(
        """
    ALTER TABLE slides
                ADD COLUMN title TEXT,
                DROP COLUMN position,
                DROP COLUMN prompt,
                DROP COLUMN version;
    """
    )
