import { connect } from 'react-redux'
import SearchBar from './ui/SearchBar'
import SavedList from './ui/SavedList'
import AuthenticatePage from './ui/AuthenticatePage'
import { sortFunction } from '../lib/array-helpers'
import { toggleSaved, authorizeUser, searchSaved } from '../actions'
import { Component } from 'react'


export const Search = connect(
    state =>null,

    dispatch => 
        ({
            onSearch(value) {
                dispatch(searchSaved(value))
            },
        }),
)(SearchBar)


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
