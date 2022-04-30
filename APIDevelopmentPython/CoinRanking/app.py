from datetime import datetime
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, Boolean, create_engine, CheckConstraint
, select, BIGINT, DECIMAL)
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
import GetStatsData


metadata = MetaData()
# MySQl Connection
engine = create_engine("mysql+pymysql://prashant:admin123@@localhost:3306/coins")
Base = declarative_base()




# Load the stats table
class Stats(Base):
    __tablename__ = 'stats'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    total = Column(BIGINT, nullable=True)
    total_coins = Column(BIGINT, nullable=True)
    total_markets = Column(BIGINT, nullable=True)
    total_exchanges = Column(BIGINT, nullable=True)
    total_market_cap = Column(BIGINT, nullable=True)
    total_24h_vol = Column(BIGINT, nullable=True)

    def __init__(self, total, total_coins, total_markets, total_exchanges,
                 total_market_cap,
                 total_24h_vol):
        # self.id = id
        self.total = total
        self.total_coins = total_coins
        self.total_markets = total_markets
        self.total_exchanges = total_exchanges
        self.total_market_cap = total_market_cap
        self.total_24h_vol = total_24h_vol

    def __repr__(self):
        return f"Stats(id = {self.id}," \
               f"total={self.total}," \
               f"total_coins={self.total_coins}," \
               f"total_markets={self.total_markets}," \
               f"total_market_cap={self.total_market_cap}," \
               f"total_24h_vol={self.total_24h_vol}".format(self=self)


Session = sessionmaker(bind=engine)
session = Session()

#stats2 = Stats(20, 0, 0, 0, 0, 0, 0, 0)
stats_response = GetStatsData.get_stats_data()
stats = Stats(
    stats_response.get('total'),
    stats_response.get('total_coins'),
    stats_response.get('totalMarkets'),
    stats_response.get('totalExchanges'),
    stats_response.get('totalMarketCap'),
    stats_response.get('total24hVolume')
)

print(stats)
# Add the instance to the session
session.add(stats)

# Commit the data to the database
session.commit()

# Print the ID
print(stats.id)
