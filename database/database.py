from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.constants import DATABASE_URL
from sqlalchemy.orm import relationship


Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(String, primary_key=True)  #
    creator_id = Column(String, index=True)
    video_created_at = Column(DateTime(timezone=True))
    views_count = Column(BigInteger)
    likes_count = Column(Integer)
    comments_count = Column(Integer)
    reports_count = Column(Integer)
    created_at = Column(String)
    updated_at = Column(String)

    snapshots = relationship("VideoSnapshot", backref="video")

class VideoSnapshot(Base):
    __tablename__ = 'video_snapshots'
    
    id = Column(String, primary_key=True)
    video_id = Column(String, ForeignKey('videos.id'), index=True)
    views_count = Column(BigInteger)
    likes_count = Column(Integer)
    comments_count = Column(Integer)
    reports_count = Column(Integer)
    delta_views_count = Column(BigInteger)
    delta_likes_count = Column(Integer)
    delta_comments_count = Column(Integer)
    delta_reports_count = Column(Integer)
    created_at = Column(String, index=True)
    updated_at = Column(String)


def db_init():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    return engine, async_session


async def create_tables():
    engine = create_async_engine(DATABASE_URL)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
