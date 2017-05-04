import { createStore, combineReducers, applyMiddleware } from 'redux'
import { sort, saved, user} from './reducers'
import { fetchSaved } from '../actions'
import stateData from '../../data/initialState.json'
import {createLogger} from 'redux-logger'
import thunk from 'redux-thunk'
import thunkMiddleware from 'redux-thunk';

const loggerMiddleware = createLogger()

const saver = store => next => action => {
    let result = next(action)
    // localStorage['redux-store'] = JSON.stringify(store.getState())
    return result
}

const storeFactory = (initialState={stateData}) =>
    applyMiddleware(thunk, loggerMiddleware)(createStore)(
        combineReducers({sort, saved, user}), stateData)
    //     (!localStorage['redux-store']) ?
    //         JSON.parse(localStorage['redux-store']) :
    //         stateData
    // )

export default storeFactory
