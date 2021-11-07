<template>
  <section class="lottery-output">
    <div class="lottery-output__wrapper">
      <div class="lottery-output__left">
        <div class="lottery-output__parameters">
          <h2>Параметры лотереи</h2>
          <div>
            <span>Количество билетов:</span>
            <input type="number" v-model="this.lottery_output_data().ticket_amount" readonly>
          </div>
          <div>
            <span>Себестоимость лотереи:</span>
            <input type="number" v-model="this.lottery_output_data().total_cost" readonly>
          </div>
        </div>
        <div class="lottery-output__profit">
          <h2>Выгода от лотереи</h2>
          <span>От:</span>
          <input type="number" v-model="this.lottery_output_data().min_profit" readonly>
          <span>До:</span>
          <input type="number" v-model="this.lottery_output_data().write_off" readonly>
        </div>
      </div>
      <div class="lottery-output__right">
        <div class="lottery-output__ticket-cost">
          <h2>Стоимость билета</h2>
          <div><input type="number" v-model="this.lottery_output_data().ticket_price" readonly><span>бобров</span></div>
          <div><input type="number" :value="this.lottery_output_data().ticket_price * this.course().bobr_to_rub" readonly><span>рублей</span></div>
        </div>
        <div class="lottery-output__rentability">
          <h2>Рентабильность</h2>
          <span>От:</span>
          <input type="number" v-model="this.lottery_output_data().min_rentability" readonly>
          <span>До:</span>
          <input type="number" v-model="this.lottery_output_data().max_rentability" readonly>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "lottery-output",
  methods: {
    ...mapGetters(['lottery_output_data', 'course'])
  }
}
</script>

<style scoped lang="scss">
.lottery-output {
  &__wrapper {
    display: flex;
    > div {
      flex: 1 1 50%;
    }
    input {
      @extend %standard-input;
    }
  }
  &__parameters, &__ticket-cost {
    div {
      margin-top: $similar-element-margin;
    }
    input {
      width: 160px;
      margin: 0 10px;
    }
  }
  &__profit, &__rentability {
    margin-top: $element-margin;
    input, span {
      margin-top: $similar-element-margin;
      margin-right: 10px;
    }
    input {
      width: 60px;
    }
  }
}
</style>