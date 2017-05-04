import React from 'react';
import '../styles/index.scss';
import { UserInfo, Saved, Search } from './components/containers'
// import SearchBar from './components/ui/SearchBar'
import { connect } from 'react-redux'
import { fetchSaved, fetchUser, searchSaved } from './actions'
import cookie from 'react-cookie'


class App extends React.Component {
	constructor (props) {
		super(props)
	}

	componentWillMount() {
		const {dispatch, user} = this.props
		const access_token = cookie.load('at')

		dispatch(fetchUser(access_token))
		dispatch(fetchSaved(access_token))
	}
	
	render() {
		return (
		  <div>
		  	<UserInfo />
		  	<Search onSearch={searchSaved}/>
		    <Saved />
		  </div>
		)
	}
}

function mapStateToProps(state) {
  const { saved, user, sort } = state

  return {
    saved,
    user,
    sort
  }
}

export default connect(mapStateToProps)(App)
