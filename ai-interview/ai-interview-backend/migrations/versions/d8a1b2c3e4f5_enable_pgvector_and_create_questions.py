"""enable_pgvector_and_create_questions

Revision ID: d8a1b2c3e4f5
Revises: c7f982abaaf0
Create Date: 2026-05-20 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision: str = 'd8a1b2c3e4f5'
down_revision: Union[str, None] = 'c7f982abaaf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table('questions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=True),
        sa.Column('tags', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('reference_answer', sa.Text(), nullable=True),
        sa.Column('key_points', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('embedding', Vector(1024), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    op.create_index(op.f('ix_questions_category'), 'questions', ['category'], unique=False)
    op.create_index(op.f('ix_questions_difficulty'), 'questions', ['difficulty'], unique=False)
    op.create_index(op.f('ix_questions_is_active'), 'questions', ['is_active'], unique=False)

    op.execute(
        "CREATE INDEX ix_questions_embedding_hnsw ON questions "
        "USING hnsw (embedding vector_cosine_ops) "
        "WITH (m = 16, ef_construction = 200)"
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_questions_embedding_hnsw'), table_name='questions')
    op.drop_index(op.f('ix_questions_is_active'), table_name='questions')
    op.drop_index(op.f('ix_questions_difficulty'), table_name='questions')
    op.drop_index(op.f('ix_questions_category'), table_name='questions')
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_table('questions')
