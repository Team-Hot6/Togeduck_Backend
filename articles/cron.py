from datetime import datetime, timedelta
from .models import Article
from workshops.models import Workshop
from django.db.models import Q
import os, json
from pathlib import Path

# if __name__ == "__main__":
def get_score():
    # article 점수 배수
    article_category_score_dict = {1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100}
    article_like_multiple = 1.2
    article_view_multiple = 1
    article_time_multiple = 0.1
    current_time = datetime.now()
    
    # workshop 점수 배수
    workshop_category_score_dict = {1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100}
    workshop_like_multiple = 1.4
    workshop_view_multiple = 1
    workshop_time_multiple = 0.1

    # article 취미 카테고리별 점수
    def article_score(obj) -> int:
        result = 1
        result += article_category_score_dict[obj.category.id]
        result += obj.like.count() * article_like_multiple
        result += obj.views * article_view_multiple

        hour_diff_sec = (current_time - obj.created_at).total_seconds() / 3600
        
        # (10 - 시간배수 * 시간차이(hours)) 시간당 0.1 배수 차이
        # ex) 1시간 -> 9.9 , 2시간 -> 9.8
        # print(result)
        # print(hour_diff_sec)
        return result * (10 - (article_time_multiple * hour_diff_sec))
    
    def workshop_score(obj) -> int:
        result = 1
        result += workshop_category_score_dict[obj.category.id]
        result += obj.likes.count() * workshop_like_multiple
        result += obj.views * workshop_view_multiple

        hour_diff_sec = (current_time - obj.created_at).total_seconds() / 3600
        
        # (10 - 시간배수 * 시간차이(hours)) 시간당 0.1 배수 차이
        # ex) 1시간 -> 9.9 , 2시간 -> 9.8
        # print(result)
        # print(hour_diff_sec)
        return result * (10 - (workshop_time_multiple * hour_diff_sec))
    result = {}
    
    # Article 로직
    article_obj = Article.objects.filter(Q(created_at__gte=(datetime.now() - timedelta(days=2))))
    article_score_id_list = [(x, article_score(x)) for x in article_obj]
    article_score_id_list.sort(key=lambda x:x[1], reverse=True)

    article_result_id = [article_score_id_list[x][0].id for x in range(len(article_score_id_list[0:10]))]
    result['result_article_lank'] = article_result_id
    
    # Workshop 로직
    workshop_obj = Workshop.objects.filter(Q(created_at__gte=(datetime.now() - timedelta(days=2))))
    workshop_score_id_list = [(x, workshop_score(x)) for x in workshop_obj]
    workshop_score_id_list.sort(key=lambda x:x[1], reverse=True)

    workshop_result_id = [workshop_score_id_list[x][0].id for x in range(len(workshop_score_id_list[0:7]))]
    result['result_workshop_lank'] = workshop_result_id

    # Lank.json 에 쓰기
    BASE_DIR = Path(__file__).resolve().parent.parent
    lank_file_path = os.path.join(BASE_DIR, 'Lank.json')

    with open(lank_file_path, 'w') as f:
        json.dump(result, f, indent=4)