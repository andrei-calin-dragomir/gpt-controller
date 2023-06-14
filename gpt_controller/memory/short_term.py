# Short term memory for the GPT controller
# This is an in-memory database that stores the most recent user inputs, system outputs and other internal data.
# Short term memory flushing is either triggered by the user or by the system. The user can trigger flushing by
# saying "forget everything" or "forget the last thing I said".
# The system can trigger flushing based on the ATTENTION_SPAN parameter found in the `config.py` file.
# TODO #8 Implement short term memory flushing retrieval and storage
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Text, Enum
from sqlalchemy.orm import sessionmaker, relationship, declarative_base 

from gpt_controller.config import SHORT_MEM_URL

engine = create_engine(SHORT_MEM_URL, echo=False)
Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

