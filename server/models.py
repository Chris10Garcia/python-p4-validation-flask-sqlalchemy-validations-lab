from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
import re

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    @validates('name')
    def check_name(self, key, address):
        if address == "":
            raise ValueError("Please input a name")
        if Author.query.filter(Author.name == address).first():
            raise ValueError("Name already exist in the DB")        
        return address
    
    @validates('phone_number')
    def check_phone(self, key, address):
        if len(address) != 10:
            raise ValueError("Please input a correct 10 digit number")
        return address
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    @validates("title")
    def check_title(self, key, address):
        if address == "":
            raise ValueError("Please input a title")
        # return address
        clickbait_titles = [
            "Won't Believe",
            "Secret",
            "Top",
            "Guess"
        ]

        for title in clickbait_titles:
            pattern = rf"{title}"
            regex = re.compile(pattern)
            match = regex.search(address)

            if not match:
                raise ValueError("Title is not click-baity enough")
        
        return address

    @validates("content")
    def check_content(self, key, address):
        if len(address) < 250:
            raise ValueError("Content length is insufficient")
        return address

    @validates("summary")
    def check_summary(self, key, address):
        if len(address) >= 250:
            raise ValueError ("Summary is too long")
        return address
    
    @validates("category")
    def check_category(self, key, address):
        if address != "Fiction" and address != "Non-Fiction":
            raise ValueError ("Category should be Fiction or Non-Fiction")
        return address


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250))
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
