from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import CreateInvestmentForm, ApproverForm, AddBenefitForm, AddOperatingCostForm, SearchForm, AddAssetForm, \
    AddImplementationCostForm
from .models import *


class MainView(View):
    def get(self, request):
        return render(request, "investment_tool/main.html")

    def post(self, request):
        return render(request, "investment_tool/main.html")


class CreateInvestmentView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateInvestmentForm
        title = "Stwórz nowy projekt"
        return render(request, "investment_tool/form.html", {'form': form, 'title': title})

    def post(self, request):
        form = CreateInvestmentForm(request.POST)
        if form.is_valid():
            name = form.data.get('name')
            description = form.data.get('description')
            Investment.objects.create(name=name, description=description,
                                      created_by=request.user)
            messages.success(request, "Inwestycja została utworzona")
            return redirect('main')
        messages.warning(request, "Wprowadzono błędne dane")
        return redirect('main')


class InvestmentListView(LoginRequiredMixin, View):
    def get(self, request):
        user_investments = Investment.objects.filter(created_by=request.user)
        return render(request, "investment_tool/investment_list.html",
                      {'user_investments': user_investments})


class PendingInvestmentsView(LoginRequiredMixin, View):
    def get(self, request):
        approver_investments = Investment.objects.filter(approver=request.user)
        return render(request, "investment_tool/pending_investments.html",
                      {'approver_investments': approver_investments})


class InvestmentDeleteView(LoginRequiredMixin, View):
    def get(self, request, investment_id):

        investment = get_object_or_404(Investment, id=investment_id)

        if investment.created_by == request.user or investment.approver == request.user:
            investment.delete()
            messages.success(request, "Wniosek został skasowany")
        else:
            raise Http404("Brak uprawnień")

        return redirect("investments-list")


class ApproveInvestmentView(LoginRequiredMixin, View):
    def get(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()

        if request.user in investment_approvers:
            investment.approved = True
            investment.save()
            messages.success(request, "Wniosek został zaakceptowany")
        else:
            raise Http404("Brak uprawnień")

        return redirect("investments-list")


class InvestmentView(LoginRequiredMixin, View):
    def get(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()
        if investment.created_by == request.user or request.user in investment_approvers:
            form = ApproverForm(initial={'approver': investment_approvers})

            return render(request, "investment_tool/investment_view.html", {'investment': investment, 'form': form})

        else:
            raise Http404("Brak uprawnień")

    def post(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()

        if investment.created_by == request.user or request.user in investment_approvers:
            form_post = ApproverForm(request.POST)
            approvers = form_post.data.get('approver')

            for item in approvers:
                user = get_object_or_404(User, id=item)
                if user not in investment_approvers:
                    investment.approver.add(user)

            messages.success(request, "Dodano akceptujących do wniosku")
            return render(request, "investment_tool/investment_view.html", {'investment': investment})

        else:
            raise Http404("Brak uprawnień")


class InvestmentBenefitsView(LoginRequiredMixin, View):
    def get(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()
        form = AddBenefitForm(initial={'investment': investment})

        benefits = Benefit.objects.filter(investment=investment).order_by('date')
        sum_of_benefits = 0

        for benefit in benefits:
            sum_of_benefits += benefit.amount

        if investment.created_by == request.user or request.user in investment_approvers:

            return render(request, "investment_tool/investment_benefits.html", {'investment': investment,
                                                                                'form': form,
                                                                                'benefits': benefits,
                                                                                'total': sum_of_benefits})
        else:
            raise Http404("Brak uprawnień")

    def post(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()

        benefits = Benefit.objects.filter(investment=investment).order_by('date')
        sum_of_benefits = 0

        for benefit in benefits:
            sum_of_benefits += benefit.amount

        if investment.created_by == request.user or request.user in investment_approvers:
            form_post = AddBenefitForm(request.POST)
            form = AddBenefitForm(initial={'investment': investment})

            if form_post.is_valid():
                start_date = form_post.cleaned_data.get('start_date')
                end_date = form_post.cleaned_data.get('end_date')
                name = form_post.cleaned_data.get('name')
                amount = form_post.cleaned_data.get('amount')

                if start_date > end_date:
                    messages.warning(request, "Data początkowa jest późniejsza od końcowej")
                    return render(request, "investment_tool/investment_benefits.html", {'investment': investment,
                                                                                        'form': form,
                                                                                        'benefits': benefits,
                                                                                        'total': sum_of_benefits})

                date = start_date
                dates_list = [date]

                while date < end_date:
                    date += relativedelta(months=1)
                    if date > end_date:
                        dates_list.append(end_date)
                    else:
                        dates_list.append(date)

                for date in dates_list:
                    new_benefit = Benefit.objects.create(amount=amount, investment=investment, name=name,
                                                         date=date)
                    new_benefit.save()

                messages.success(request, "Informacja została dodana")
            else:
                messages.warning(request, "Podano nieprawidłowe dane")

            benefits = Benefit.objects.filter(investment=investment).order_by('date')
            sum_of_benefits = 0

            for benefit in benefits:
                sum_of_benefits += benefit.amount

            return render(request, "investment_tool/investment_benefits.html",
                          {'investment': investment, 'form': form, 'benefits': benefits, 'total': sum_of_benefits})

        else:
            raise Http404("Brak uprawnień")


class InvestmentOperatingCostsView(LoginRequiredMixin, View):
    def get(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()
        form = AddOperatingCostForm(initial={'investment': investment})
        costs = OperatingCost.objects.filter(investment=investment)

        sum_of_costs = 0

        for cost in costs:
            sum_of_costs += cost.amount

        if investment.created_by == request.user or request.user in investment_approvers:

            return render(request, "investment_tool/investment_operating_costs.html", {'investment': investment,
                                                                                       'form': form,
                                                                                       'costs': costs,
                                                                                       'total': sum_of_costs,
                                                                                       })
        else:
            raise Http404("Brak uprawnień")

    def post(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()

        costs = OperatingCost.objects.filter(investment=investment)

        sum_of_costs = 0

        for cost in costs:
            sum_of_costs += cost.amount

        if investment.created_by == request.user or request.user in investment_approvers:
            form_post = AddOperatingCostForm(request.POST)
            form = AddOperatingCostForm(initial={'investment': investment})

            if form_post.is_valid():
                start_date = form_post.cleaned_data.get('start_date')
                end_date = form_post.cleaned_data.get('end_date')
                name = form_post.cleaned_data.get('name')
                amount = form_post.cleaned_data.get('amount')

                if start_date > end_date:
                    messages.warning(request, "Data początkowa jest późniejsza od końcowej")
                    return render(request, "investment_tool/investment_operating_costs.html", {'investment': investment,
                                                                                               'form': form,
                                                                                               'costs': costs,
                                                                                               'total': sum_of_costs,
                                                                                               })

                date = start_date
                dates_list = [date]

                while date < end_date:
                    date += relativedelta(months=1)
                    if date > end_date:
                        dates_list.append(end_date)
                    else:
                        dates_list.append(date)

                for date in dates_list:
                    new_cost = OperatingCost.objects.create(amount=amount, investment=investment,
                                                            name=name,
                                                            date=date)
                    new_cost.save()

                messages.success(request, "Informacja została dodana")
            else:
                messages.warning(request, "Podano nieprawidłowe dane")

            costs = OperatingCost.objects.filter(investment=investment)

            sum_of_costs = 0

            for cost in costs:
                sum_of_costs += cost.amount

            return render(request, "investment_tool/investment_operating_costs.html", {'investment': investment,
                                                                                       'form': form,
                                                                                       'costs': costs,
                                                                                       'total': sum_of_costs,
                                                                                       })

        else:
            raise Http404("Brak uprawnień")


class InvestmentImplementationCostsView(LoginRequiredMixin, View):
    def get(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()
        form = AddImplementationCostForm(initial={'investment': investment})
        costs = ImplementationCost.objects.filter(investment=investment)

        sum_of_costs = 0

        for cost in costs:
            sum_of_costs += cost.amount

        assets = Asset.objects.filter(investment=investment)

        sum_of_assets = 0

        for asset in assets:
            sum_of_assets += asset.amount

        if investment.created_by == request.user or request.user in investment_approvers:
            return render(request, "investment_tool/investment_implementation.html", {'investment': investment,
                                                                                      'form': form,
                                                                                      'costs': costs,
                                                                                      'total_costs': sum_of_costs,
                                                                                      'assets': assets,
                                                                                      'total_assets': sum_of_assets,
                                                                                      })
        else:
            raise Http404("Brak uprawnień")

    def post(self, request, investment_id):

        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()

        costs = ImplementationCost.objects.filter(investment=investment)

        sum_of_costs = 0

        for cost in costs:
            sum_of_costs += cost.amount

        assets = Asset.objects.filter(investment=investment)

        sum_of_assets = 0

        for asset in assets:
            sum_of_assets += asset.amounts

        if investment.created_by == request.user or request.user in investment_approvers:
            form_post = AddImplementationCostForm(request.POST)
            form = AddImplementationCostForm(initial={'investment': investment})

            if form_post.is_valid():
                date = form_post.cleaned_data.get('date')
                name = form_post.cleaned_data.get('name')
                amount = form_post.cleaned_data.get('amount')
                new_cost = ImplementationCost.objects.create(investment=investment, name=name, date=date, amount=amount)
                new_cost.save()

                messages.success(request, "Informacja została dodana")
            else:
                messages.warning(request, "Podano nieprawidłowe dane")

            costs = ImplementationCost.objects.filter(investment=investment)

            sum_of_costs = 0

            for cost in costs:
                sum_of_costs += cost.amount

            return render(request, "investment_tool/investment_implementation.html", {'investment': investment,
                                                                                      'form': form,
                                                                                      'costs': costs,
                                                                                      'total_costs': sum_of_costs,
                                                                                      'assets': assets,
                                                                                      'total_assets': sum_of_assets,
                                                                                      })

        else:
            raise Http404("Brak uprawnień")


class InvestmentAssetsView(LoginRequiredMixin, View):
    def get(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()
        form = AddAssetForm(initial={'investment': investment})
        costs = ImplementationCost.objects.filter(investment=investment)

        sum_of_costs = 0

        for cost in costs:
            sum_of_costs += cost.amount

        assets = Asset.objects.filter(investment=investment)

        sum_of_assets = 0

        for asset in assets:
            sum_of_assets += asset.amount

        if investment.created_by == request.user or request.user in investment_approvers:
            return render(request, "investment_tool/investment_implementation_asset.html", {'investment': investment,
                                                                                            'form': form,
                                                                                            'costs': costs,
                                                                                            'total_costs': sum_of_costs,
                                                                                            'assets': assets,
                                                                                            'total_assets': sum_of_assets,
                                                                                            })
        else:
            raise Http404("Brak uprawnień")

    def post(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id)
        investment_approvers = investment.approver.all()

        costs = ImplementationCost.objects.filter(investment=investment)

        sum_of_costs = 0

        for cost in costs:
            sum_of_costs += cost.amount

        assets = Asset.objects.filter(investment=investment)

        sum_of_assets = 0

        for asset in assets:
            sum_of_assets += asset.amount

        if investment.created_by == request.user or request.user in investment_approvers:
            form_post = AddAssetForm(request.POST)
            form = AddAssetForm(initial={'investment': investment})

            if form_post.is_valid():
                date = form_post.cleaned_data.get('date')
                name = form_post.cleaned_data.get('name')
                amount = form_post.cleaned_data.get('amount')
                depreciation_period = form_post.cleaned_data.get('depreciation_period')
                new_asset = Asset.objects.create(investment=investment, name=name, date=date, amount=amount,
                                                 depreciation_period=depreciation_period)
                new_asset.save()

                messages.success(request, "Informacja została dodana")
            else:
                messages.warning(request, "Podano nieprawidłowe dane")

            assets = Asset.objects.filter(investment=investment)

            sum_of_assets = 0

            for asset in assets:
                sum_of_assets += asset.amount

            return render(request, "investment_tool/investment_implementation.html", {'investment': investment,
                                                                                      'form': form,
                                                                                      'costs': costs,
                                                                                      'total_costs': sum_of_costs,
                                                                                      'assets': assets,
                                                                                      'total_assets': sum_of_assets,
                                                                                      })

        else:
            raise Http404("Brak uprawnień")


class SearchProjectView(LoginRequiredMixin, View):
    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('name')
            results_created = Investment.objects.filter(name__icontains=search,
                                                        created_by=request.user) | Investment.objects.filter(
                description__icontains=search, created_by=request.user)
            results_approver = Investment.objects.filter(name__icontains=search,
                                                         approver=request.user) | Investment.objects.filter(
                description__icontains=search, approver=request.user)
            results = results_created | results_approver

            return render(request, 'investment_tool/search_projects.html',
                          {'results': results})
        else:
            messages.warning(request, "Brak wyników wyszukiwania")
            return redirect('main')


class DeleteBenefitView(LoginRequiredMixin, View):
    def get(self, request, benefit_id):
        benefit = get_object_or_404(Benefit, id=benefit_id)
        investment = get_object_or_404(Investment, id=benefit.investment.id)
        investment_approvers = investment.approver.all()

        if investment.created_by == request.user or request.user in investment_approvers:
            benefit.delete()

            return redirect('investment-benefits-view', investment_id=investment.id)
        else:
            raise Http404("Brak uprawnień")


class DeleteOperatingCostView(LoginRequiredMixin, View):
    def get(self, request, cost_id):
        cost = get_object_or_404(OperatingCost, id=cost_id)
        investment = get_object_or_404(Investment, id=cost.investment.id)
        investment_approvers = investment.approver.all()

        if investment.created_by == request.user or request.user in investment_approvers:
            cost.delete()

            return redirect('investment-operating-costs-view', investment_id=investment.id)
        else:
            raise Http404("Brak uprawnień")


class DeleteAssetView(LoginRequiredMixin, View):
    def get(self, request, asset_id):
        asset = get_object_or_404(Asset, id=asset_id)
        investment = get_object_or_404(Investment, id=asset.investment.id)
        investment_approvers = investment.approver.all()

        if investment.created_by == request.user or request.user in investment_approvers:
            asset.delete()

            return redirect('investment-implementation-costs-view', investment_id=investment.id)
        else:
            raise Http404("Brak uprawnień")


class DeleteImplementationCostView(LoginRequiredMixin, View):
    def get(self, request, cost_id):
        cost = get_object_or_404(ImplementationCost, id=cost_id)
        investment = get_object_or_404(Investment, id=cost.investment.id)
        investment_approvers = investment.approver.all()

        if investment.created_by == request.user or request.user in investment_approvers:
            cost.delete()

            return redirect('investment-implementation-costs-view', investment_id=investment.id)
        else:
            raise Http404("Brak uprawnień")
