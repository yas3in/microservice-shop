from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, ConfigDict


# ==========================================
# SQLModel Database Entities (DrawSQL Schema)
# ==========================================

class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    parent: Optional[int] = Field(default=None, foreign_key="categories.id", nullable=True, index=True)


class Brand(SQLModel, table=True):
    __tablename__ = "brands"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    parent: Optional[int] = Field(default=None, foreign_key="brands.id", nullable=True, index=True)


class ProductType(SQLModel, table=True):
    __tablename__ = "product_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)


class ProductAttribute(SQLModel, table=True):
    __tablename__ = "product_attributes"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    product_type: int = Field(foreign_key="product_types.id", nullable=False, index=True)
    attribute_type: str = Field(default="text", nullable=False)  # text, integer, float, boolean, select


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    upc: str = Field(unique=True, index=True, nullable=False)
    title: str = Field(index=True, nullable=False)
    description: str = Field(default="", nullable=False)
    type: int = Field(foreign_key="product_types.id", nullable=False, index=True)
    category: int = Field(foreign_key="categories.id", nullable=False, index=True)
    brand: Optional[int] = Field(default=None, foreign_key="brands.id", nullable=True, index=True)


class ProductAttributeValue(SQLModel, table=True):
    __tablename__ = "product_attribute_values"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_attribute: int = Field(foreign_key="product_attributes.id", nullable=False, index=True)
    value: str = Field(nullable=False)
    product: int = Field(foreign_key="products.id", nullable=False, index=True)


# ==========================================
# Pydantic Schemas / DTOs
# ==========================================

# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    parent: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent: Optional[int] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CategoryTreeRead(CategoryRead):
    children: List["CategoryTreeRead"] = []


# --- Brand Schemas ---
class BrandBase(BaseModel):
    name: str
    parent: Optional[int] = None


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    parent: Optional[int] = None


class BrandRead(BrandBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- ProductType Schemas ---
class ProductTypeBase(BaseModel):
    title: str


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeUpdate(BaseModel):
    title: Optional[str] = None


class ProductTypeRead(ProductTypeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- ProductAttribute Schemas ---
class ProductAttributeBase(BaseModel):
    name: str
    product_type: int
    attribute_type: str = "text"


class ProductAttributeCreate(ProductAttributeBase):
    pass


class ProductAttributeUpdate(BaseModel):
    name: Optional[str] = None
    product_type: Optional[int] = None
    attribute_type: Optional[str] = None


class ProductAttributeRead(ProductAttributeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- ProductAttributeValue Schemas ---
class AttributeValueInput(BaseModel):
    product_attribute: int
    value: str


class ProductAttributeValueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_attribute: int
    attribute_name: Optional[str] = None
    value: str
    product: int


# --- Product Schemas ---
class ProductBase(BaseModel):
    upc: str
    title: str
    description: str = ""
    type: int
    category: int
    brand: Optional[int] = None


class ProductCreate(ProductBase):
    attributes: Optional[List[AttributeValueInput]] = None


class ProductUpdate(BaseModel):
    upc: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[int] = None
    category: Optional[int] = None
    brand: Optional[int] = None
    attributes: Optional[List[AttributeValueInput]] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductDetailRead(ProductRead):
    category_name: Optional[str] = None
    brand_name: Optional[str] = None
    type_title: Optional[str] = None
    attributes: List[ProductAttributeValueRead] = []
