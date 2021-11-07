<template>
  <section class="black-box-table">
    <table>
      <tr>
        <th class="black-box-table__header-empty-cell">&nbsp;</th>
        <th class="black-box-table__header-empty-cell" colspan="2" rowspan="2">Название</th>
        <th colspan="3" class="black-box-table__header-first-row">Цены лотов</th>
        <th rowspan="2">Лояльн.</th>
        <th rowspan="2">Рент.</th>
        <th colspan="3" class="black-box-table__header-first-row">Количества лотов</th>
        <th rowspan="2"><div>Цена</div> <div>BlackBox</div></th>
      </tr>
      <tr>
        <th class="black-box-table__header-empty-cell">&nbsp;</th>
        <th>Дешёвый</th>
        <th>Средний</th>
        <th>Дорогой</th>
        <th>Дешёвый</th>
        <th>Средний</th>
        <th>Дорогой</th>
      </tr>
      <tr v-if="this.saved_boxes().length !== 0" v-for="box in this.saved_boxes()">
        <td><img src="@/assets/img/trash.png" alt="" @click="this.deleteBlackBox(box.id)"></td>
        <td colspan="2">{{box.truncated_name}}</td>
        <td><input type="number" v-model="box.lot_cost.cheap" readonly></td>
        <td><input type="number" v-model="box.lot_cost.middle" readonly></td>
        <td><input type="number" v-model="box.lot_cost.costly" readonly></td>
        <td><input type="number" v-model="box.loyalty" readonly></td>
        <td><input type="number" v-model="box.rentability" readonly></td>
        <td><input type="number" v-model="box.lot_amount.cheap" readonly></td>
        <td><input type="number" v-model="box.lot_amount.middle" readonly></td>
        <td><input type="number" v-model="box.lot_amount.costly" readonly></td>
        <td><input type="number" v-model="box.price" readonly></td>
      </tr>
      <tr v-else>
        <td colspan="11">К сожалению, сохранённые Black Box не найдены, создайте новый или повторите попытку позже</td>
      </tr>
    </table>
    <div class="black-box-table__buttons">
      <button>Факт</button>
      <button>Ретро</button>
    </div>
  </section>
</template>

<script>
import {mapGetters} from "vuex";
import {mapActions} from "vuex";

export default {
  name: "black-box-table",
  methods: {
    ...mapGetters(['saved_boxes']),
    ...mapActions(['loadBlackBoxes', 'deleteBlackBox'])
  },
  beforeMount() {
    this.loadBlackBoxes()
  }
}
</script>

<style scoped lang="scss">
.black-box-table {
  table{
    border-collapse: collapse;
    width: 90%;
    margin: 0 auto;
    text-align: center;
    th{
      background-color: #fff;
      font-weight: 400;
      line-height: 24px;
      &:not(.black-box-table__header-first-row) {
        padding: $similar-element-margin / 2;
      }
      &:not(.black-box-table__header-empty-cell) {
        border-left: 1px solid $border-grey;
        border-right: 1px solid $border-grey;
      }
    }
    td {
      padding: $similar-element-margin;
    }
    input {
      @extend %standard-input;
      width: 75px;
    }
    img {
      &:hover {
        cursor: pointer;
      }
    }
  }
  &__header-first-row {
    padding-top: $similar-element-margin;
  }
  &__buttons {
    text-align: center;
    margin-top: $section-margin;
    button {
      @extend %standard-button-active;
      margin: 0 20px;
    }
  }
}
</style>