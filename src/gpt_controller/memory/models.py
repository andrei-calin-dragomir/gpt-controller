import enum
import itertools
import hashlib
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Time, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
import json
import uuid
from gpt_controller import config

from datetime import datetime

Base = declarative_base()


def model_to_dict(c: Base) -> dict:
    pass
    # return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Define the UserInput model
class UserInput(Base):
    __tablename__ = 'user_inputs'

    id = Column(String, primary_key=True, default=uuid.uuid4)

    context         = Column(Text, nullable=False)
    prompt          = Column(Text, nullable=False)

    iterations      = Column(Integer, nullable=False)
    tokens_used     = Column(Integer, nullable=False)
    time_stamp      = Column(DateTime, default=datetime.utcnow)

    simple_requests = relationship('SimpleRequest', backref='user_input')
    error_counters  = relationship('ErrorCounter', backref='user_input')
    
    def __repr__(self):
        return json.dumps(model_to_dict(self))


# Define the SimpleRequest model
class SimpleRequest(Base):
    __tablename__ = 'simple_requests'

    id              = Column(String, primary_key=True, default=uuid.uuid4)
    user_input_id   = Column(Integer, ForeignKey('user_inputs.id'))

    input_idx       = Column(Integer, nullable=False)
    context         = Column(Text, nullable=False)
    prompt          = Column(String, nullable=False)
    completion      = Column(String, nullable=False)

    iterations      = Column(Integer, nullable=False)
    tokens_used     = Column(Integer, nullable=False)
    time_stamp      = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return json.dumps(model_to_dict(self))

# TODO
# Define the ErrorCounter model
class ErrorCounter(Base):
    __tablename__ = 'error_counters'
    
    id              = Column(String, primary_key=True, default=uuid.uuid4)
    user_input_id   = Column(Integer, ForeignKey('user_inputs.id'))
    
    simple_req_err  = Column(Integer, default=0)
    action_seq_err  = Column(Integer, default=0)
    simple_req_err  = Column(Integer, default=0)
    
    
    def __repr__(self):
        return json.dumps(model_to_dict(self))
    

# # Define the Action model

#     __tablename__ = 'actions'
    
#     id              = Column(String, primary_key=True, default=uuid.uuid4)
    
#     action_type     = Column(Enum(ActionType), nullable=False)
#     description     = Column(Text, nullable=False)
    
#     verb            = Column(String, nullable=False)

# TODO: #5 Finish object model
class Object(Base):

    # The key of a compressionSet entry is a hash calculated from the hashing of all attribute names in each possible combination of attributes
    # The value of a compressionSet entry is a value of the sum or merging of all attribute values in each possible combination of attributes
    compression_set : dict = []

    # IMPORTANT: DO NOT CHANGE THE ORDER OF THE ATTRIBUTES OR THEIR NAMES
    def __init__(self, name, position=None, color=None, size=None, weight=None, number=None):
        self.name = name
        self.position = position
        self.color = color
        self.size = size
        self.weight = weight
        self.number = number # Number of objects of this type
        self.compression_set = self._generate_compression_set()

    def store_in_long_memory(self):
        self.compress_value = self._populate_compression_set()

    # This function is only called when memorizing (from short-term to long-term memory)
    def _populate_compression_set(self):        
        attributes_with_values = {attr: value for attr, value in vars(self).items() if value is not None}
        hash_object = hashlib.md5()
        hash_object.update(str(attributes_with_values).encode('utf-8'))
        self.compression_set[hash_object.hexdigest()].add() # TODO create hashing function for  values of compression set

        return [self.position, self.color, self.size, self.weight]


    # Generates a set of all possible combinations of attributes, if new attributes are added after, the set will be updated
    def _generate_compression_set(self, except_attributes=['compression_set', 'compress_value']):
        if len(self.compression_set) > 0:
            attribute_names = Object.__dict__.keys()
            if except_attributes:
                attribute_names = attribute_names.difference(except_attributes)
            combinations = []
            # Generate all possible combinations of attribute names
            for r in range(1, len(attribute_names) + 1):
                combinations.extend(itertools.combinations(attribute_names, r))
                itertools.compress()

            hashkeys = set()
            # Generate hash keys for each combination
            for combination in combinations:
                hash_object = hashlib.md5()
                hash_object.update(str(combination).encode('utf-8'))
                hashkeys.add(hash_object.hexdigest())
            return hashkeys
        else:
            return self.compression_set