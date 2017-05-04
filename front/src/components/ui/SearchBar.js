import { PropTypes, Component } from 'react'

const SearchBar = ({onSearch=f=>f}) => 
	<div className="search-bar">
        <input placeholder="search" onChange={event =>
        	onSearch(event.target.value)} />
	</div>

SearchBar.propTypes = {
	onSearch: PropTypes.func
}

export default SearchBar