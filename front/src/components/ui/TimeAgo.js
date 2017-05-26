import { ago } from '../../lib/time-helpers'

const TimeAgo = ({timestamp}) => {
    return <span className="time-ago">
        { ago(timestamp) }
    </span>
}

export default TimeAgo