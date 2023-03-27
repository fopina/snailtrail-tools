import { h } from 'preact';
import { Route, Router } from 'preact-router';


// Code-splitting is automated for `routes` directory
import Home from '../routes/home';
import Header from './header';

import baseroute from '../baseroute';

const App = () => (
	<div id="app">
		<Header />
		<main>
			<Router>
				<Route path={`${baseroute  }/`} component={Home} />
			</Router>
		</main>
	</div>
);

export default App;
