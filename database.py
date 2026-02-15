from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔥 PUT YOUR NEON CONNECTION STRING HERE
DATABASE_URL = "postgresql://neondb_owner:npg_gTfKOm7vPjw4@ep-aged-star-aijx3omz-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# ✅ Neon-safe engine configuration
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # prevents dead connection error
    pool_recycle=300,        # refresh connection every 5 mins
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()



