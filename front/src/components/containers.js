import { connect } from 'react-redux'
import SearchBar from './ui/SearchBar'
import SavedList from './ui/SavedList'
import FilterBar from './ui/FilterBar'
import AuthenticatePage from './ui/AuthenticatePage'
import { sortFunction } from '../lib/array-helpers'
import { toggleSaved, toggleSelected, removeSelected, authorizeUser, searchSaved } from '../actions'
import { Component } from 'react'


export const Search = connect(
    state => {
        return ({
                filters: [...state.filters],
                search: state.search
             })
    },

    dispatch => 
        ({
            onSearch(value, subreddit_ids) {
                dispatch(searchSaved(value, subreddit_ids))
            },
        }),
)(SearchBar)


const mapStateToProps = (state, ownProps) => {
    self.ownProps = {filters: state.filters}
    return {
        filters: [...state.filters],
        search_value: state.search
    }}

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        onFilter(search_value, selectedValues, filter_name) {
            dispatch(toggleSelected(selectedValues, filter_name))
            dispatch(searchSaved(search_value, selectedValues.map(s=>s.id)))
        },
        onRemove(search_value, selectedValue, filter_name) {
            var newValues = self.ownProps.filters.filter(s => s.name = 'subreddit')[0]
                                                 .selectedValues.filter(v => v.id != selectedValue.id)

            dispatch(toggleSelected(newValues, filter_name))
            dispatch(searchSaved(search_value, newValues.map(v=>v.id)))
        }
    }}

export const Filters = connect(
    mapStateToProps,
    mapDispatchToProps
)(FilterBar)


export const Saved = connect(
    state =>
        ({
            saved_list: [...state.saved].sort(sortFunction(state.sort)),
        }),

    dispatch => 
        ({
            onRemove(id, is_saved) {
                dispatch(toggleSaved(id, is_saved))
            },
        }),
)(SavedList)


export const UserInfo = connect(
    state => null,

    dispatch => 
        ({
            onClick() {
                null
            },
        }),
)(AuthenticatePage)
