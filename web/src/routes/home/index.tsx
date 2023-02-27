import { h } from 'preact';
import { useState, useRef } from 'preact/hooks';
import style from './style.css';
import Chart from '../../components/chart';
import CopyButton from '../../components/copybutton';
import { Point } from '../../utils/utils';

const Home = () => {
	const [lastValue, setLastValue] = useState("?");
	const [lastDate, setLastDate] = useState("?");
	const startDateRef = useRef<HTMLInputElement>();
	const endDateRef = useRef<HTMLInputElement>();
	const chartBreed = useRef<Chart>();
	const chartPopAlive = useRef<Chart>();
	const chartPopDead = useRef<Chart>();
	const chartPopWorking = useRef<Chart>();

	const dataLoaded = ((points: Point[]) => {
		const lastPoint = points.slice(-1)[0];
		const minDate = new Date(points[0].x).toISOString().split('T')[0];
		const maxDate = new Date(lastPoint.x).toISOString().split('T')[0];
		// default view to last 7 days
		const initialFromDate = new Date();
		initialFromDate.setDate(new Date(lastPoint.x).getDate() - 7);
		if (startDateRef.current) {
			startDateRef.current.setAttribute("min", minDate);
			startDateRef.current.setAttribute("max", maxDate);
			startDateRef.current.value = initialFromDate.toISOString().split('T')[0];
		}
		if (endDateRef.current) {
			endDateRef.current.setAttribute("min", minDate);
			endDateRef.current.setAttribute("max", maxDate);
			endDateRef.current.value = maxDate;
		}

		setLastValue((lastPoint.y / 1000).toString());
		setLastDate(new Date(lastPoint.x).toISOString())
	})

	const dateRangeChanged = (() => {
		[chartBreed, chartPopAlive, chartPopDead, chartPopWorking].forEach((chart) => {
			chart.current.setState({
				startDate: new Date(startDateRef.current.value),
				endDate: new Date(endDateRef.current.value),
			});
		})
	});

	return (
		<div class={style.home}>
			<h1>Tracking snailtrail coefficients</h1>
			<section>
				<Card>
					This shows breeding coefficent of <a href="https://www.snailtrail.art">SnailTrail</a> over time,
					more details can be found in the <a href="https://github.com/fopina/snailtrail-tools/">github project</a>
				</Card>

				<Card>
					Feel free to send any SLIME or AVAX over to
					<CopyButton copyTest='0xd991975e1C72E43C5702ced3230dA484442F195a'>
						<em>0xd991975e1C72E43C5702ced3230dA484442F195a</em>
					</CopyButton>
					if you find this useful!
				</Card>
				<Card title={lastValue + ' %'}>
					Last value ({lastDate})
				</Card>
			</section>
			<section>
				<Chart ref={chartBreed} label="Coefficient" url="https://raw.githubusercontent.com/fopina/snailtrail-tools/data/log.bin" onDataLoaded={dataLoaded}></Chart>
				<Chart ref={chartPopAlive} label="Current Pop" url="https://raw.githubusercontent.com/fopina/snailtrail-tools/data/pop.alive.bin"></Chart>
				<Chart ref={chartPopDead} label="Burnt" url="https://raw.githubusercontent.com/fopina/snailtrail-tools/data/pop.dead.bin"></Chart>
				<Chart ref={chartPopWorking} label="Working" url="https://raw.githubusercontent.com/fopina/snailtrail-tools/data/pop.working.bin"></Chart>
			</section>
			<section>
				<table>
					<tr>
						<td>
							<input ref={startDateRef} onChange={dateRangeChanged} type="date" />
						</td>
						<td>
							to
						</td>
						<td>
							<input ref={endDateRef} onChange={dateRangeChanged} type="date" />
						</td>
					</tr>
				</table>
			</section>
		</div>
	);
};

interface CardProps {
	title?: string;
	children: any;
}

const Card = (props: CardProps) => {
	return (
		<div class={style.resource}>
			<h2>{props.title}</h2>
			<p>{props.children}</p>
		</div>
	);
};

export default Home;
