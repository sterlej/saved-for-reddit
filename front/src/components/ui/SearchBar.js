import { PropTypes, Component } from 'react'

const SearchBar = ({filters=[], onSearch=f=>f}) => {

	var subreddit_filter = filters.filter(filt => filt.name = 'subreddit')[0]
	
	if (subreddit_filter) {
		var subreddit_ids = subreddit_filter.selectedValues.map(val => val.id)
	}
	else {
		var subreddit_ids = []
	}

	return (
		<div className="search-bar">
	        <input placeholder="search" onChange={event =>
	        	onSearch(event.target.value, subreddit_ids)} />
		</div>
)}

SearchBar.propTypes = {
	onSearch: PropTypes.func,
	filters: PropTypes.array
}

export default SearchBar