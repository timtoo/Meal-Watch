from django.db import models


class EatenManager(models.Manager):
    def eaten_count(self, meal=None):
        "Count of how many times each meal has been eaten"
        result = self.model.objects.values('meal').order_by().annotate(models.Count('meal'))
        if meal:
            result = result.filter(meal = hasattr(meal, 'id') and meal.id or meal)
        return result

    def eaten_with_count(self, ownerid):
        return self.model.objects.raw("""
                select dinner_eaten.*,
                    dinner_meal.name AS meal__name,
                    dinner_meal.common AS meal__common,
                    dinner_foodtype.color AS meal__foodtype__color,
                    dinner_foodtype.name AS meal__foodtype__name,
                    meal_count
                from dinner_eaten
                join dinner_meal ON (dinner_eaten.meal_id=dinner_meal.id)
                join dinner_foodtype ON (dinner_meal.foodtype_id = dinner_foodtype.id)
                JOIN (
                  SELECT meal_id, count(meal_id) AS meal_count
                  from dinner_eaten
                  group by meal_id
                ) AS mc ON (dinner_eaten.meal_id=mc.meal_id)
                WHERE dinner_meal.owner_id = %d
                order by dinner_eaten.date DESC, dinner_eaten.id DESC
                """ % ownerid)

