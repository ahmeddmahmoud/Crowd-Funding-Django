from django.shortcuts import render
from django.shortcuts import render , get_object_or_404 ,redirect, reverse
from project.models import Project
from django.views import generic
from django.db.models import Q

# Create your views here.



class projectSearchView(generic.ListView):
    template_name = 'project/crud/list.html'
    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        projects = Project.objects.filter(
            Q(title__icontains=search_query)
        )
        print(projects)
        self.extra_context = {'search_query': search_query}
        return projects


def products_index(request):
    projects=Project.objects.all()
    latest_books = projects.order_by('-created_at')[:4]
    latest_featured_projects = Project.objects.filter(is_featured=True).order_by('-featured_at')[:5]

    sorted_products = sorted(projects, key=lambda p: p.rate, reverse=True)

    # Get the top five products
    top_five_products = sorted_products[:5]
    print("Top Five Product Rates:")
    for product in top_five_products:
        print(f"Product: {product.title}, Rate: {product.rate}")
    return render(request , 'homepage/home.html' ,
                  context={"projects" : projects,"latest_books":latest_books,
                           "top_five_products": top_five_products, "latest_featured_projects":latest_featured_projects
                           })