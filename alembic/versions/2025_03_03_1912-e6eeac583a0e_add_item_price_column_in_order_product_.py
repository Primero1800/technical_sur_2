"""add item_price column in order_product_association

Revision ID: e6eeac583a0e
Revises: 48caf4fe0964
Create Date: 2025-03-03 19:12:25.855843

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e6eeac583a0e"
down_revision: Union[str, None] = "48caf4fe0964"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "src_order_product_association",
        sa.Column("item_price", sa.Integer(), server_default="0", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("src_order_product_association", "item_price")
    # ### end Alembic commands ###
