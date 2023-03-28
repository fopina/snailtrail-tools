import { h } from 'preact'
import { Link } from 'preact-router/match'
import style from './style.css'
import baseroute from '../../baseroute'

const Header = () => (
	<header class={style.header}>
		<a href={`${baseroute}/`} class={style.logo}>
			<img src="https://www.snailtrail.art/assets/img/logo.svg" alt="Snail Logo" />
			<h1>Tools</h1>
		</a>
		<nav>
			<Link activeClassName={style.active} href={`${baseroute}/`}>
				Home
			</Link>
			<a href="https://github.com/fopina/snailtrail-tools" target="_blank" rel="noreferrer">
				GitHub
			</a>
			<a href="https://www.snailtrail.art/" target="_blank" rel="noreferrer">
				SnailTrail
			</a>
		</nav>
	</header>
)

export default Header
