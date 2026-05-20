"""create_job_templates

Revision ID: e9b2c3d4f5a6
Revises: d8a1b2c3e4f5
Create Date: 2026-05-20 10:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'e9b2c3d4f5a6'
down_revision: Union[str, None] = 'd8a1b2c3e4f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('job_templates',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('required_skills', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('preferred_skills', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('responsibilities', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('question_categories', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('difficulty_level', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_templates_id'), 'job_templates', ['id'], unique=False)
    op.create_index(op.f('ix_job_templates_title'), 'job_templates', ['title'], unique=False)
    op.create_index(op.f('ix_job_templates_is_active'), 'job_templates', ['is_active'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_job_templates_is_active'), table_name='job_templates')
    op.drop_index(op.f('ix_job_templates_title'), table_name='job_templates')
    op.drop_index(op.f('ix_job_templates_id'), table_name='job_templates')
    op.drop_table('job_templates')
