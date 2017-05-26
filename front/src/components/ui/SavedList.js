import { PropTypes, Component } from 'react'
import Saved from './Saved'
import AuthenticatePage from './AuthenticatePage'
import '../../../styles/index.scss';
import { fetchSaved } from '../../actions'

const SavedList = ({ saved_list=[], onRemove=f=>f }) =>
    <div className="saved-list">
        {(saved_list.length === 0) ?
            null:
            saved_list.map((saved, i) =>
                <Saved key={saved.id}
                    {...saved}
                    onRemove={() => onRemove(saved.id, saved.is_saved)} />
            )
        }
    </div>

SavedList.propTypes = {
    saved_list: PropTypes.array,
    onRemove: PropTypes.func
}

export default SavedList