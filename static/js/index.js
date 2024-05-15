const leaguePage = async () => {
  
  await leagueDetails('static/components/league-details/league-details.html')
    
  new Vue({
        el: '#vue',
        mixins: [windowMixin],
        data: function () {
          return {
            league: null,
            divisions: [],
            leagueDialog: {
              show: false,
              data: {}
            },
            divisionDialog: {
              show: false,
              data: {}
            }
          }
        },
        methods: {
          resetForms() {
            this.leagueDialog.data = {}
            this.divisionDialog.data = {}
          },
          editLeague(){
            this.leagueDialog.data = this.league
            this.leagueDialog.show = true
          },
          createLeague() {
            const data = this.leagueDialog.data
            const wallet = _.findWhere(this.g.user.wallets, {id: data.wallet})
            LNbits.api
              .request(
                'POST',
                '/sattrick/api/v1/league',
                wallet.adminkey,
                data
              )
              .then(res => {
                this.leagueDialog.show = false
                this.league = res.data
                this.resetForms()
                this.$q.notify({
                  message: 'League created successfully',
                  color: 'positive',
                  position: 'top'
                })
              })
              .catch(err => {
                this.$q.notify({
                  message: 'Error creating league',
                  color: 'negative',
                  position: 'top'
                })
              })
          },
          getDivisions() {
            if(!this.league) return
            const wallet = _.findWhere(this.g.user.wallets, {id: this.league.wallet})
            LNbits.api.request('GET', `/sattrick/api/v1/divisions`, wallet.inkey, null)
              .then(res => {
                this.divisions = res.data
                console.log(this.divisions.length)
              })
              .catch(err => {
                console.error(err)
              })
          },
          createDivision() {
            const data = this.divisionDialog.data
            data.rank = this.divisions.length + 1
            LNbits.api
              .request(
                'POST',
                `/sattrick/api/v1/${this.league.id}/division`,
                this.g.user.wallets[0].adminkey,
                data
              )
              .then(res => {
                this.divisionDialog.show = false
                this.divisions = [...this.divisions, res.data].sort((a, b) => a.rank - b.rank)
                this.resetForms()
                this.$q.notify({
                  message: 'Division created successfully',
                  color: 'positive',
                  position: 'top'
                })
              })
              .catch(err => {
                console.error(err)
                this.$q.notify({
                  message: 'Error creating division',
                  color: 'negative',
                  position: 'top'
                })
              })
          }
        },
        created() {
          this.countries = countries
          this.league = league
          this.getDivisions()    
        }
      })
}

leaguePage()