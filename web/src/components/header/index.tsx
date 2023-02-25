import { h } from 'preact';
import { Link } from 'preact-router/match';
import style from './style.css';

const Header = () => (
	<header class={style.header}>
		<a href="/" class={style.logo}>
			<img src="https://www.snailtrail.art/assets/img/logo.svg" alt="Snail Logo" />
			<h1>Tools</h1>
		</a>
		<nav>
			<Link activeClassName={style.active} href="/">
				Home
			</Link>
			<a href="https://github.com/fopina/snailtrail-tools" target="_blank">
				GitHub
			</a>
			<a href="https://www.snailtrail.art/" target="_blank">
				SnailTrail
			</a>
		</nav>
	</header>
);

export default Header;
