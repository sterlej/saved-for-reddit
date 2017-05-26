import C from './constants'
import { v4 } from 'uuid'
import fetch from 'isomorphic-fetch'
import { push } from 'react-router-redux'
import { browserHistory } from 'react-router'
import cookie from 'react-cookie'


export const toggleSaved = (id, is_saved) => {
    const access_token = cookie.load('at')
    const not_is_saved = !is_saved
    fetch('api/saved/delete/'.concat(id), {
          method: "PUT",
          body: JSON.stringify({is_saved: not_is_saved}),
          headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer ".concat(access_token)
                    }})
    return {
        type: C.TOGGLE_SAVED,
        id,
        not_is_saved
    }
}


export const searchSaved = (search_value='', subreddit_ids=[]) => dispatch => {
    const access_token = cookie.load('at')
    if (subreddit_ids.length !== 0 && search_value) {
      var query = "?q=".concat(search_value).concat("&sid=").concat(subreddit_ids.join('&sid='))
    } 

    else if (subreddit_ids.length !== 0){
      var query = "?".concat("sid=").concat(subreddit_ids.join('&sid='))
    }

    else {
      var query = "?q=".concat(search_value) 
    }                

    var res = fetch('api/saved/search/'.concat(query), {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer ".concat(access_token)
                  }})
          .then(response => response.json())
          .then(json => dispatch(receiveSaved(json)))
          .then(() => dispatch(seachValueChanged(search_value)))
}


export const seachValueChanged = search_value =>
    ({
        type: C.SEARCH_VALUE_CHANGED,
        search: search_value
    })


export const sortColors = sortBy =>
    ({
        type: "SORT_COLORS",
        sortBy
    })


const requestSubreddits = access_token => 
    ({
        type: C.REQUEST_SUBREDDITS,
        access_token
    })


export const receiveSubreddits = subreddits => 
    ({
        type: C.RECEIVE_SUBREDDITS,
        subreddits: subreddits.map(subreddit => ({
                                      ...subreddit,
                                      selected: false
                                  })),
        receivedAt: Date.now()
    })
  


export const fetchSubreddits =  access_token => dispatch => {
    dispatch(requestSubreddits(access_token))
    return fetch('api/saved/subreddits', {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer ".concat(access_token)
                  }})
      .then(response => response.json())
      .then(json => dispatch(receiveSubreddits(json)))
    }


// [{id, selected}]
export const toggleSelected = (selectedValues, filter_name) => 
     ({
        type: C.TOGGLE_SELECTED,
        selectedValues,
        filter_name
     })


export const removeSelected = (selectedValue, filter_name, vals) => 
     {
     return {
        type: C.REMOVE_SELECTED,
        selectedValue,
        filter_name
     }
   }


const requestSaved = access_token => 
    ({
        type: C.REQUEST_SAVED,
        access_token
    })


export const receiveSaved = saved =>
    ({
        type: C.RECEIVE_SAVED,
        saved,
        receivedAt: Date.now()
    })


export const fetchSaved =  access_token => dispatch => {
    dispatch(requestSaved(access_token))
    return fetch('api/saved/', {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer ".concat(access_token)
                  }})
      .then(response => response.json())
      .then(json => dispatch(receiveSaved(json)))
    }


const requestUser = access_token => 
    ({
        type: C.REQUEST_USER,
        access_token
    })


export const receiveUser = user =>
    ({
        type: C.RECEIVE_USER,
        receivedAt: Date.now(),
        user
    })


export const fetchUser = access_token => dispatch =>
    {
        dispatch(requestUser(access_token))
        return fetch('api/accounts/user', {
                      method: "GET",
                      headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer ".concat(access_token)
                      }})
          .then(response => response.json())
          .then(json => dispatch(receiveUser(json)))
    }


// export function fetchPostsIfNeeded(subreddit) {
//   return (dispatch, getState) => {
//     if (shouldFetchPosts(getState(), subreddit)) {
//       return dispatch(fetchPosts(subreddit))
//     }
//   }
// }
