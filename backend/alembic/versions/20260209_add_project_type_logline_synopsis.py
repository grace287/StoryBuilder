"""add project_type, logline, synopsis (소설/시나리오 아카이브)

Revision ID: 20260209_archive
Revises:
Create Date: 2026-02-09

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260209_archive"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    projecttype_enum = sa.Enum("novel", "scenario", name="projecttype")
    projecttype_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "projects",
        sa.Column("project_type", projecttype_enum, nullable=True, server_default="novel"),
    )
    op.add_column("projects", sa.Column("logline", sa.Text(), nullable=True))
    op.add_column("projects", sa.Column("synopsis", sa.Text(), nullable=True))
    op.alter_column(
        "projects",
        "project_type",
        existing_type=projecttype_enum,
        nullable=False,
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("projects", "synopsis")
    op.drop_column("projects", "logline")
    op.drop_column("projects", "project_type")
    sa.Enum(name="projecttype").drop(op.get_bind(), checkfirst=True)
