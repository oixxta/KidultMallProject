from django.urls import path
from . import views


urlpatterns = [
    #메인페이지
    path('', views.mainPage, name='mainPage'),
    #회원가입
    path('register/', views.register, name='register'),
    #로그인
    path('login/', views.loginView, name='login'),
    #로그아웃
    path('logout/', views.logoutView, name='logout'),
    #신규입고
    path('new/', views.newArrivalsView, name='new'),
    #남자어른이
    path('men/', views.forKidultBoysView, name='men'),
    #여자어른이
    path('women/', views.forKidultGirlsView, name='women'),
    #제품문의(게시판)
    path('board/', views.boardList, name='boardList'),
    path('board/write/', views.boardWrite, name='boardWrite'),
    path('board/<int:boardId>', views.boardDetail, name='boardDetail'),
    path('board/<int:boardId>/update/', views.boardUpdate, name='boardUpdate'),
    #장바구니
    path('basket/', views.basketView, name='basketView'),
    path('addToCart/', views.addToCart, name='addToCart'),
    path('deleteFromCart/', views.deleteFromCart, name='deleteFromCart'),
    #마이페이지
    path('mypage/', views.mypageView, name='mypageView'),
    path('mypage/edit', views.mypageEdit, name='mypageEdit'),
    path('mypageWithdraw/', views.mypageWithdraw, name='mypageWithdraw')
]

