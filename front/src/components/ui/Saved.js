import { PropTypes, Component, dangerouslySetInnerHTML } from 'react'
import FaTrash from 'react-icons/lib/fa/trash-o'
import MdHighlightRemove from 'react-icons/lib/md/highlight-remove'

import '../../../styles/index.scss';
import { Button, ButtonGroup, Media, Row, Col } from 'react-bootstrap'
import TimeAgo from './TimeAgo'


const CommentButtons = ({comment_url, full_comments_url, is_saved, onRemove=f=>f}) => {
    const context_url = comment_url.concat("/?context=3") 
    return (
        <ButtonGroup bsSize="xsmall">
            <Button href={comment_url}>permalink</Button>
            <Button href={context_url}>context</Button>
            <Button href={full_comments_url}>full comments</Button>
            {
            (is_saved === true) ? 
            <Button onClick={onRemove}>unsave</Button> :  
            <Button onClick={onRemove}>save</Button>}
        </ButtonGroup>
        )
}


const SubmissionButtons = ({comments_url, is_saved, onRemove=f=>f}) => 
        <ButtonGroup bsSize="xsmall">
            <Button href={comments_url}>comments</Button>
            
            {(is_saved === true) ? 
                <Button onClick={onRemove}>unsave</Button> :
                <Button onClick={onRemove}>save</Button>
            }        
        </ButtonGroup>
        

const Comment  = ({comment_id, url, title, body_html, link_author, comment_author, subreddit, time_created}) =>
    <div className="comment" id={comment_id}>
        <Col xs={11} sm={11} md={11}>
            <h4><a href={url}>{title}</a></h4><span> by <a href={'https://www.reddit.com/user/'.concat(link_author)}>{link_author}</a> in 
                <a href={'https://www.reddit.com/r/'.concat(subreddit)}> {subreddit}</a> </span>
            <div>comment by <a href={'https://www.reddit.com/user/'.concat(comment_author)}>{comment_author}</a> <TimeAgo timestamp={time_created}/></div>
            <div dangerouslySetInnerHTML={{__html: body_html}} />
        </Col>
    </div>


const Submission = ({submission_id, thumbnail, url, title, author, time_created, subreddit, is_saved}) =>
    <div className="submission" id={submission_id}>
        {(thumbnail) ? 
        <Col xs={11} sm={11} md={2}>
                <a href={thumbnail} title="Lorem ipsum" className="thumbnail"><img src={thumbnail} /></a> 
        </Col>
        : null
        }
        <Col xs={11} sm={11} md={10}>
            <h4><a href={url}>{title}</a></h4>
            <div> submitted <TimeAgo timestamp={time_created} /> by <a href={'https://www.reddit.com/user/'.concat(author)}>{author}</a> in 
            <a href={'https://www.reddit.com/r/'.concat(subreddit)}> {subreddit}</a> </div>
        </Col>
    </div>


class Saved extends Component {

    render() {
        const { submission, comment, subreddit, author, author_flair, onRemove, created_utc, is_saved} = this.props
        return (
            <div>
                <Row className="saved">
                    {(submission) ?
                        <Submission id={submission.submission_id} thumbnail={submission.thumbnail} url={submission.url} title={submission.title} 
                                    author={author} time_created={created_utc} subreddit={subreddit.name}/> :
                        <Comment id={comment.comment_id} url={comment.link_url} title={comment.link_title} body_html={comment.body_html} 
                                 link_author={comment.link_author} comment_author={author} time_created={created_utc} subreddit={subreddit.name}/>
                    }
                    <div style={{'clear': 'left'}}>
                    {(submission) ?
                        <SubmissionButtons comments_url={submission.permalink} is_saved={is_saved} onRemove={onRemove} /> :
                        <CommentButtons comment_url={comment.permalink} full_comments_url={comment.full_comments_url}
                                is_saved={is_saved} onRemove={onRemove}/>

                    }
                    </div>
                </Row>
                
            </div>
        )
    }
}

Saved.propTypes = {
    // title: PropTypes.string.isRequired,
    onRemove: PropTypes.func,
}

Saved.defaultProps = {
    onRemove: f=>f,
}

export default Saved


