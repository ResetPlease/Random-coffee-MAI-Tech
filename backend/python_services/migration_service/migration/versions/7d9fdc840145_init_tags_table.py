"""init_tags_table

Revision ID: 7d9fdc840145
Revises: 38ca41614ca6
Create Date: 2025-04-06 17:13:39.069069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7d9fdc840145'
down_revision: Union[str, None] = '38ca41614ca6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
from migration.TableInit import TableInit


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    tags = sa.Table('tags', sa.MetaData(), autoload_with = op.get_bind())
    user_tags = sa.Table('users_tags_association', sa.MetaData(), autoload_with = op.get_bind())
    TableInit.insert_data_from_file(tags, './migration/csv_data/hobbies.csv', ['id'])
    TableInit.insert_data_from_file(user_tags, './migration/csv_data/user_hobbies.csv')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.text('TRUNCATE tags CASCADE;'))
    # ### end Alembic commands ###
