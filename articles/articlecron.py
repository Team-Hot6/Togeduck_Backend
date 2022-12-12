from datetime import datetime, timedelta
from .models import Article
from django.db.models import Q

if __name__ == "__main__":
    category_score_dict = {1: 20, 2: 20, 3: 20, 4: 20, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20}
    like_multiple = 1.2
    view_multiple = 1
    time_multiple = 0.2
    current_time = datetime.now()
    
    # 취미 카테고리별 점수
    def score(obj) -> int:
        result = 1
        result *= category_score_dict[obj.category]
        result *= obj.like.count() * like_multiple
        result *= obj.views * view_multiple

        hour_diff_sec = (current_time - obj.created_at).total_seconds() / 3600
        
        # (10 - 시간배수 * 시간차이(hours)) 시간당 0.2 배수 차이
        # ex) 1시간 -> 9.8 , 2시간 -> 9.6
        return result * (10 - (time_multiple * hour_diff_sec))

    time_now = datetime.now()

    article_obj = Article.objects.filter(
        Q(created_at__gte=datetime.now() - timedelta(days=2)) 
        &
        Q(update_at__gte=datetime.now() - timedelta(days=2)))
    
    article_score_id_list = [(x, score(x)) for x in article_obj]

    article_score_id_list.sort(key=lambda x:x[1], reverse=True)

    result_id = [article_score_id_list[x][0] for x in range(len(article_score_id_list))]

    print(result_id)