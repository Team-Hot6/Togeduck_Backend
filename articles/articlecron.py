from datetime import datetime, timedelta
from .models import Article
from django.db.models import Q

if __name__ == "__main__":
    category_score_dict = {1: 20, 2: 20, 3: 20, 4: 20, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20}
    
    def score(obj) -> int:
        result = 0
        result += category_score_dict[obj.category]
        result += 
        
        return 
    # 취미 카테고리별 점수

    time_now = datetime.now()

    article_obj = Article.objects.filter(
        Q(created_at__gte=datetime.now() - timedelta(days=2)) 
        &
        Q(update_at__gte=datetime.now() - timedelta(days=2)))
    
    article_temp_list = []
    