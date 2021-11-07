export default {
    state: {
        products: [],
        active_half: 'top',
        lot_cost: {
            cheap: '',
            middle: '',
            costly: '',
        },
        loyalty: '',
        rentability: '',
        amounts: {
            cheap: '',
            middle: '',
            costly: '',
        },
        percents: {
            cheap: '',
            middle: '',
            costly: '',
        },
        black_box_cost: {
            min: 0,
            cur: 0,
            max: 0
        },
        message: '',
        black_box_name: '',
        saved_black_boxes: ''
    },
    mutations: {
        updateActiveHalf(state, value) {
            state.active_half = value;
        },
        updateCost(state, value) {
            state.lot_cost = value;
        },
        updateLoyalty(state, value) {
            state.loyalty = value;
        },
        updateRentability(state, value) {
            state.rentability = value;
        },
        updateCostlyAmount(state, value) {
            state.amounts.costly = value;
        },
        updatePercents(state, value) {
           state.percents = value;
        },
        updateAmounts(state, value) {
           state.amounts = value;
        },
        updateBlackBoxCost(state, value) {
           state.black_box_cost = value;
        },
        updateMessage(state, value) {
            state.message = value;
        },
        updateProducts(state, value) {
            state.products = value;
        },
        updateBlackBoxName(state, value) {
            state.black_box_name = value;
        },
        updateSavedBoxes(state, value) {
            state.saved_black_boxes = value;
        }
    },
    getters: {
        active_half(state) {
            return state.active_half;
        },
        input_data(state) {
            return {
                lot_cost: state.lot_cost,
                loyalty: state.loyalty,
                rentability: state.rentability,
                costly_amount: state.amounts.costly,
                black_box_cost: state.black_box_cost.cur,
            }
        },
        output_data(state) {
            return {
                percents: state.percents,
                amounts: state.amounts,
                black_box_cost: state.black_box_cost,
            }
        },
        recalculate_data(state) {
            return {
                loyalty: state.loyalty,
                rentability: state.rentability,
                black_box_cost: state.black_box_cost,
                message: state.message,
            }
        },
        products(state) {
            return state.products;
        },
        save_data(state) {
            return {
                name: state.black_box_name,
                price: state.black_box_cost.cur,
                lot_cost: state.lot_cost,
                lot_amount: state.amounts,
                //loyalty: state.loyalty,
                //rentability: state.rentability,
            }
        },
        saved_boxes(state) {
            return state.saved_black_boxes
        }
    },
    actions: {
        async sendRequest(ctx) {
            const url = "http://localhost:8000/api/v1/black-box/calculate/";
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.input_data)
            });
            if (response.ok) {
                const json = await response.json();
                console.log(json)
                ctx.commit('updatePercents', json.probabilities)
                ctx.commit('updateAmounts', json.amounts)
                ctx.commit('updateBlackBoxCost', json.black_box_cost)
                ctx.commit('updateMessage', json.message)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
        },
        async calculateParametersClicked(ctx,  form_input_data) {
            ctx.commit('updateCost', form_input_data.lot_cost)
            ctx.commit('updateLoyalty', form_input_data.loyalty)
            ctx.commit('updateRentability', form_input_data.rentability)
            ctx.commit('updateCostlyAmount', form_input_data.costly_amount)

            await this.dispatch('sendRequest', ctx)

            ctx.commit('updateActiveHalf', 'bottom')
        },
        async recalculateParametersClicked(ctx,  form_recalc_data) {
            ctx.commit('updateLoyalty', form_recalc_data.loyalty)
            ctx.commit('updateRentability', form_recalc_data.rentability)
            ctx.commit('updateBlackBoxCost', form_recalc_data.black_box_cost)

            ctx.commit('updateActiveHalf', 'none')
            await this.dispatch('sendRequest', ctx)
            ctx.commit('updateActiveHalf', 'bottom')
        },
        blackBoxReset(ctx) {
            ctx.commit('updateLoyalty', 0.6)
            ctx.commit('updateRentability', 0.15)
            ctx.commit('updateCost', {cheap: '', middle: '', costly: ''})
            ctx.commit('updateAmounts', {cheap: '', middle: '', costly: ''})
            ctx.commit('updateBlackBoxCost', {min: '', cur: 0, max: ''})
            ctx.commit('updatePercents', {cheap: '', middle: '', costly: ''})
            ctx.commit('updateActiveHalf', 'none')
            ctx.commit('updateActiveHalf', 'top')
        },
        async loadProducts(ctx) {
            const url = "http://localhost:8000/api/v1/product/";
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            });
            if (response.ok) {
                const json = await response.json();
                console.log(json)
                ctx.commit('updateProducts', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
        },
        async saveBlackBox(ctx, name) {
            ctx.commit('updateBlackBoxName', name)
            const url = "http://localhost:8000/api/v1/black-box/";
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ctx.getters.save_data)
            });
            if (response.ok) {
                const json = await response.json();
                console.log(json)
                ctx.dispatch('blackBoxReset')
                ctx.dispatch('loadBlackBoxes')
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
        },
        async loadBlackBoxes(ctx) {
            const url = "http://localhost:8000/api/v1/black-box/";
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            });
            if (response.ok) {
                const json = await response.json();
                console.log(json)
                ctx.commit('updateSavedBoxes', json)
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
        },
        async deleteBlackBox(ctx, id) {
            const url = `http://localhost:8000/api/v1/black-box/${id}`;
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            });
            if (response.ok) {
                console.log('delete OK')
                ctx.dispatch('loadBlackBoxes')
            } else {
                console.log("Ошибка HTTP: " + response.status);
                const json = await response.json();
                console.log(json);
            }
        }
    }
}