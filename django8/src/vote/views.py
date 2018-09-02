from django.shortcuts import render, get_object_or_404
from .models import Question
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#HttpResponseRedirect : 클라이언트에게 HTML파일을 전달하는것이 아닌
#URL 주소를 전달 -> 웹 클라이언트는 받은 URL주소로 웹서버에 재요청
#reverse 함수 : URL의 별칭(name)을 이용해 URL 주소를 찾는 함수
#(Template 엔진의 url함수와 동일 기능 제공)

#함수 or 클래스 형태로 뷰 구현
#함수형태로 구현시 첫번째 매개변수로 request를 받아야함
#request : 웹 클라이언트의 요청에 대한 정보를 알고있는 매개변수
'''
def index(request):
    #render(request, html 파일경로, 템플릿에서 사용할 데이터 - 사전형)
    return render(request, 'vote/index.html',{'hello':'django개발'})
'''
#질문 목록 보기
def index(request):
    #Question.objects.all() : 데이터베이스에 저장된 모든 Question 객체를
    #                         리스트형태로 가져옴
    list = Question.objects.all()
    print(list)
    
    return render(request, 'vote/index.html', {'question_list':list})

#설문지 출력 및 투표 선택
def detail(request, question_id):
    #매개변수에 작성한 조건에 따라 모델클래스의 객체 1개를 추출
    #매개변수이름은 모델클래스에서 작성한 변수를 사용가능
    #내부적으로 id변수(고유 키)가 추가됨
    obj = Question.objects.get(id = question_id)
    return render(request, 'vote/detail.html', {'question':obj})

#투표 처리
def vote(request):
    #request.method : 클라이언트의 요청이 GET방식인지 POST방식인지 지정한 변수
    #문자열 비교시 "GET"/"POST" 문자열과 같은지 비교(전부 대문자로 작성)
    if request.method =="POST": #클라이언트 요청이 POST인가?
        #request.POST : POST 요청으로 온 데이터들
        #request.POST.get(name 값) : POST방식으로 들어온 데이터 중
        #name과 같은 데이터를 추출
        #get함수가 반환하는 값은 전부 문자열
        id = request.POST.get('choice')
        #pk : Choice객체의 id변수와 동일
        obj = get_object_or_404
        obj.votes += 1 # obj.votes = obj.votes + 1
        obj.save() #객체의 변경 사항을 데이터베이스에 저장
        #obj.question : Choice 객체가 연결된 Question 객체를 뜻함
        #obj.question.question_text : Choice 객체가 연결된 Question 객체에
        #저장된 question_text 변수를 읽기
        return HttpResponseRedirect(reverse('result', args= (obj.question.id,) ))
    
def result(request, question_id):
    #obj 벼눗 : Question 객체
    obj = get_object_or_404(Question, pk = question_id)
    return render(request, 'vote/result.html', {'obj' : obj})

from .forms import *
import datetime #시간에 관한 모듈

@login_required
def registerQ(request):
    #하난의 뷰 함수는 사용자가 GET/POST 요청할 때를 구분지어서 작업
    if request.method == "GET":
    #QuestionForm 객체 생성. 사용자로부터 입력받을 변수값을 HTML 
    #문서에서 처리할수 있도록 HTML코드로 변환 가능
    #객체를 생성한 경우, <input>태그에 값이 비어있는 상태로 사용자에게 전달
        form = QuestionForm()
        return render(request, 'vote/registerQ.html',{'form':form})
    elif request.method == "POST":
        #폼 객체 생성시 사용자가 입력한 데티어를 각 폼 변수에 대입
        form = QuestionForm(request.POST)
        
        if form.is_valid(): #해당 폼에 입력값들이 에러가 없는지 확인
            #form.save() #해당 폼에 입력값들로 모델클래스 객체를 생성 후 데이터 베이스에 저장
            obj = form.save(commit=False)#해당 폼에 입력값들로 모델클래스 객체를 생성
            obj.pub_date = datetime.datetime.now()#현재시간을 대입
            obj.author = request.user #글쓴이 등록
            obj.save()#Question 객체를 데이터베이스에 저장
            return HttpResponseRedirect( reverse( 'detail', args=(obj.id,) ) )

@login_required
def registerC(request):
        if request.method =="GET":#vote/registerC.html�쓣 �궗�슜
        #GET諛⑹떇 泥섎━ 肄붾뱶 留뚮뱾湲� 1)�뤌媛앹껜 �깮�꽦 2)render�븿�닔 諛섑솚

            form = ChoiceForm()
            print( form.as_table() )
            #request.GET
            return render(request, 'vote/registerC.html', {'form':form})
        elif request.method =="POST":
            #1-3-2-1)POST - 사용자 입력
            form = ChoiceForm(request.POST)
            #2)�쑀�슚�븳 媛믪씠 �뱾�뼱�엳�뒗 �뤌�씤吏� �솗�씤
            if form.is_valid():
                #print(request.user)
                #print(form.cleaned_data['question'].author)#Question모델클래스 객체
                #print(request.POST.get('question'))
                #현재 로그인된 유저와 Question 모델클래스 객체에 저장된
                #글쓴이를 비교
                if request.user == form.cleaned_data['question'].author:
                    
                #3)紐⑤뜽�겢�옒�뒪 媛앹껜瑜� �깮�꽦 諛� �뜲�씠�꽣踰좎씠�뒪�뿉 ���옣
                    obj = form.save()
                    return HttpResponseRedirect( 
                        reverse('detail',args=(obj.question.id,) ) )
                    #4)'detail' 蹂꾩묶�쓣 媛�吏� URL 諛섑솚
                else:
                    return render(request, 'vote/register.html',{'form':form,'error':'현재 로그인된 유저의 글이 아닙니다.'})
    
@login_required
def deleteQ(request,question_id):
    #�궘�젣�븷 媛앹껜 李얘린
    #pk=id �룞�씪
    obj = get_object_or_404(Question,pk=question_id)
    obj.delete() #�빐�떦 媛앹껜瑜� �뜲�씠�꽣踰좎씠�뒪�뿉�꽌 �젣嫄�
    return HttpResponseRedirect( reverse('index') )

@login_required
def deleteC(request, choice_id):
    obj = get_object_or_404(Choice,pk=choice_id)
    question_id = obj.question.id
    obj.delete()
    return HttpResponseRedirect(reverse('detail', args=(question_id,)))

@login_required
def updateQ(request, question_id):
    obj = get_object_or_404(Question, pk = question_id)
    if request.method == "GET":
        #Question 媛앹껜�뿉 ���옣�맂 媛믪쓣 QuestionForm 媛앹껜瑜� �깮�꽦�븷 �븣 �엯�젰
        #紐⑤뜽�뤌�쓽 �깮�꽦�옄�뿉 instance 留ㅺ컻蹂��닔�뒗 �씠誘� �깮�꽦�맂 紐⑤뜽�겢�옒�뒪�쓽媛앹껜瑜�
        #�꽔�뼱�빞�븿
        form = QuestionForm(instance = obj)
        return render(request, 'vote/updateQ.html', {"form":form})
    elif request.method=="POST":
        #�씠誘� �깮�꽦�맂 Question 媛앹껜�뿉 蹂��닔媛믩뱾�쓣 �겢�씪�씠�뼵�듃媛� �옉�꽦�븳 �궡�슜�쑝濡�
        #�뜮�뼱�뵆��
        form = QuestionForm(request.POST, instance = obj)
        if form.is_valid():
            question = form.save()
            #question = form.save(commit=False)
            #question.pub_date = obj.pub_date
            #question.save()
            
            return HttpResponseRedirect(
                reverse('detail', args=(question.id,)))
            
@login_required
def updateC(request,choice_id):
#1-1)Choice객체 찾기
    obj = get_object_or_404(Choice,pk=choice_id)
    #1-2)GET/POST 구분
    if request.method == "GET":
        #1-3-1-1)GET-폼객체 생성 후 Html반환
        form = ChoiceForm(instance = obj)
        return render(request, 'vote/updateC.html',{'data':form})
    elif request.method =="POST":
        #1-3-2-1)POST - 사용자 입력 + Choice 객체를 통해 생성자 호출
        form = ChoiceForm(request.POST, instance = obj)
        #1-3-2-2)데이터가 유효한지 확인
        if form.is_valid():
            #1-3-2-3)폼객체 저장
            cho=form.save()
            #cho.question.id
            #1-3-2-4)사용자에게 detail 뷰의 URL 전송 
            return HttpResponseRedirect( 
                reverse( 'detail',args=(cho.question.id,)  ) )
        else: #사용자의 입력이 유효하지 않는 데이터인경우
            #다시 html문서를 전달하면서 특정변수에 에러문구 대입
            return render(request, 'vote/updateC.html',
                          {'data':form , 'error' :'유효하지않는 입력' })
    
        