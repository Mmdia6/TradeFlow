from alembic import op
import sqlalchemy as sa
revision="0002_seed_and_idempotency"; down_revision="0001_initial"; branch_labels=None; depends_on=None
def upgrade():
    op.create_table("idempotency_keys",sa.Column("id",sa.Integer(),primary_key=True),sa.Column("user_id",sa.Integer(),sa.ForeignKey("users.id"),nullable=False),sa.Column("key",sa.String(128),nullable=False),sa.Column("request_hash",sa.String(64),nullable=False),sa.Column("order_id",sa.Integer(),sa.ForeignKey("orders.id")),sa.Column("created_at",sa.DateTime(),nullable=False),sa.UniqueConstraint("user_id","key",name="uq_idempotency_user_key"))
    b=op.get_bind()
    for s,n,d in [("USDT","Tether USD",6),("BTC","Bitcoin",8),("ETH","Ethereum",18),("SOL","Solana",9)]:
        b.execute(sa.text("INSERT INTO assets(symbol,name,decimals,is_active,created_at) VALUES(:s,:n,:d,1,CURRENT_TIMESTAMP)"),{"s":s,"n":n,"d":d})
    ids={r.symbol:r.id for r in b.execute(sa.text("SELECT id,symbol FROM assets WHERE symbol IN ('USDT','BTC','ETH','SOL')"))}
    for s,base,quote,pp,qp,mq,mn in [("BTC/USDT",ids["BTC"],ids["USDT"],2,6,"0.000001","10"),("ETH/USDT",ids["ETH"],ids["USDT"],2,5,"0.00001","10"),("SOL/USDT",ids["SOL"],ids["USDT"],3,3,"0.001","10")]:
        b.execute(sa.text("INSERT INTO markets(symbol,base_asset_id,quote_asset_id,price_precision,quantity_precision,min_quantity,min_notional,is_active,created_at) VALUES(:s,:b,:q,:pp,:qp,:mq,:mn,1,CURRENT_TIMESTAMP)"),{"s":s,"b":base,"q":quote,"pp":pp,"qp":qp,"mq":mq,"mn":mn})
def downgrade():
    op.drop_table("idempotency_keys"); b=op.get_bind(); b.execute(sa.text("DELETE FROM markets")); b.execute(sa.text("DELETE FROM assets WHERE symbol IN ('USDT','BTC','ETH','SOL')"))
