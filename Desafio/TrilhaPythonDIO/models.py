import sqlalchemy as sa
from .database import metadata

accounts = sa.Table(
    "accounts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.Integer, unique=True, nullable=False),
    sa.Column("balance", sa.Float, default=0),
)

transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("account_id", sa.Integer, sa.ForeignKey("accounts.id")),
    sa.Column("amount", sa.Float, nullable=False),
    sa.Column("type", sa.String, nullable=False),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
)
