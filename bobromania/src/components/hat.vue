<template>
  <section class="hat">
    <h1 class="hat__headline">Калькулятор игровых механик</h1>
    <div class="courses">
      <h2>Курс перевода валют</h2>
      <div class="courses__rub-to-bobr">
        <span>1 рубль =</span> <input type="number" placeholder="введите значение" name="rub-to-bobr" v-model="courseInput.rub_to_bobr" @input="rtbchanged()"> <span>бобров</span>
      </div>
      <div class="courses__bobr-to-rub">
        <span>1 бобр =</span> <input type="number" placeholder="введите значение" name="rub-to-bobr" v-model="courseInput.bobr_to_rub" @input="btrchanged()"> <span>рублей</span>
      </div>
    </div>
    <ul class="hat__navigation">
      <li class="hat__link" :class="{hat__link_active: active_page === 'BlackBox'}" @click="active_page = 'BlackBox'"><router-link to="/BlackBox">Black Box</router-link></li>
      <li class="hat__link" :class="{hat__link_active: active_page === 'Lottery'}" @click="active_page = 'Lottery'"><router-link to="/Lottery">Лотерея</router-link></li>
      <li class="hat__link" :class="{hat__link_active: active_page === 'Bingo'}" @click="active_page = 'Bingo'"><router-link to="/Bingo">Бинго</router-link></li>
    </ul>
  </section>
</template>

<script>
import {mapGetters} from "vuex";
import {mapActions} from "vuex";

export default {
  name: "hat.vue",
  data() {
    return {
      courseInput: {
        rub_to_bobr: 1,
        bobr_to_rub: 1
      },
      active_page: ''
    }
  },
  methods: {
    ...mapGetters(['course']),
    ...mapActions(['rub_to_bobr_changed', 'bobr_to_rub_changed']),
    rtbchanged() {
      this.rub_to_bobr_changed(this.courseInput.rub_to_bobr)
      this.courseInput.bobr_to_rub = this.course().bobr_to_rub
    },
    btrchanged() {
      this.bobr_to_rub_changed(this.courseInput.bobr_to_rub)
      this.courseInput.rub_to_bobr = this.course().rub_to_bobr
    }
  },
  beforeMount() {
    this.courseInput = this.course()
  },
}
</script>

<style scoped lang="scss">
.hat {
  &__headline {
    font-size: 28px;
    font-weight: 400;
    text-align: center;
  }
  &__courses {
    margin-top: $element-margin;
  }
  &__navigation {
    margin-top: $element-margin;
    list-style-type: none;
    display: flex;
    width: 50%;
    text-align: center;
  }
  &__link {
    flex: 1 1 auto;
    a {
      font-size: 24px;
      color: $main-grey;
    }
    a:hover {
      color: $main-green;
    }
  }
  &__link_active {
    border-bottom: 3px solid $main-green;
    a:hover {
      cursor: default;
      color: $main-grey;

    }
  }
}

.courses {
  h2, span {
    font-weight: 400;
    font-size: 15px;
  }
  span {
    display: inline-block;
    min-width: 65px;
  }
  &__rub-to-bobr, &__bobr-to-rub {
    margin-top: $similar-element-margin;
  }
  input {
    margin: 0 $similar-element-margin;
    width: 135px;
    @extend %standard-input;
  }
}

</style>