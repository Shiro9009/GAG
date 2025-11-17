from django.shortcuts import render, get_object_or_404
from .models import Streams, Users, Subscriptions, StreamCategory

def page1(request):
    """Главная страница со списком активных стримов"""
    try:
        current_streams = Streams.get_current_streams()
        
        # Создаем тестовые данные если база пустая
        if not current_streams.exists():
            # Создаем тестового пользователя если нет пользователей
            if not Users.objects.exists():
                test_user = Users.objects.create(
                    user_name="Тестовый пользователь",
                    email="test@example.com",
                    nickname="TestStreamer",
                    roles="Обычный пользователь"
                )
            else:
                test_user = Users.objects.first()
            
            # Создаем тестовую категорию если нет категорий
            if not StreamCategory.objects.exists():
                category = StreamCategory.objects.create(
                    name="JUST CHATTING",
                    description="Общение с аудиторией"
                )
            else:
                category = StreamCategory.objects.first()
            
            # Создаем тестовый стрим
            Streams.objects.create(
                name="Добро пожаловать на Wstream!",
                id_users=test_user,
                category=category,
                status="Транслируется",
                description="Это тестовый стрим для демонстрации работы платформы"
            )
            current_streams = Streams.get_current_streams()
        
    except Exception as e:
        # В случае ошибки возвращаем пустой queryset
        current_streams = Streams.objects.none()
        print(f"Error in page1: {e}")
    
    context = {
        'streams': current_streams,
    }
    return render(request, 'base.html', context)

def page2(request):
    """Страница профиля текущего пользователя"""
    try:
        # Для демонстрации берем первого пользователя
        user_profile = Users.objects.first()
        if not user_profile:
            # Создаем тестового пользователя если нет пользователей
            user_profile = Users.objects.create(
                user_name="Тестовый пользователь",
                email="test@example.com",
                nickname="TestUser",
                roles="Обычный пользователь",
                about="Это тестовый профиль для демонстрации"
            )
        
        # Получаем подписки пользователя
        subscriptions = Subscriptions.objects.filter(id_users_from=user_profile)[:6]
        
        # Получаем архив стримов пользователя
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
                # Если нет активных стримов, берем последний завершенный
                stream = Streams.objects.filter(status="Завершился").order_by('-start_time').first()
                if not stream:
                    # Создаем тестовый стрим если нет вообще стримов
                    user_profile = Users.objects.first()
                    if not user_profile:
                        user_profile = Users.objects.create(
                            user_name="Тестовый стример",
                            email="streamer@example.com",
                            nickname="TestStreamer",
                            roles="Обычный пользователь"
                        )
                    
                    # Создаем категорию если нет
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
            # Для демонстрации берем пользователя, который не является текущим
            all_users = Users.objects.all()
            if all_users.count() > 1:
                # Берем второго пользователя
                user_profile = all_users[1]
            else:
                # Если только один пользователь, создаем второго
                user_profile = Users.objects.create(
                    user_name="Другой пользователь",
                    email="other@example.com",
                    nickname="OtherUser",
                    roles="Обычный пользователь",
                    about="Это профиль другого пользователя для демонстрации"
                )
        
        # Получаем активные стримы пользователя
        current_stream = Streams.objects.filter(id_users=user_profile, status="Транслируется").first()
        
        # Получаем архив стримов пользователя
        archive_streams = Streams.objects.filter(id_users=user_profile, status="Завершился")[:3]
        
        # Получаем количество подписчиков
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
        # Получаем все категории с актуальной статистикой
        categories = StreamCategory.objects.all()
        
        # Обновляем статистику для каждой категории
        for category in categories:
            category.update_statistics()
        
    except Exception as e:
        categories = []
        print(f"Error in page5: {e}")
    
    context = {
        'categories': categories,
    }
    return render(request, 'page-5.html', context)