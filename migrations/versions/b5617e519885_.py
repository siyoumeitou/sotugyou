"""empty message

Revision ID: b5617e519885
Revises: 
Create Date: 2025-01-23 11:54:40.591996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5617e519885'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('chat_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('chat_id', 'user_id')
    )
    op.create_table('schedules',
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('memo', sa.String(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('schedule_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('if_ProjectLeader', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)

    op.create_table('chat_contents',
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('sender_name', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('sended_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id', 'user_id'], ['chats.chat_id', 'chats.user_id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('content_id')
    )
    op.create_table('chat_members',
    sa.Column('chat_member_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('member_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id', 'user_id'], ['chats.chat_id', 'chats.user_id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('chat_member_id')
    )
    op.create_table('folders',
    sa.Column('folder_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('creater_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creater_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('folder_id')
    )
    op.create_table('friends',
    sa.Column('friend_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('friend_user_id', sa.Integer(), nullable=True),
    sa.Column('friend_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('friend_id')
    )
    op.create_table('projects',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('creater_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creater_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('project_id')
    )
    op.create_table('memos',
    sa.Column('memo_id', sa.Integer(), nullable=False),
    sa.Column('folder_id', sa.Integer(), nullable=True),
    sa.Column('creater_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('memo', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creater_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['folder_id'], ['folders.folder_id'], ),
    sa.PrimaryKeyConstraint('memo_id')
    )
    op.create_table('project_members',
    sa.Column('project_member_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('member_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], ),
    sa.PrimaryKeyConstraint('project_member_id')
    )
    op.create_table('tasks',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('creater_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creater_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], ),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.create_table('checks',
    sa.Column('check_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('register_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('checked', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['register_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.task_id'], ),
    sa.PrimaryKeyConstraint('check_id')
    )
    op.create_table('tasks_progresses',
    sa.Column('progress_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('register_id', sa.Integer(), nullable=True),
    sa.Column('register_name', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('progress', sa.String(), nullable=True),
    sa.Column('percent', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['register_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.task_id'], ),
    sa.PrimaryKeyConstraint('progress_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks_progresses')
    op.drop_table('checks')
    op.drop_table('tasks')
    op.drop_table('project_members')
    op.drop_table('memos')
    op.drop_table('projects')
    op.drop_table('friends')
    op.drop_table('folders')
    op.drop_table('chat_members')
    op.drop_table('chat_contents')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    op.drop_table('schedules')
    op.drop_table('chats')
    # ### end Alembic commands ###
