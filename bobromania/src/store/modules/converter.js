export default {
    state: {
        rub_to_bobr: 1,
        bobr_to_rub: 1
    },
    mutations: {
        updateRubToBobr(state, value) {
            state.rub_to_bobr = value
            state.bobr_to_rub = ((value == 0) ? 0 : 1/value).toPrecision(1)
        },
        updateBobrToRub(state, value) {
            state.bobr_to_rub = value
            state.rub_to_bobr = ((value == 0) ? 0 : 1/value).toPrecision(1)
        }
    },
    getters: {
        course(state) {
            return {
                rub_to_bobr: state.rub_to_bobr,
                bobr_to_rub: state.bobr_to_rub
            }
        }
    },
    actions: {
        rub_to_bobr_changed(ctx, value) {
            ctx.commit('updateRubToBobr', value)
        },
        bobr_to_rub_changed(ctx, value) {
            ctx.commit('updateBobrToRub', value)
        }
    }
}