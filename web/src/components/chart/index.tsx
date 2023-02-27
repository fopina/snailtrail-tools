import { h, Component, createRef } from 'preact';
import { Chart as ChartJS } from 'chart.js/auto';
import { Point, loadData } from '../../utils/utils'
import "chartjs-adapter-date-fns";

interface ChartState {
	points: Point[];
	startDate?: any;
	endDate?: any;
}

interface ChartProps {
	url: string;
	label: string;
	onDataLoaded?: Function;
}

class Chart extends Component<ChartProps, ChartState> {
	chart = createRef();
	chartJS = null;

	componentDidMount(): void {
		this.chartJS = new ChartJS(this.chart.current, {
			type: 'line',
			data: {
				datasets: [
					{
						label: this.props.label,
						data: [],
					},
				]
			},
			options: {
				responsive: true,
				scales: {
					x: {
						type: 'time',
						time: {
							unit: 'day'
						},
					}
				}
			}
		});

		loadData(this.props.url).then(points => {
			this.setState({points: points})
			if (this.props.onDataLoaded) this.props.onDataLoaded(points);
		});
	}

	componentDidUpdate(previousProps: Readonly<any>, previousState: Readonly<ChartState>, snapshot: any): void {
		if (this.state.points === undefined) return;
		let startDate = this.state.startDate;

		if (startDate === undefined) {
			const initialFromDate = new Date();
        	initialFromDate.setDate(new Date(this.state.points.slice(-1)[0].x).getDate() - 7);
			startDate = initialFromDate;
		}

		this.chartJS.data.datasets[0].data = this.state.points;
		this.chartJS.options.scales.x.min = startDate;
		if (this.state.endDate) this.chartJS.options.scales.x.max = this.state.endDate;
		this.chartJS.update();
	}

	render() {
		return (
			<div class="chart">
				<canvas ref={this.chart} role="img" />
			</div>
		);
	}
};

export default Chart;
