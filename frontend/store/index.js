export const state = () => ({
  apiCount: 0,
})

export const mutations = {
  SET_apiCount(state, value) {
    state.apiCount = value
  },
}
