import C from '../constants'
import uuid from 'uuid'

export const user = (state={}, action) => {
    switch (action.type) {
        case C.REQUEST_USER :
            return {...state}

        case C.RECEIVE_USER :
            return {
                    ...state,
                    username: action.user.uid
            }

        default:
            return {...state}
    }
}


export const filters = (state=[], action) => {
    switch (action.type) {
        case C.REQUEST_SUBREDDITS :
            return [...state]

        case C.RECEIVE_SUBREDDITS :
            return [
                     ...state,
                     {
                        name: 'subreddit',
                        options: action.subreddits,
                        selectedValues: [],
                        placeholder: 'Subreddit'
                     }
                   ]

        case C.TOGGLE_SELECTED:
            state.filter(filt => filt.name == action.filter_name)
                 .map(filt => filt.selectedValues = action.selectedValues)
            return [...state]

        case C.REMOVE_SELECTED:
            var selectVals = state.filter(filt => filt.name == action.filter_name)[0].selectedValues
                 .filter(val => val.id != action.selectedValue.id)

            state.filter(filt => filt.name == action.filter_name)
                 .map(filt => filt.selectedValues = selectVals)
            return [...state]
                   
        default:
            return [...state]
    }
}


export const saved = (state = [], action) => {
    switch (action.type) {
        case C.TOGGLE_SAVED : 
            state.map(saved => { 
                if (saved.id == action.id) {
                    (saved.is_saved === true) ? saved.is_saved = false : saved.is_saved = true
                }})
            return [...state]

        case C.REQUEST_SAVED :
            return [...state]

        case C.RECEIVE_SAVED :
            return [
                    // ...state,
                    ...action.saved
                ]

        case C.ADD_SAVED_ATTRIBUTES : 
            return [...state]

        default:
            return [...state]
    }
}

export const sort = (state = "SORTED_BY_DATE", action) => {
    switch (action.type) {
        case "SORT_COLORS":
            return action.sortBy
        default :
            return state
    }
}

export const search = (state = "", action) => {
    switch (action.type) {
        case C.SEARCH_VALUE_CHANGED:
            return action.search
        default :
            return state
    }
}