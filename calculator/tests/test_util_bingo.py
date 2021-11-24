from math import isclose

import pytest

from calculator.utils.bingo import BingoUtil, DiscountBingoUtil,\
    BoosterBingoUtil, MiniBingoUtil, BOOSTER_VALUES
from .data.util_lottery_data import RWEB_DATA, RPS_DATA, SFL_DATA,\
    INIT_DISCOUNT_DATA, DIC_DATA, INIT_BOOSTER_DATA, RECALC_DISCOUNT_DATA


class TestBingo:
    @pytest.mark.parametrize("discounts, amounts", RWEB_DATA)
    def test_round_wo_exceeding_budget(self, discounts, amounts):
        price = 100
        budget = price * sum(a * d for a, d in zip(amounts, discounts))
        total_amount = sum(amounts)
        bingo = MiniBingoUtil(price, discounts, budget, int(sum(amounts)))
        res = bingo.round_wo_exceeding_budget(amounts)
        assert isclose(sum(res), total_amount)
        assert price * sum(a * d for a, d in zip(res, discounts)) <= budget + 1e-2
        assert max(abs(a - r) for a, r in zip(amounts, res)) < 1

    @pytest.mark.parametrize("amounts", RPS_DATA)
    def test_round_preserving_sum(self, amounts):
        res = BingoUtil.round_preserving_sum(amounts)
        assert isclose(sum(amounts), sum(res))
        assert max(abs(a - r) for a, r in zip(amounts, res)) < 1

    @pytest.mark.parametrize("inp, exp", SFL_DATA)
    def test_solve_for_single_lot(self, inp, exp):
        bingo = MiniBingoUtil(*inp)
        res = bingo.solve_amounts_normal_budget()
        assert max(abs(r - e) for r, e in zip(res, exp)) < 1e-2

    @pytest.mark.parametrize("input_data", INIT_DISCOUNT_DATA + RECALC_DISCOUNT_DATA)
    def test_discounts_initial(self, input_data):
        bingo = DiscountBingoUtil(**input_data)
        res = bingo.to_json()
        assert res['expected_budget'] >= 0
        assert all(p >= 0 for p in res['participants_per_lot'])
        assert isclose(sum(res['budget_distribution']), 1)
        assert sum(sum(row) for row in res['amounts']) <= input_data['lucky_participants']
        assert all(all(a >= 0 for a in row) for row in res['amounts'])
        un_p = input_data['unlucky_participants']
        if un_p is not None:
            if res['total_participants'] != 0:
                assert isclose(1 - un_p, res['lucky_participants'] / res['total_participants'], abs_tol=0.1)

    @pytest.mark.parametrize("inp, exp", DIC_DATA)
    def test_discounts_initial_concrete(self, inp, exp):
        bingo = DiscountBingoUtil(**inp)
        res = bingo.to_json()
        for key in ['amounts', 'participants_per_lot', 'lucky_participants']:
            assert res[key] == exp[key]

    @pytest.mark.parametrize("input_data", INIT_BOOSTER_DATA)
    def test_boosters_initial(self, input_data):
        bingo = BoosterBingoUtil(**input_data)
        res = bingo.to_json()
        assert all(all(a in BOOSTER_VALUES for a in row['booster']) for row in res['values'])
        assert all(all(a >= 0 for a in row['fix']) for row in res['values'])
        assert all(all(a >= 0 for a in row) for row in res['amounts'])
        assert sum(sum(row) for row in res['amounts']) <= input_data['participants']
