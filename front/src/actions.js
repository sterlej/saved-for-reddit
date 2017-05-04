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


export const searchSaved = (search_value) => dispatch => {
    console.log(search_value)
    const access_token = cookie.load('at')
    var res = fetch('api/saved/search/?q='.concat(search_value), {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer ".concat(access_token)
                  }})
          .then(response => response.json())
          // .then(json => console.log(json))
          .then(json => dispatch(receiveSaved(json)))
    // return {
    //     type: C.SEARCH_SAVED
    // }
    // return dispatch(receiveSaved([]))
}


export const sortColors = sortBy =>
    ({
        type: "SORT_COLORS",
        sortBy
    })


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
