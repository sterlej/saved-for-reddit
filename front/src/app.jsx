import React from 'react';
import '../styles/index.scss';
import { UserInfo, Saved, Search, Filters } from './components/containers'
// import SearchBar from './components/ui/SearchBar'
import { connect } from 'react-redux'
import { fetchSaved, fetchUser, searchSaved, fetchSubreddits } from './actions'
import cookie from 'react-cookie'


class App extends React.Component {
	constructor (props) {
		super(props)
	}

	componentWillMount() {
		const {dispatch, user} = this.props
		const access_token = cookie.load('at')

		dispatch(fetchSubreddits(access_token))
		dispatch(fetchUser(access_token))
		dispatch(fetchSaved(access_token))
	}
	
	render() {
		return (
		  <div>
		  	<UserInfo />
		  	<Search onSearch={searchSaved}/>
		  	<Filters />
		    <Saved />
		  </div>
		)
	}
}

function mapStateToProps(state) {
  const { saved, user, sort, filters, search } = state

  return {
    saved,
    user,
    filters,
    sort,
    search
  }
}

export default connect(mapStateToProps)(App)
