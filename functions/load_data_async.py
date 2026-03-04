import json
import aiofiles
from database.database import Base, db_init
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from dateutil import parser
from database.database import Video, VideoSnapshot
from config.constants import DATABASE_URL, JSON_PATH


databsase_conn = db_init()

engine = create_async_engine(
    DATABASE_URL, 
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def load_data_async(json_data):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            for v_data in data.get('videos', []):
                
        
                video = Video(
                    id=v_data['id'],
                    creator_id=v_data['creator_id'],
                    video_created_at=parser.parse(v_data['video_created_at']),
                    views_count=v_data['views_count'],
                    likes_count=v_data['likes_count'],
                    comments_count=v_data['comments_count'],
                    reports_count=v_data['reports_count'],
                    created_at=v_data['created_at'],
                    updated_at=v_data['updated_at']
                )
                
                current_snapshots = []
                for s_data in v_data.get('snapshots', []):
                    snapshot = VideoSnapshot(
                        id=s_data['id'],
                        video_id=s_data['video_id'],
                        views_count=s_data['views_count'],
                        likes_count=s_data['likes_count'],
                        comments_count=s_data['comments_count'],
                        reports_count=s_data['reports_count'],
                        delta_views_count=s_data['delta_views_count'],
                        delta_likes_count=s_data['delta_likes_count'],
                        delta_comments_count=s_data['delta_comments_count'],
                        delta_reports_count=s_data['delta_reports_count'],
                        created_at=s_data['created_at'],
                        updated_at=s_data['updated_at']
                    )
                    current_snapshots.append(snapshot)
                
                video.snapshots = current_snapshots
                
                await session.merge(video)
            
            await session.commit()
            
        except Exception as e:
            await session.rollback()
            print(f"Ошибка: {e}")
            raise


async def read_json():
    async with aiofiles.open(JSON_PATH, mode='r', encoding='utf-8') as f:
        content = await f.read()
    
    await load_data_async(content)
