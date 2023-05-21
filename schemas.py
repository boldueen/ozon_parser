from pydantic import BaseModel


class TypePrice(BaseModel):
    coefficient: float
    min: float
    max: float


class OzonPrice(BaseModel):
    volume_weight: float
    fbs: TypePrice
    fbo: TypePrice

    def __lt__(self, other):
        return self.volume_weight < other.volume_weight


class ReqCatFee(BaseModel):
    category_id: int
    level: int
    name: str


class OzonCategoryFee(BaseModel):
    base_category: ReqCatFee
    marketplace_category: str = ''
    fee: float = 0
    delivered_percent: float = 0

    def __lt__(self, other):
        return self.marketplace_category < other.marketplace_category
