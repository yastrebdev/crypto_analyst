from sqlalchemy import ForeignKey, DateTime, Index
from sqlalchemy import String, Integer, Float, Numeric
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from datetime import datetime


class Base(DeclarativeBase):
    pass


class Coin(Base):
    __tablename__ = "dim_coins"

    id: Mapped[str] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(30))
    name: Mapped[str]


class ActiveCoin(Base):
    __tablename__ = "active_coins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    api_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    market_charts: Mapped[list["MarketChart"]] = relationship(
        back_populates="coin"
    )

    candles_4h: Mapped[list["Candle"]] = relationship(
        back_populates="coin"
    )

    news: Mapped[list["News"]] = relationship(
        back_populates="coin",
        cascade="all, delete-orphan"
    )


class MarketChart(Base):
    __tablename__ = "market_chart"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    price: Mapped[float] = mapped_column(Numeric(20, 8))
    total_volumes: Mapped[float] = mapped_column(Float)

    coin_api_id: Mapped[str] = mapped_column(String(50))

    coin_id: Mapped[int | None] = mapped_column(
        ForeignKey("active_coins.id", ondelete="SET NULL"),
        nullable=True
    )
    coin: Mapped["ActiveCoin | None"] = relationship(
        back_populates="market_charts"
    )

    __table_args__ = (
        Index('ix_market_chart_coin_timestamp', 'coin_api_id', 'timestamp'),
    )


class Candle(Base):
    __tablename__ = "candles_4h"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    open: Mapped[float] = mapped_column(Numeric(20, 8))
    high: Mapped[float] = mapped_column(Numeric(20, 8))
    low: Mapped[float] = mapped_column(Numeric(20, 8))
    close: Mapped[float] = mapped_column(Numeric(20, 8))
    volume: Mapped[float] = mapped_column(Float)

    coin_api_id: Mapped[str] = mapped_column(String(50))

    coin_id: Mapped[int | None] = mapped_column(
        ForeignKey("active_coins.id", ondelete="SET NULL"),
        nullable=True
    )
    coin: Mapped["ActiveCoin | None"] = relationship(
        back_populates="candles_4h"
    )

    __table_args__ = (
        Index('ix_candles_4h_coin_timestamp', 'coin_api_id', 'timestamp'),
    )


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(60))
    author: Mapped[str | None] = mapped_column(String(200), nullable=True)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(String(500), unique=True)  # URL должен быть уникальным
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    coin_id: Mapped[int] = mapped_column(
        ForeignKey("active_coins.id", ondelete="CASCADE")
    )
    coin: Mapped["ActiveCoin"] = relationship(back_populates="news")

    __table_args__ = (
        Index('ix_news_coin_published', 'coin_id', 'published_at'),
    )