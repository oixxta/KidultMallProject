from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
import random

# Create your views here.

##메인페이지
def mainPage(request):
    bannerImages = ['mainBanner1.jpg', 'mainBanner2.jpg', 'mainBanner3.jpg', 'mainBanner4.jpg']
    selectedBanner = random.choice(bannerImages)
    return render(request, 'mainPage.html', {'bannerImage':selectedBanner})

##로그인
def loginView(request):
    if request.method == "POST":
        userId=request.POST['userId']
        password=request.POST['password']

        try:
            user = Member.objects.get(userId = userId)
            if password == user.password:
                request.session['userId'] = user.no
                request.session['userNickname'] = user.nickname
                return redirect('mainPage')
            else:
                messages.error(request, "비밀번호가 틀렸습니다")
        except Member.DoesNotExist:
            messages.error(request, "존재하지 않는 사용자입니다.")
    return render(request, 'login.html')

##로그아웃
def logoutView(request):
    request.session.flush()
    messages.success(request, '성공적으로 로그아웃 되었습니다.')
    return redirect('mainPage')

##회원가입
def register(request):
    if request.method == "POST":
        userId = request.POST.get('userId')
        password = request.POST.get('password')
        name = request.POST.get('name')
        nickname = request.POST.get('nickname')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phoneNumber = request.POST.get('phoneNumber')
        address = request.POST.get('address')

        if Member.objects.filter(userId = userId).exists():
            messages.error(request, "이미 존재하는 아이디입니다!")
            return redirect('register')

        newMember = Member.objects.create(
            userId=userId,
            password=password,
            name=name,
            nickname=nickname,
            gender=gender,
            email=email,
            phoneNumber=phoneNumber,
            address=address
        )

        Cart.objects.create(cartOwner = newMember)

        messages.success(request, "회원가입이 완료되었습니다.")
        return redirect('login')
    return render(request, 'register.html')

##신규입고
def newArrivalsView(request):
    products = Product.objects.all().filter(category='new')
    return render(request, 'newArrivalsView.html', {'products': products})

##남자어른이
def forKidultBoysView(request):
    products = Product.objects.all().filter(category='boy')
    return render(request, 'forKidultBoysView.html', {'products': products})

##여자어른이
def forKidultGirlsView(request):
    products = Product.objects.all().filter(category='girl')
    return render(request, 'forKidultGirlsView.html', {'products': products})

##제품문의(상담게시판)
def boardList(request):
    boards = Board.objects.all().order_by('-created_at')
    return render(request, 'boardList.html', {'boards': boards})

def boardWrite(request):
    if request.method == 'POST':
        Board.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            content=request.POST['content'] 
        )
        return redirect('boardList')
    return render(request, 'boardWrite.html')

def boardDetail(request, boardId):
    board = get_object_or_404(Board, no=boardId)
    board.showCount += 1
    board.save()
    return render(request, 'boardDetail.html', {'board':board})

def boardUpdate(request, boardId):
    board = get_object_or_404(Board, no=boardId)

    if request.method == 'POST':
        board.title = request.POST['title']
        board.author = request.POST['author']
        board.content = request.POST['content']
        board.save()
        messages.success(request, '게시글이 수정되었습니다.')
        return redirect('boardDetail', boardId=board.no)
    
    return render(request, 'boardUpdate.html', {'board': board})

##장바구니
def basketView(request):
    userId = request.session.get('userId')
    if not userId:
        messages.success(request, '로그인이 필요한 서비스입니다.')
        return redirect('login')
    user = Member.objects.get(no = userId)
    return render(request, 'basketView.html', {'user':user})

def addToCart(request):
    if request.method == "POST":
        userId = request.session.get('userId')
        if not userId:
            messages.success(request, '로그인이 필요한 서비스입니다.')
            return redirect('login')
        member = get_object_or_404(Member, no=userId)
        productId = request.POST.get('productId')
        product = get_object_or_404(Product, id=productId)

        cart = member.cart

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            productInCart=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, f"'{product.productName}' 수량이 증가했습니다.")
        else:
            messages.success(request, f"'{product.productName}'이(가) 장바구니에 추가되었습니다.")

        product.quantity -= 1
        product.save()

        return redirect(request.META.get('HTTP_REFERER', 'product_list'))
    
def deleteFromCart(request):
    if request.method == "POST":
        userId = request.session.get('userId')
        productId = request.POST.get('productId')
        member = get_object_or_404(Member, no=userId)
        product = get_object_or_404(Product, id=productId)
        cart = member.cart

        cart_item = CartItem.objects.filter(cart=cart, productInCart=product).first()
        product.quantity += cart_item.quantity  # 재고 복구
        product.save()
        cart_item.delete()
        messages.success(request, f"'{product.productName}'이(가) 장바구니에서 삭제되었습니다.")
        
        return redirect('basketView')

##마이페이지
def mypageView(request):
    userId = request.session.get('userId')
    if not userId:
        messages.success(request, '로그인이 필요한 서비스입니다.')
        return redirect('login')
    user = Member.objects.get(no = userId)
    return render(request, 'mypage.html', {'user':user})

def mypageEdit(request):
    userId = request.session.get('userId')
    if not userId:
        return redirect('login')
    user = Member.objects.get(no = userId)

    if request.method == 'POST':
        user.userId = request.POST['userId']
        user.password = request.POST['password']
        user.name = request.POST['name']
        user.nickname = request.POST['nickname']
        user.gender = request.POST['gender']
        user.email = request.POST['email']
        user.phoneNumber = request.POST['phoneNumber']
        user.address = request.POST['address']
        user.save()
        messages.success(request, '회원정보가 수정되었습니다.')
        return redirect('mypageView')

    return render(request, 'mypageEdit.html', {'user':user})

def mypageWithdraw(request):
    userId = request.session.get('userId')
    if not userId:
        return redirect('login')
    user = Member.objects.get(no = userId)
    user.delete()
    request.session.flush()
    messages.success(request, '회원탈퇴가 완료되었습니다.')
    return redirect('mainPage')