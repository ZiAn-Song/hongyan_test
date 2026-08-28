"""add sdu_talents table

Revision ID: c2d3e4f5a6b7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-27 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c2d3e4f5a6b7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'resource_embeddings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source_type', sa.String(length=30), nullable=False),
        sa.Column('source_id', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=True),
        sa.Column('embedding', sa.Text(), nullable=False),
        sa.Column('content_digest', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_resource_embeddings_source_type'), 'resource_embeddings', ['source_type'])
    op.create_index(op.f('ix_resource_embeddings_source_id'), 'resource_embeddings', ['source_id'])

    op.create_table(
        'completed_achievements',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('achievement_id', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('region', sa.String(length=300), nullable=True),
        sa.Column('parties', sa.String(length=500), nullable=True),
        sa.Column('finish_time', sa.String(length=100), nullable=True),
        sa.Column('work_done', sa.Text(), nullable=True),
        sa.Column('highlights', sa.Text(), nullable=True),
        sa.Column('achievement_type', sa.String(length=100), nullable=True),
        sa.Column('replicable_points', sa.String(length=500), nullable=True),
        sa.Column('image_note', sa.Text(), nullable=True),
        sa.Column('image_link', sa.String(length=1000), nullable=True),
        sa.Column('evidence', sa.Text(), nullable=True),
        sa.Column('source_level', sa.String(length=100), nullable=True),
        sa.Column('source_body', sa.String(length=500), nullable=True),
        sa.Column('publish_date', sa.String(length=50), nullable=True),
        sa.Column('source_url', sa.String(length=1000), nullable=True),
        sa.Column('verification_status', sa.String(length=50), nullable=True),
        sa.Column('boundary_note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('achievement_id'),
    )
    op.create_index(op.f('ix_completed_achievements_title'), 'completed_achievements', ['title'])
    op.create_table(
        'sdu_talents',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('domain', sa.String(length=50), nullable=False),
        sa.Column('org', sa.String(length=200), nullable=True),
        sa.Column('field', sa.String(length=500), nullable=True),
        sa.Column('team', sa.String(length=300), nullable=False),
        sa.Column('leader', sa.String(length=200), nullable=True),
        sa.Column('leader_title', sa.Text(), nullable=True),
        sa.Column('patents', sa.Text(), nullable=True),
        sa.Column('core_tech', sa.Text(), nullable=True),
        sa.Column('awards', sa.Text(), nullable=True),
        sa.Column('west_scene', sa.String(length=500), nullable=True),
        sa.Column('application', sa.String(length=500), nullable=True),
        sa.Column('maturity', sa.String(length=100), nullable=True),
        sa.Column('cases', sa.Text(), nullable=True),
        sa.Column('source_url', sa.String(length=1000), nullable=True),
        sa.Column('source_note', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_sdu_talents_domain'), 'sdu_talents', ['domain'])
    op.create_index(op.f('ix_sdu_talents_team'), 'sdu_talents', ['team'])


def downgrade() -> None:
    op.drop_index(op.f('ix_sdu_talents_team'), table_name='sdu_talents')
    op.drop_index(op.f('ix_sdu_talents_domain'), table_name='sdu_talents')
    op.drop_index(op.f('ix_completed_achievements_title'), table_name='completed_achievements')
    op.drop_index(op.f('ix_resource_embeddings_source_id'), table_name='resource_embeddings')
    op.drop_index(op.f('ix_resource_embeddings_source_type'), table_name='resource_embeddings')
    op.drop_table('resource_embeddings')
op.drop_table('completed_achievements')
op.drop_table('sdu_talents')
