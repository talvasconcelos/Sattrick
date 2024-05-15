async function leagueDetails(path) {
  const template = await loadTemplateAsync(path)
  Vue.component('league-details', {
    name: 'league-details',
    props: ['league-id'],
    template,

    data: function () {
      return {}
    },
    methods: {
      deleteLeague() {
        console.log('delete league')
      },
    },
    created() {
      
    }
  })
}
