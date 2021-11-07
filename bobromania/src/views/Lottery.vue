<template>
  <div class="lottery">
    <lotteryInput/>
    <hr>
    <lotteryOutput/>
  </div>
</template>

<script>
import lotteryInput from "@/components/lottery-input.vue"
import lotteryOutput from "@/components/lottery-output.vue"

export default {
  name: "Lottery.vue",
  components: {
    lotteryInput,
    lotteryOutput,
  }
}
</script>

<style scoped lang="scss">

hr {
  @extend %standard-hr;
}

</style>