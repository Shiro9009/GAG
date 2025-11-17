from django.shortcuts import render, get_object_or_404
from .models import Streams, Users, Subscriptions, StreamCategory

def page1(request):
    """Главная страница со списком активных стримов"""
    try:
        current_streams = Streams.get_current_streams()
        
        if not current_streams.exists():
            if not Users.objects.exists():
                test_user = Users.objects.create(
                    user_name="Тестовый пользователь",
                    email="test@example.com",
                    nickname="TestStreamer",
                    roles="Обычный пользователь"
                )
            else:
                test_user = Users.objects.first()
            
            if not StreamCategory.objects.exists():
                category = StreamCategory.objects.create(
                    name="JUST CHATTING",
                    description="Общение с аудиторией"
                )
            else:
                category = StreamCategory.objects.first()
            
            Streams.objects.create(
                name="Добро пожаловать на Wstream!",
                id_users=test_user,
                category=category,
                status="Транслируется",
                description="Это тестовый стрим для демонстрации работы платформы"
            )
            current_streams = Streams.get_current_streams()
        
    except Exception as e:
        current_streams = Streams.objects.none()
        print(f"Error in page1: {e}")
    
    context = {
        'streams': current_streams,
    }
    return render(request, 'base.html', context)

def page2(request):
    """Страница профиля текущего пользователя"""
    try:
        user_profile = Users.objects.first()
        if not user_profile:
            user_profile = Users.objects.create(
                user_name="Тестовый пользователь",
                email="test@example.com",
                nickname="TestUser",
                roles="Обычный пользователь",
                about="Это тестовый профиль для демонстрации"
            )
        
        subscriptions = Subscriptions.objects.filter(id_users_from=user_profile)[:6]
        
        archive_streams = Streams.objects.filter(id_users=user_profile, status="Завершился")[:4]
        
    except Exception as e:
        user_profile = None
        subscriptions = []
        archive_streams = []
        print(f"Error in page2: {e}")
    
    context = {
        'user_profile': user_profile,
        'subscriptions': subscriptions,
        'archive_streams': archive_streams,
    }
    return render(request, 'page-2.html', context)

def page3(request, stream_id=None):
    """Страница просмотра стрима"""
    try:
        if stream_id:
            stream = get_object_or_404(Streams, id=stream_id)
        else:
            stream = Streams.get_current_stream()
            if not stream:
                stream = Streams.objects.filter(status="Завершился").order_by('-start_time').first()
                if not stream:
                    user_profile = Users.objects.first()
                    if not user_profile:
                        user_profile = Users.objects.create(
                            user_name="Тестовый стример",
                            email="streamer@example.com",
                            nickname="TestStreamer",
                            roles="Обычный пользователь"
                        )
                    
                    if not StreamCategory.objects.exists():
                        category = StreamCategory.objects.create(
                            name="JUST CHATTING",
                            description="Общение с аудиторией"
                        )
                    else:
                        category = StreamCategory.objects.first()
                    
                    stream = Streams.objects.create(
                        name="Пример стрима",
                        id_users=user_profile,
                        category=category,
                        status="Завершился",
                        description="Это пример завершенного стрима"
                    )
        
    except Exception as e:
        stream = None
        print(f"Error in page3: {e}")
    
    context = {
        'stream': stream,
    }
    return render(request, 'page-3.html', context)

def page4(request, user_id=None):
    """Страница профиля другого пользователя"""
    try:
        if user_id:
            user_profile = get_object_or_404(Users, id=user_id)
        else:
            all_users = Users.objects.all()
            if all_users.count() > 1:
                user_profile = all_users[1]
            else:
                user_profile = Users.objects.create(
                    user_name="Другой пользователь",
                    email="other@example.com",
                    nickname="OtherUser",
                    roles="Обычный пользователь",
                    about="Это профиль другого пользователя для демонстрации"
                )
        
        current_stream = Streams.objects.filter(id_users=user_profile, status="Транслируется").first()

        archive_streams = Streams.objects.filter(id_users=user_profile, status="Завершился")[:3]
        
        subscriber_count = Subscriptions.objects.filter(id_users_for=user_profile).count()
        
    except Exception as e:
        user_profile = None
        current_stream = None
        archive_streams = []
        subscriber_count = 0
        print(f"Error in page4: {e}")
    
    context = {
        'user_profile': user_profile,
        'current_stream': current_stream,
        'archive_streams': archive_streams,
        'subscriber_count': subscriber_count,
    }
    return render(request, 'page-4.html', context)

def page5(request):
    """Страница категорий"""
    try:
        categories = StreamCategory.objects.all()
        
        for category in categories:
            category.update_statistics()
        
    except Exception as e:
        categories = []
        print(f"Error in page5: {e}")
    
    context = {
        'categories': categories,
    }
    return render(request, 'page-5.html', context)

def page6(request):
    return render(request, 'page6.html')

def page7(request):
    return render(request, 'page7.html')