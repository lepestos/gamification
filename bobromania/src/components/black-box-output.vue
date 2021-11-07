<template>
  <section class="black-box-output">
    <div class="black-box-output__lot-info lot-info">
      <span class="lot-info__cheap">Дешёвый лот</span>
      <span class="lot-info__middle">Средний лот</span>
      <span class="lot-info__costly">Дорогой лот</span>
      <span class="lot-info__amount">Количество</span>
      <input type="text" class="lot-info__amount-cheap" v-model="this.output_data().amounts.cheap" readonly>
      <input type="text" class="lot-info__amount-middle" v-model="this.output_data().amounts.middle" readonly>
      <input type="text" class="lot-info__amount-costly" v-model="this.output_data().amounts.costly" readonly>
      <span class="lot-info__percent">Вероятность выпадения</span>
      <input type="text" class="lot-info__percent-cheap" v-model="this.output_data().percents.cheap" readonly>
      <input type="text" class="lot-info__percent-middle" v-model="this.output_data().percents.middle" readonly>
      <input type="text" class="lot-info__percent-costly" v-model="this.output_data().percents.costly" readonly>
    </div>
    <div class="black-box-output__black-box-cost black-box-cost">
      <h2>Рассчитанная стоимость Black Box</h2>
        <input type="number" :value="this.output_data().black_box_cost.cur" readonly><span>бобров</span>
        <input type="number" :value="this.output_data().black_box_cost.cur * this.course().bobr_to_rub" readonly><span>рублей</span>
    </div>
  </section>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "black-box-output.vue",
  methods: mapGetters(['output_data', 'course'])
}
</script>

<style scoped lang="scss">

.black-box-output {
  display: flex;
  > div {
    flex: 1 1 50%;
  }
}

.lot-info {
  display: grid;
  grid-template-columns: repeat(4, 100px);
  grid-gap: $similar-element-margin;
  grid-auto-rows: $input-height;
  span:not(.lot-info__percent) {
    line-height: $input-height;
  }
  input {
    @extend %standard-input;
  }
  &__cheap {
    grid-column: 2;
    grid-row: 1;
  }
  &__middle {
    grid-column: 3;
    grid-row: 1;
  }
  &__costly {
    grid-column: 4;
    grid-row: 1;
  }
  &__amount {
    grid-column: 1;
    grid-row: 2;
  }
  &__amount-cheap {
    grid-column: 2;
    grid-row: 2;
  }
  &__amount-middle {
    grid-column: 3;
    grid-row: 2;
  }
  &__amount-costly {
    grid-column: 4;
    grid-row: 2;
  }
  &__percent {
    grid-column: 1;
    grid-row: 3;
  }
  &__percent-cheap {
    grid-column: 2;
    grid-row: 3;
  }
  &__percent-middle {
    grid-column: 3;
    grid-row: 3;
  }
  &__percent-costly {
    grid-column: 4;
    grid-row: 3;
  }
}

.black-box-cost {
  display: grid;
  grid-template-columns: 150px 100px;
  grid-gap: $similar-element-margin;
  grid-auto-rows: $input-height;
  line-height: $input-height;
  input {
    @extend %standard-input;
  }
  h2 {
    grid-column: 1/3;
    grid-row: 1;
  }
}

</style>