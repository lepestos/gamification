export default {
    state: {
        products: [],
        active_half: 'top',
        lots: [],
        write_off: '',
        referral_coeff: '',
        discount: '',
        ticket_amount: '',
        total_cost: '',
        ticket_price: '',
        min_profit: '',
        min_rentability: '',
        max_rentability: '',
        message: '',
    },
    mutations: {
        updateInput(state, value) {
            state.lots = value.lots;
            state.write_off = value.write_off;
            state.referral_coeff = value.referral_coeff;
            state.discount = value.discount;
            state.ticket_price = value.ticket_price;
            state.ticket_amount = value.ticket_amount;
        },
        updateOutput(state, value) {
            state.write_off = value.write_off;
            state.ticket_amount = value.ticket_amount;
            state.total_cost = value.total_cost;
            state.ticket_price = value.ticket_price;
            state.min_profit = value.min_profit;
            state.min_rentability = value.min_rentability;
            state.max_rentability = value.max_rentability;
            state.message = value.message;
        }
    },
    getters: {
        active_half(state) {
            return state.active_half;
        },
        lottery_input_data(state) {
            return {
                lots: state.lots,
                write_off: state.write_off,
                referral_coeff: state.referral_coeff,
                discount: state.discount,
                ticket_price: state.ticket_price,
                ticket_amount: state.ticket_amount,
            }
        },
        lottery_output_data(state) {
            return {
                write_off: state.write_off,
                ticket_amount: state.ticket_amount,
                total_cost: state.total_cost,
                ticket_price: state.ticket_price,
                min_profit: state.min_profit,
                min_rentability: state.min_rentability,
                max_rentability: state.max_rentability,
                message: state.message,
            }
        },
    },
    actions: {
        async sendLotteryRequest(ctx) {
            const url = "http://localhost:8000/api/v1/lottery/calculate/";
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.lottery_input_data)
            });
            if (response.ok) {
                const json = await response.json();
                console.log(json)
                ctx.commit('updateOutput', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
        },
        async calculateLotteryClicked(ctx,  form_input_data) {
            ctx.commit('updateInput', form_input_data)
            await this.dispatch('sendLotteryRequest', ctx)
        }
    }
}