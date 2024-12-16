from rest_framework import serializers
from .models import Author, Book, BorrowRecord
from datetime import date

class Authorserializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=['id','name','bio']
        

class Bookserilaizer(serializers.ModelSerializer):
    author=Authorserializer()
    class Meta:
        model=Book
        fields=['id', 'title', 'author','available_copies']
        
    def validate_available_copies(self,value):
        if value <=0:
            raise serializers.ValidationError("Add Copies")
        return value
        
    def create(self,validated_data):
        author_data = validated_data.pop('author')
        book = Book.objects.create(**validated_data)  
        Author.objects.create(book=book, **author_data)
        return book
    
    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)

        instance.title = validated_data.get('title', instance.title)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.available_copies = validated_data.get('available_copies', instance.available_copies)
        instance.save()
        
        if author_data:
            author = instance.author 
            author.name = author_data.get('name', author.name)
            author.bio = author_data.get('bio', author.bio)
            author.save()

        return instance

class BorrowRecordSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=BorrowRecord
        fields=['id', 'book', 'borrowed_by', 'borrowed_date', 'return_date']
        
    
    def create(self, validated_data):
        book = validated_data.get('book') 
        borrowed_by = validated_data.get('borrowed_by')  
        if book.available_copies <= 0:
            raise serializers.ValidationError("No available copies left for this book.")
        borrow_record = BorrowRecord.objects.create(**validated_data)
        return borrow_record
    
    def update(self, instance, validated_data):
        if instance.return_date is not None:
            raise serializers.ValidationError("This book has already been returned.")

        instance.return_date = validated_data.get('return_date', date.today())
        instance.book.available_copies += 1
        instance.book.save()
        instance.save()
        
        return instance