"""init_db

Revision ID: 3423b3aaf7f4
Revises: 
Create Date: 2022-12-27 09:26:26.627302

"""
from alembic import op
import sqlalchemy as sa
from sqlmodel import SQLModel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3423b3aaf7f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
                    sa.Column('api_token', sa.TEXT(), autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='user_pkey'),
                    sa.UniqueConstraint('username', name='user_username_key')
                    )
    op.create_table('followings',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('follows_user_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['follows_user_id'], ['user.id'], name='followings_follows_user_id_fkey'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='followings_user_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='followings_pkey')
                    )
    op.create_table('tweet',
                    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tweet_id_seq'::regclass)"),
                              autoincrement=True, nullable=False),
                    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              autoincrement=False, nullable=True),
                    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='tweet_user_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='tweet_pkey'),
                    postgresql_ignore_search_path=False
                    )
    op.create_table('tweet_likes',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('tweet_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], name='tweet_likes_tweet_id_fkey'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='tweet_likes_user_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='tweet_likes_pkey')
                    )

    op.create_table('media',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('tweet_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('path_file', sa.TEXT(), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], name='media_tweet_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='media_pkey')
                    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('media')
    op.drop_table('tweet')
    op.drop_table('tweet_likes')
    op.drop_table('followings')

    # ### end Alembic commands ###
