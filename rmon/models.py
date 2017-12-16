"""
该模块实现了所有model类以及相应的序列化类
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from redis import StrictRedis,RedisError
from rmon.common.rest import RestException

db = SQLAlchemy()

class Server(db.Model):
    """
    redis servers model
    """
    __tablename__ = 'redis_server'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    description = db.Column(db.String(512))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer,default=6379)
    password = db.Column(db.String())
    updated_at = db.Column(db.DateTime,default=datetime.utcnow)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    @property
    def redis(self):
        return StrictRedis(host=self.host,port=self.port,password=self.password)

    def __repr__(self):
        return '<Server(name=%s)>' % self.name
    def save(self):
        """
        save to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        delete from database
        """
        db.session.delete(self)
        db.session.commit()

    def ping(self):
        try:
            return self.server.ping()
        except RedisError:
            raise RestException(400,'Redis server %s can not connected' % self.host)

    def get_metrics(self):
        try:
            return self.redis.info()
        except RedisError:
            raise RestException(400,'Redis server %s can not connected' % self.host) 
