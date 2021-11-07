from rest_framework.routers import DefaultRouter

from calculator.views.products import ProductViewSet

from calculator.views.blackbox import BlackBoxViewSet

from calculator.views.lottery import LotteryViewSet


router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('black-box', BlackBoxViewSet)
router.register('lottery', LotteryViewSet)

urlpatterns = router.urls
