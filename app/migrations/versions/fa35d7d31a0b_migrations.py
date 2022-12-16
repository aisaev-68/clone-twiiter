"""migrations

Revision ID: fa35d7d31a0b
Revises: 
Create Date: 2022-12-16 12:14:24.762842

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fa35d7d31a0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_images')
    op.drop_table('images')
    op.drop_table('likes')
    op.drop_table('followings')
    op.drop_table('tweets')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('api_token', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('tweets',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tweets_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('tweet', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('stamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='tweets_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='tweets_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('followings',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_to_follow_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='followings_user_id_fkey'),
    sa.ForeignKeyConstraint(['user_to_follow_id'], ['users.id'], name='followings_user_to_follow_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'user_to_follow_id', name='followings_pkey')
    )
    op.create_table('likes',
    sa.Column('tweet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], name='likes_tweet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='likes_user_id_fkey'),
    sa.PrimaryKeyConstraint('tweet_id', 'user_id', name='likes_pkey')
    )
    op.create_table('images',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('images_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='images_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('post_images',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('tweet_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='post_images_image_id_fkey'),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], name='post_images_tweet_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='post_images_pkey')
    )
    # ### end Alembic commands ###
