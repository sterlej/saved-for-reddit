import React from 'react'
import {ReactSelectize, SimpleSelect, MultiSelect} from 'react-selectize'
import _ from 'underscore'
import { PropTypes, Component } from 'react'

class MultiSelectFilter extends React.Component {

	render() {
		const { options, placeholder, name, search_value, selectedValues, onFilter, onRemove} = this.props
		return (
			<MultiSelect 
				options = {options.map(option => ({id: option.id, 
					value: option.name, label: option.name}))} 
				placeholder = {placeholder}
				values = {selectedValues}

				filterOptions = { (options, values, search) => {
			         return _.chain(options)
			            .filter(option => option.label.indexOf(search) > -1)
			            .map(option => { option.selectable = values.map(item => item.value)
			            	.indexOf(option.value) == -1 
			            	return option 
			            }).value()
			        }}

            	renderValue = { (item) => {
	                return <div className = "removable-value">
		                       <span style={{paddingLeft: 5}} onClick={() => onRemove(
									                       							search_value,
									                       							item,
									                       							name
									                       				 		)
		                       }> x   </span> 
		                       <span> {item.value} </span>
		                   </div>
            	}}

			    onValuesChange = { (values) => {
			    	onFilter(search_value, values, name)
            	}}>
		 	</MultiSelect>
		)
	}
}


const FilterBar = ({filters=[], onFilter=f=>f, onRemove=f=>f, search_value}) => {
	return (
		<div className="filter-bar">
	        {filters.map((filter, i) =>
	            <MultiSelectFilter key={i} 
	            				   placeholder={filter.placeholder}
	            				   name={filter.name}
	            				   options={filter.options}
	            				   selectedValues={filter.selectedValues}
	            				   onFilter={onFilter}
	            				   onRemove={onRemove}
	            				   search_value={search_value} /> 
	            		)
	    	}
	    </div> 
	)}
	

FilterBar.propTypes = {
	filters: PropTypes.array,
	onFilter: PropTypes.func
}

export default FilterBar
