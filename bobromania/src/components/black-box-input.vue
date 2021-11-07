<template>
  <section class="black-box-input">
    <form action="" @submit.prevent="checkAndSubmit()">
      <div class="black-box-input__wrapper">
        <div class="black-box-input__left">
          <div class="black-box-input_lot-costs lot-costs">
            <h2>Стоимость лотов</h2>
            <div class="lot-costs__inputs">
              <datalist id="lots">
                <option v-for="lot in this.products()" :value="lot.price">{{lot.name}}</option>
              </datalist>
              <input type="number"  class="lot-costs__cheap" placeholder="Дешёвый" v-model="input_data.lot_cost.cheap" min="0" required :disabled="this.active_half() !== 'top'" list="lots">
              <input type="number" class="lot-costs__middle" placeholder="Средний" v-model="input_data.lot_cost.middle" min="0" required :disabled="this.active_half() !== 'top'" list="lots">
              <input type="number" class="lot-costs__costly" placeholder="Дорогой" v-model="input_data.lot_cost.costly" min="0" required :disabled="this.active_half() !== 'top'" list="lots">
            </div>
          </div>
        </div>
        <div class="black-box-input__right">
          <div class="black-box-input__constants constants">
            <h2>Расчётные константы</h2>
            <div class="constants__inputs">
              <span class="constants__span_two-lines">Целевая лояльность:</span>
              <input type="number" v-model="input_data.loyalty" min="0.3" max="0.9" step="0.01" required :disabled="this.active_half() !== 'top'">
              <span class="constants__span_one-line">Рентабельность:</span>
              <input type="number" v-model="input_data.rentability" min="0" max="1" step="0.01" required :disabled="this.active_half() !== 'top'">
            </div>
          </div>
          <div class="black-box-input__costly-amount costly-amount">
            <h2>Количество дорогих лотов</h2>
            <input type="number" placeholder="Введите количество" v-model="input_data.costly_amount" min="0" required :disabled="this.active_half() !== 'top'">
          </div>
        </div>
      </div>
      <button type="submit" class="black-box-input__calculate-parameters" :disabled="this.active_half() !== 'top'">Рассчитать параметры</button>
      <h2 class="black-box-input__error" v-if="error_message !== ''">{{error_message}}</h2>
    </form>
  </section>
</template>

<script>
import {mapActions} from 'vuex';
import {mapGetters} from "vuex";

export default {
  name: "black-box-input.vue",
  methods: {
    ...mapActions(['calculateParametersClicked']),
    ...mapGetters(['active_half', 'products']),
    checkAndSubmit() {
      if (this.input_data.lot_cost.cheap < this.input_data.lot_cost.middle && this.input_data.lot_cost.middle < this.input_data.lot_cost.costly) {
        this.error_message = ''
        this.calculateParametersClicked(this.input_data)
      }
      else {
        this.error_message = "Неворно заданы цены лотов. Проверьте данные и повторите попытку."
      }
    }
  },
  async beforeCreate() {
    await this.$store.dispatch('loadProducts');
  },
  data() {
    return {
      input_data: {
        lot_cost: {
          cheap: '',
          middle: '',
          costly: '',
        },
        loyalty: 0.6,
        rentability: 0.15,
        costly_amount: '',
      },
      error_message: '',
    }
  }
}
</script>

<style scoped lang="scss">
.black-box-input {
  text-align: center;
  &__wrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  &__left, &__right {
    text-align: left;
    flex: 1 1 50%;
  }
  &__choose-from-showcase {
    margin-top: $element-margin;
  }
  &__costly-amount {
    margin-top: $element-margin;
  }
  &__calculate-parameters {
    margin-top: $section-margin;
    @extend %standard-button-active;
  }
  &__error {
    margin-top: $element-margin;
    color: red
  }
}

.lot-costs {
  &__inputs {
    margin: $similar-element-margin 0 0 -11px;
    display: flex;
    input {
      flex: 1 1 auto;
      margin: 0 11px;
      max-width: 100px;
      @extend %standard-input;
    }
  }
}

.constants {
  &__inputs {
    margin: $similar-element-margin 0 0 -6px;
    display: flex;
    input, span {
      flex: 1 1 auto;
      margin: 0 6px;
      max-width: 100px;
    }
    input {
      @extend %standard-input;
    }
  }
  &__span {
    &_one-line {
      line-height: $input-height;
    }
    &_two-lines {
      line-height: $input-height / 2;
    }
  }
}

.costly-amount {
  input {
    margin-top: $similar-element-margin;
    @extend %standard-input;
  }
}

</style>