from django.urls import path

from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('create_investment/', CreateInvestmentView.as_view(), name='create-investment'),
    path('investments_list/', InvestmentListView.as_view(), name='investments-list'),
    path('delete_investment/<int:investment_id>/', InvestmentDeleteView.as_view(), name='delete-investment'),
    path('approve_investment/<int:investment_id>/', ApproveInvestmentView.as_view(), name='approve-investment'),
    path('pending_investments/', PendingInvestmentsView.as_view(), name='pending-investments'),
    path('investment/<int:investment_id>/', InvestmentView.as_view(), name='investment-view'),
    path('investment_benefits_view/<int:investment_id>/', InvestmentBenefitsView.as_view(),
         name='investment-benefits-view'),
    path('investment_operating_costs_view/<int:investment_id>/', InvestmentOperatingCostsView.as_view(),
         name='investment-operating-costs-view'),
    path('investment_implementation_costs_view/<int:investment_id>/', InvestmentImplementationCostsView.as_view(),
         name='investment-implementation-costs-view'),
    path('search_project/', SearchProjectView.as_view(), name='search-project'),
]
