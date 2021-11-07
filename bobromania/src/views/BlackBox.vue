<template>
  <div class="black-box">
    <black-box-input :class="{transparent: this.active_half() === 'bottom'}"/>
    <hr>
    <black-box-output :class="{transparent: this.active_half() === 'top'}"/>
    <transition appear name="fade">
      <black-box-recalculate v-if="this.active_half() === 'bottom'"/>
    </transition>
    <hr>
    <black-box-table/>
  </div>
</template>

<script>
import blackBoxInput from "../components/black-box-input.vue"
import blackBoxOutput from "../components/black-box-output.vue"
import blackBoxRecalculate from "../components/black-box-recalculate.vue"
import blackBoxTable from "../components/black-box-table.vue"
import {mapGetters} from 'vuex'
export default {
  name: "BlackBox.vue",
  components: {
    blackBoxInput,
    blackBoxOutput,
    blackBoxRecalculate,
    blackBoxTable
  },
  methods: mapGetters(['active_half'])
}
</script>

<style scoped lang="scss">

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

hr {
  @extend %standard-hr;
}

.transparent {
  opacity: .3;
}

</style>