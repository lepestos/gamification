from rest_framework.routers import DefaultRouter

from calculator.views.products import ProductViewSet

from calculator.views.blackbox import BlackBoxViewSet

from calculator.views.lottery import LotteryViewSet

from calculator.views.bingo import BingoViewSet


router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('black-box', BlackBoxViewSet)
router.register('lottery', LotteryViewSet)
router.register('bingo-discount', BingoViewSet)

urlpatterns = router.urls
