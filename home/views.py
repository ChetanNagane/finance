import imp
from django.shortcuts import redirect, render
from .models import User, Stocks, History
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.contrib import messages
from .forms import *
import requests
# Create your views here.


def getPrice(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS?interval=1d"
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2490.80'
    }
    r = requests.get(url, headers=headers).json()
    return {
        'price': float(r["chart"]["result"][0]["meta"]["regularMarketPrice"]),
        'symbol': r["chart"]["result"][0]["meta"]["symbol"],
    }


def message(request, form):
    for error in form.errors.values():
        messages.error(request, error[0])


def Login(request):
    if(request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid Credentials")
                return render(request, "login.html", {
                    'login': True,
                    'form': form
                })

        message(request, form)
        return render(request, "login.html", {
            'login': True,
            "form": form
        })

    return render(request, "login.html", {
        'login': True,
        'form': LoginForm()
    })


def Register(request):
    if(request.method == "POST"):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

        message(request, form)
        return render(request, "login.html", {
            'login': False,
            "form": form
        })

    return render(request, "login.html", {
        'login': False,
        'form': RegisterForm()
    })


@login_required
def Home(request):
    if request.method == "GET":
        stocks = Stocks.objects.filter(user=request.user)
        invest_value = 0
        current_value = 0
        for stock in stocks:
            stock.LTP = round(getPrice(stock.symbol)["price"], 2)
            current_value = current_value + stock.LTP*stock.quantity
            invest_value = invest_value + stock.price*stock.quantity

        # invest_value = Stocks.objects.filter(user=request.user).aggregate(total=Sum(F('quantity')*F('price')))['total']
        # current_value = Stocks.objects.filter(user=request.user).aggregate(total=Sum(F('quantity')*('LTP')))['total']

        return render(request, "home.html", {
            'table': stocks,
            'invest_value': round(invest_value, 2),
            'current_value': round(current_value, 2),
            'profit_loss': round(current_value - invest_value, 2),

        })


@login_required
def Quote(request):
    if(request.method == "POST"):
        form = QuoteForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data["symbol"]
            try:
                stock_data = getPrice(symbol)
                price = stock_data["price"]
                symbol = stock_data["symbol"][:-3]
            except:
                messages.error(request, "Invalid Symbol")
                return render(request, "quote.html", {
                    'form': form
                })
            return render(request, "quote.html", {
                'price': price,
                'symbol': symbol,
                'form': form
            })
        message(request, form)
        return render(request, "quote.html", {
            'form': form
        })

    return render(request, "quote.html", {
        'form': QuoteForm()
    })


@login_required
def Buy(request):
    if(request.method == "POST"):
        form = BuyForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data["symbol"]
            quantity = form.cleaned_data["quantity"]
            try:
                stock_data = getPrice(symbol)
                current_price = stock_data["price"]
                symbol = stock_data["symbol"][:-3]
            except:
                messages.error(request, "Invalid Symbol")
                return render(request, "buy.html", {
                    'form': form
                })
            if(request.user.cash < current_price*quantity):
                messages.error(request, "Insufficient Cash")
                return render(request, "buy.html", {
                    'form': form
                })
            try:
                stock = Stocks.objects.get(user=request.user, symbol=symbol)
            except:
                stock = Stocks.objects.create(user=request.user, quantity=0, symbol=symbol, price=0)
            stock.price = round((stock.price*stock.quantity + current_price*quantity)/(stock.quantity + quantity), 2)
            stock.quantity = stock.quantity + quantity
            History.objects.create(user=request.user, quantity=quantity, price=current_price, symbol=symbol)
            stock.save()
            request.user.cash = request.user.cash - current_price*quantity
            request.user.save()
            messages.success(request, f'{quantity} Stocks of {symbol} Bought')
            return redirect('home')

        return render(request, "buy.html", {
            'form': form
        })

    return render(request, "buy.html", {
        'form': BuyForm()
    })


@login_required
def Sell(request):
    if request.method == 'POST':
        stocks = Stocks.objects.filter(user=request.user).values_list("symbol", flat=True)
        form = SellForm(data=request.POST, choice=stocks)

        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            quantity = form.cleaned_data['quantity']
            stock_data = getPrice(symbol)
            current_price = stock_data["price"]
            symbol = stock_data["symbol"][:-3]
            stock = Stocks.objects.get(user=request.user, symbol=symbol)
            if(stock.quantity < quantity):
                messages.error(request, "Insufficient Stock")
                return render(request, 'sell.html', {
                    'form': form
                })
            stock.quantity = stock.quantity - quantity
            History.objects.create(user=request.user, quantity=-quantity, price=current_price, symbol=symbol)
            stock.save()
            request.user.cash = request.user.cash + current_price*quantity
            request.user.save()
            messages.success(request, f'{quantity} Stocks of {symbol} Sold')
            return redirect('home')

        message(request, form)
        stocks = Stocks.objects.filter(user=request.user).values_list("symbol", flat=True)
        return render(request, 'sell.html', {
            'form': form
        })

    stocks = Stocks.objects.filter(user=request.user).values_list("symbol", flat=True)
    return render(request, 'sell.html', {
        'form': SellForm(choice=stocks)
    })


@login_required
def Historys(request):
    if request.method == 'GET':
        history = History.objects.filter(user=request.user)
        return render(request, 'history.html', {
            'table': history
        })


def Logout(request):
    logout(request)
    return redirect('login')
