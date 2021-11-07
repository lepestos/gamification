<template>
  <section class="lottery-input">
      <form action="" @submit.prevent="submit()">
        <div class="lottery-input__wrapper">
          <div class="lottery-input__left">
            <div class="lottery-input__lots">
              <h2>Количество и стоимость лотов</h2>
              <input type="number" placeholder="количество" v-model="input_data.lots[0].amount" required>
              <input type="number" placeholder="стоимость" v-model="input_data.lots[0].price" required>
              <button>Добавить лот</button>
            </div>
          </div>
          <div class="lottery-input__right">
            <div class="lottery-input__write-off">
              <h2>Дополнительное списание</h2>
              <input type="number" placeholder="введите значение" v-model="input_data.write_off" required>
            </div>
            <div class="lottery-input__referal">
              <h2>Реферальная программа</h2>
              <span>Коэффициент:</span>
              <input type="number" placeholder="число" v-model="input_data.referral_coeff" required>
              <span>Скидка:</span>
              <input type="number" step="0.01" placeholder="число" v-model="input_data.discount" required>
            </div>
          </div>
        </div>
        <button type="submit" class="lottery-input__submit">Рассчитать параметры</button>
      </form>
  </section>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "lottery-input",
  data() {
    return {
      input_data: {
        lots: [{price:'', amount: ''}],
        write_off: '',
        referral_coeff: '',
        discount: '',
        ticket_price: 0,
        ticket_amount: 0,
      }
    }
  },
  methods: {
    ...mapActions(['calculateLotteryClicked']),
    submit() {
      this.calculateLotteryClicked(this.input_data)
    }
  }
}
</script>

<style scoped lang="scss">
  .lottery-input {
    text-align: center;
    &__wrapper {
      text-align: left;
      display: flex;
      > div {
        flex: 1 1 50%;
      }
      input {
        @extend %standard-input;
      }
    }
    &__lots {
      input {
        margin-top: $similar-element-margin;
        width: 100px;
        margin-right: 10px;
      }
      button {
        margin-top: $similar-element-margin;
        @extend %standard-button-inactive;
        display: block;
      }
    }

    &__write-off {
      input {
        margin-top: $similar-element-margin;
        width: 160px;
      }
    }
    &__referal {
      margin-top: $element-margin;
      input, span {
        margin-top: $similar-element-margin;
        margin-right: 10px;
      }
      input {
        width: 60px;
      }
    }
    &__submit {
      @extend %standard-button-active;
      margin-top: $section-margin;
      align-self: center;
    }
  }
</style>