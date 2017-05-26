import { Button }from 'react-bootstrap'
import { PropTypes } from 'react'

const AuthenticatePage = ({onClick=f=>f}) =>
	<div className="autenticate-page">
	 	<Button onClick={() => onClick()} href='api/accounts/authorize/'>Authenticate Account</Button>
	</div>
	


export default AuthenticatePage
