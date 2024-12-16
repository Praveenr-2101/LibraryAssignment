
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated 

from rest_framework.exceptions import NotFound
from .models import Author, Book, BorrowRecord
from .serializers import *
from django.utils.timezone import now

# Create your views here.

from django.http import FileResponse
from .tasks import generate_report
from django.conf import settings



class AuthorList(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        try:
            author=Author.objects.all()
            serializers=Authorserializer(author,many=True)
            if serializers:
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response({"message":"No data"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve Author.',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request):
        try:
            data=request.data
            serializers=Authorserializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            return Response(serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            raise NotFound(detail="'Failed to create Author.") 
        

    
class AuthorDetail(APIView):
    
    def get(self,request,pk):
        try:
            author=Author.objects.get(pk=pk)
            serializers=Authorserializer(author)
            if serializers:
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response({"Message":"Author Does Not Exists"},status=status.HTTP_403_FORBIDDEN)
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found with the provided ID.")
    
    def put(self,request,pk):
        try:
            author=Author.objects.get(pk=pk)
            serializers=Authorserializer(author,data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response(serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found with the provided ID.")
    
    def delete(self,request,pk):
        try:
            author=Author.objects.get(pk=pk)
            if author:
                author.delete()
                return Response({"Message":"Data Bas Been Deleted"})
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found with the provided ID.")
        
            
    
    

class BookList(APIView):
    
    def get(self,request):
        try:
            books=Book.objects.all()
            serializers=Bookserilaizer(books,many=True)
            if serializers:
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response({"Message":"NO Content"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve books.',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
    def post(self,request):
        try:
            data=request.data
            serializers=Bookserilaizer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            return Response(serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Failed to create book.',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class BookDetail(APIView):
    
    def get(self,request,pk):
        try:
            book=Book.objects.get(pk=pk)
            serializers=Bookserilaizer(book)
            if serializers:
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response({"Message":"Book Not Found"},status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found with the provided ID.")
    
    
    
    def put(self,request,pk):
        try:
            book=Book.objects.get(pk=pk)
            serializers=Bookserilaizer(book,data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response(serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found with the provided ID.")
        
    def delete(self,request,pk):
        try:
            book=Book.objects.get(pk=pk)
            if book:
                book.delete()
                return Response({"Message":"Data Has Been Deleted"},status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found with the provided ID.")
            
        


class BorrowRecordCreateView(APIView):
    def post(self, request):
        try:
            serializer =BorrowRecordSerilaizer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'error': 'Failed to create Borrow.',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    


class BorrowRecordReturnView(APIView):
    
    def put(self, request, pk):
        try:
            borrow_record = BorrowRecord.objects.get(pk=pk)
            
        except BorrowRecord.DoesNotExist:
            return Response({"detail": "Borrow record not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BorrowRecordSerilaizer(borrow_record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ReportView(APIView):
    def get(self, request):
        report_files = sorted(
            [f for f in os.listdir(settings.REPORTS_DIR) if f.endswith('.json')],
            reverse=True
        )

        if not report_files:
            return Response({"error": "No reports found"}, status=404)

        latest_report = os.path.join(settings.REPORTS_DIR, report_files[0])
        return FileResponse(open(latest_report, 'rb'), as_attachment=True)

    def post(self, request):
        task = generate_report.delay()
        return Response({"message": "Report generation started", "task_id": task.id})


