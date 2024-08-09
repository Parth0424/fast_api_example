from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'mymodel'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(String)

async def async_transaction_with_rollback(async_session: AsyncSession):
    try:
        async with async_session.begin():
            # Transaction starts here
            stmt = select(MyModel).where(MyModel.id == 1)
            result = await async_session.execute(stmt)
            instance = result.scalar_one()
            
            # Modify instance
            instance.value = 'new_value'
            
            # Simulate an error
            raise ValueError("Simulated error")
            
            # Transaction is committed here if no exceptions occur
    except Exception as e:
        print(f"Transaction failed: {e}")
        # Transaction is rolled back
