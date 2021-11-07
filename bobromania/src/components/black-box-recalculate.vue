<template>
  <section class="black-box-recalculate">
    <h2 class="black-box-recalculate__error" v-if="recalc_data.message !== ''">{{recalc_data.message}}</h2>
    <form id="recalc" action="" @submit.prevent="submit()" @reset.prevent="reset()">
      <div class="black-box-recalculate__change-loyalty change-loyalty">
        <h2>Изменить целевую лояльность</h2>
        <input type="number" min="0.3" max="0.9" step="0.01" v-model="recalc_data.loyalty">
        <input type="range" class="styled-slider slider-progress" min="0.3" max="0.9" step="0.01" v-model="recalc_data.loyalty">
      </div>
      <div class="black-box-recalculate__change-rentability change-rentability">
        <h2>Изменить целевую рентабельность</h2>
        <input type="number" min="0" max="1" step="0.01" v-model="recalc_data.rentability">
        <input type="range" class="styled-slider slider-progress" min="0" max="1" step="0.01" v-model="recalc_data.rentability">
      </div>
      <div class="black-box-recalculate__change-cost change-cost">
        <h2>Изменить стоимость Black Box</h2>
        <input type="number"
               step="10"
               v-bind:min="recalc_data.black_box_cost.min"
               v-bind:max="recalc_data.black_box_cost.max"
               v-model="recalc_data.black_box_cost.cur">
        <input type="range"
               class="styled-slider slider-progress"
               name="price"
               step="10"
               v-bind:min="recalc_data.black_box_cost.min"
               v-bind:max="recalc_data.black_box_cost.max"
               v-model="recalc_data.black_box_cost.cur">
      </div>
      <div class="black-box-recalculate__buttons buttons">
        <button type="submit">Перерасчёт параметров</button>
        <button type="reset">Вернуться к первому шагу</button>
      </div>
    </form>
    <form action="" id="save" @submit.prevent="save()">
      <input type="text" placeholder="Название" v-model="name" size="10">
      <button type="submit">Сохранить расчёт</button>
    </form>
  </section>
</template>

<script>
import {mapGetters} from "vuex";
import {mapActions} from "vuex";

export default {
  name: "black-box-recalculate",
  data() {
    return {
      recalc_data: {
        loyalty: 0,
        rentability: 0,
        black_box_cost: {
          min: 0,
          cur: 0,
          max: 0
        },
        message: '',
      },
      name: '',
    }
  },
  methods: {
    ...mapGetters(['active_half', 'recalculate_data']),
    ...mapActions(['recalculateParametersClicked', 'blackBoxReset', 'saveBlackBox', 'loadBlackBoxes']),
    async submit() {
      await this.recalculateParametersClicked(this.recalc_data)
    },
    reset() {
      this.blackBoxReset()
    },
    save() {
      this.saveBlackBox(this.name)
      this.loadBlackBoxes()
    }
  },
  beforeMount() {
    this.recalc_data = this.recalculate_data()
  },
  mounted() {
    this.recalc_data.black_box_cost.cur++
    this.recalc_data.black_box_cost.cur--
  },
  updated() {
    for (let e of document.querySelectorAll('input[type="range"].slider-progress')) {
      e.style.setProperty('--value', e.name === 'price' ? this.recalc_data.black_box_cost.cur : e.value);
      e.style.setProperty('--min', e.name === 'price' ? this.recalc_data.black_box_cost.min : e.min);
      e.style.setProperty('--max', e.name === 'price' ? this.recalc_data.black_box_cost.max : e.max);
      e.addEventListener('input', () => e.style.setProperty('--value', e.value));
    }
  }
}
</script>

<style scoped lang="scss">
.black-box-recalculate {
  text-align: center;
  &__error {
    color: red
  }
  #recalc {
    display: flex;
    flex-flow: row wrap;
    div:not(.buttons) {
      flex: 1 1 50%;
      display: grid;
      margin-top: $element-margin;
      grid-template-columns: 100px 300px+$similar-element-margin*2;
      grid-gap: $similar-element-margin;
      grid-auto-rows: $input-height;
      line-height: $input-height;
      h2 {
        grid-column: 1/3;
      }
      input[type=number] {
        @extend %standard-input;
      }
    }
    .buttons {
      flex: 1 1 50%;
      display: flex;
      justify-content: space-around;
      align-items: center;
      button {
        @extend %standard-button-inactive;
      }
    }
  }
  #save {
    margin-top: $section-margin;
    input {
      @extend %standard-input;
      width: 140px;
      margin-right: 20px;
    }
    button {
      @extend %standard-button-active;
    }
  }
}


/*generated with Input range slider CSS style generator (version 20210711)
https://toughengineer.github.io/demo/slider-styler*/
input[type=range].styled-slider {
  -webkit-appearance: none;
  background-color: $background-grey;
}

/*progress support*/
input[type=range].styled-slider.slider-progress {
  --range: calc(var(--max) - var(--min));
  --ratio: calc((var(--value) - var(--min)) / var(--range));
  --sx: calc(0.5 * 17px + var(--ratio) * (100% - 17px));
}

input[type=range].styled-slider:focus {
  outline: none;
}

/*webkit*/
input[type=range].styled-slider::-webkit-slider-thumb {
  width: 17px;
  height: 17px;
  border-radius: 17px;
  background: #FFFFFF;
  border: 1px solid #7B7B7B;
  box-shadow: none;
  margin-top: calc(max((10px - 1px - 1px) * 0.5,0px) - max(17px * 0.5,1px));
  -webkit-appearance: none;
}

input[type=range].styled-slider::-webkit-slider-runnable-track {
  height: 10px;
  border-radius: 8px;
  background: #FFF;
  border: 1px solid #b2b2b2;
  box-shadow: none;
}
input[type=range].styled-slider:hover::-webkit-slider-runnable-track {
  background: #F3F3F3;
}

input[type=range].styled-slider.slider-progress::-webkit-slider-runnable-track {
  background: linear-gradient(#00A460,#00A460) 0/var(--sx) 100% no-repeat, #FFF;
}

input[type=range].styled-slider.slider-progress:hover::-webkit-slider-runnable-track {
  background: linear-gradient(#00A460,#00A460) 0/var(--sx) 100% no-repeat, #F3F3F3;
}

/*mozilla*/
input[type=range].styled-slider::-moz-range-thumb {
  width: max(calc(17px - 1px - 1px),0px);
  height: max(calc(17px - 1px - 1px),0px);
  border-radius: 17px;
  background: #FFFFFF;
  border: 1px solid #7B7B7B;
  box-shadow: none;
}

input[type=range].styled-slider::-moz-range-track {
  height: max(calc(10px - 1px - 1px),0px);
  border-radius: 8px;
  background: #FFF;
  border: 1px solid #b2b2b2;
  box-shadow: none;
}

input[type=range].styled-slider:hover::-moz-range-track {
  background: #F3F3F3;
}

input[type=range].styled-slider.slider-progress::-moz-range-track {
  background: linear-gradient(#00A460,#00A460) 0/var(--sx) 100% no-repeat, #FFF;
}

input[type=range].styled-slider.slider-progress:hover::-moz-range-track {
  background: linear-gradient(#00A460,#00A460) 0/var(--sx) 100% no-repeat, #F3F3F3;
}

/*ms*/
input[type=range].styled-slider::-ms-fill-upper {
  background: transparent;
  border-color: transparent;
}

input[type=range].styled-slider::-ms-fill-lower {
  background: transparent;
  border-color: transparent;
}

input[type=range].styled-slider::-ms-thumb {
  width: 17px;
  height: 17px;
  border-radius: 17px;
  background: #FFFFFF;
  border: 1px solid #7B7B7B;
  box-shadow: none;
  margin-top: 0;
  box-sizing: border-box;
}

input[type=range].styled-slider::-ms-track {
  height: 10px;
  border-radius: 8px;
  background: #FFF;
  border: 1px solid #b2b2b2;
  box-shadow: none;
  box-sizing: border-box;
}

input[type=range].styled-slider:hover::-ms-track {
  background: #F3F3F3;
}

input[type=range].styled-slider.slider-progress::-ms-fill-lower {
  height: max(calc(10px - 1px - 1px),0px);
  border-radius: 8px 0 0 8px;
  margin: -1px 0 -1px -1px;
  background: #00A460;
  border: 1px solid #b2b2b2;
  border-right-width: 0;
}
</style>