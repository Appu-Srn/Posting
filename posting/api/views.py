from rest_framework import generics, mixins
from posting.models import *
from .permissions import *
from .serializers import *

class BlogPostApiView(mixins.CreateModelMixin, generics.ListAPIView): #detail view created
    lookup_field = 'pk'
    serializer_class = BlogPostSerializer
    permission_classes = []

    # queryset = BlogPost.objects.all()

    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(title__icontains=query)|
                           Q(content__icontains=query)
                           ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView): #detail view created
    lookup_field = 'pk'
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = BlogPost.objects.all()

    def get_queryset(self):
        return BlogPost.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #     pk=self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)

