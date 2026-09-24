from decimal import Decimal
from pydantic import BaseModel,ConfigDict,EmailStr,Field
from app.models.order import OrderSide,OrderStatus,OrderType
class Credentials(BaseModel): email:EmailStr; password:str=Field(min_length=8,max_length=128)
class TokenResponse(BaseModel): access_token:str; refresh_token:str; token_type:str="bearer"
class RefreshRequest(BaseModel): refresh_token:str
class MessageResponse(BaseModel): message:str
class MarketResponse(BaseModel):
    id:int; symbol:str; base_asset:str; quote_asset:str; price:Decimal; price_precision:int; quantity_precision:int; min_quantity:Decimal; min_notional:Decimal
class OrderCreate(BaseModel):
    market:str; side:OrderSide; type:OrderType; quantity:Decimal=Field(gt=0); limit_price:Decimal|None=Field(default=None,gt=0)
class OrderResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; market:str; side:OrderSide; type:OrderType; status:OrderStatus; quantity:Decimal; filled_quantity:Decimal; limit_price:Decimal|None; average_fill_price:Decimal|None; reserved_amount:Decimal
class AccountResponse(BaseModel): asset:str; available_balance:Decimal; locked_balance:Decimal
class PortfolioAsset(BaseModel): asset:str; quantity:Decimal; current_value:Decimal; average_entry:Decimal|None; unrealized_pnl:Decimal
class PortfolioResponse(BaseModel): total_value:Decimal; realized_pnl:Decimal; unrealized_pnl:Decimal; assets:list[PortfolioAsset]
class TradeResponse(BaseModel): id:int; market:str; side:OrderSide; quantity:Decimal; price:Decimal; quote_amount:Decimal; fee:Decimal
