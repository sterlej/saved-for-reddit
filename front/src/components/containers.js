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


export const Filters = connect(
    state => {
        return ({
                filters: [...state.filters],
                search_value: state.search
             })
    },

    dispatch =>  ({
            onFilter(search_value, selectedValues, filter_name) {
                dispatch(toggleSelected(selectedValues, filter_name))
                dispatch(searchSaved(search_value, selectedValues.map(s=>s.id)))
            },

            onRemove(search_value, selectedValue, filter_name) {
                dispatch(removeSelected(selectedValue, filter_name))
                dispatch(searchSaved(search_value, [selectedValue.id]))
            },

        }),
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
