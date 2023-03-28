import { h } from 'preact'
import { useState, useRef } from 'preact/hooks'
import style from './style.css'
import Chart from '../../components/chart'
import CopyButton from '../../components/copybutton'
import { type Point } from '../../utils/utils'

const Home = (): h.JSX.Element => {
  const [lastValue, setLastValue] = useState('?')
  const [lastDate, setLastDate] = useState('?')
  const [lastPopValue, setLastPopValue] = useState('?')
  const [lastPopDate, setLastPopDate] = useState('?')
  const startDateRef = useRef<HTMLInputElement>()
  const endDateRef = useRef<HTMLInputElement>()
  const chartBreed = useRef<Chart>()
  const chartPopAlive = useRef<Chart>()
  const chartPopDead = useRef<Chart>()
  const chartPopWorking = useRef<Chart>()

  const coefDataLoaded = (points: Point[]): void => {
    const lastPoint = points.slice(-1)[0]
    const minDate = new Date(points[0].x).toISOString().split('T')[0]
    const maxDate = new Date(lastPoint.x).toISOString().split('T')[0]
    // default view to last 7 days
    const initialFromDate = new Date()
    initialFromDate.setDate(new Date(lastPoint.x).getDate() - 7)
    if (startDateRef.current !== undefined) {
      startDateRef.current.setAttribute('min', minDate)
      startDateRef.current.setAttribute('max', maxDate)
      startDateRef.current.value = initialFromDate.toISOString().split('T')[0]
    }
    if (endDateRef.current !== undefined) {
      endDateRef.current.setAttribute('min', minDate)
      endDateRef.current.setAttribute('max', maxDate)
      endDateRef.current.value = maxDate
    }

    setLastValue((lastPoint.y / 1000).toString())
    setLastDate(new Date(lastPoint.x).toISOString())
  }

  const popDataLoaded = (points: Point[]): void => {
    const lastPoint = points.slice(-1)[0]
    setLastPopValue((lastPoint.y).toString())
    setLastPopDate(new Date(lastPoint.x).toISOString())
  }

  const dateRangeChanged = (): void => {
    [chartBreed, chartPopAlive, chartPopDead, chartPopWorking].forEach((chart) => {
      chart.current.setState({
        startDate: new Date(startDateRef.current.value),
        endDate: new Date(endDateRef.current.value)
      })
    })
  }

	return (
		<div class={style.home}>
			<h1>Tracking snailtrail coefficients</h1>
			<section>
				<Card size={2}>
					This shows breeding coefficent of <a href="https://www.snailtrail.art">SnailTrail</a> over time,
					more details can be found in the <a href="https://github.com/fopina/snailtrail-tools/">github project</a>
				</Card>
				<Card size={2}>
					Feel free to send any SLIME or AVAX over to
					<CopyButton copyTest='0xd991975e1C72E43C5702ced3230dA484442F195a'>
						<em>0xd991975e1C72E43C5702ced3230dA484442F195a</em>
					</CopyButton>
					if you find this useful!
				</Card>
			</section>
			<section>
				<Card title={`${lastValue  } %`}>
					Last value ({lastDate})
				</Card>
				<ChartCoef class={style.resource3} ref={chartBreed} label="Coefficient" url="https://raw.githubusercontent.com/fopina/snailtrail-tools/data/log.bin" onDataLoaded={coefDataLoaded} />
			</section>
			<section>
				<Card title={lastPopValue}>
					Last value ({lastPopDate})
				</Card>
				<ChartPop class={style.resource3} ref={chartPopAlive} label="Current Pop" url="https://raw.githubusercontent.com/fopina/snailtrail-tools/data/pop.alive.bin" onDataLoaded={popDataLoaded} />
			</section>
			<section>
				<Chart class={style.resource2} ref={chartPopDead} label="Burnt" url="https://raw.githubusercontent.com/fopina/snailtrail-tools/data/pop.dead.bin" />
				<Chart class={style.resource2} ref={chartPopWorking} label="Working" url="https://raw.githubusercontent.com/fopina/snailtrail-tools/data/pop.working.bin" />
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
  title?: string
  children: any
  size?: number
}

const Card = (props: CardProps): h.JSX.Element => {
  const styles = [style.resource]
  switch (props.size) {
    // FIXME: pass size directly to style...?
    case 1.5:
      styles.push(style.resourceMid)
      break
    case 2:
      styles.push(style.resource2)
      break
    case 3:
      styles.push(style.resource3)
      break
  }
  return (
    <div class={styles.join(' ')}>
      <h2>{props.title}</h2>
      <p>{props.children}</p>
    </div>
  )
}

class ChartPop extends Chart {
	componentDidMount(): void {
		super.componentDidMount();
		this.chartJS.data.datasets.push({label: "Drop Cap", data: [], borderColor: "red", backgroundColor: "red"});
	}
	componentDidUpdate(previousProps: Readonly<any>, previousState: Readonly<any>, snapshot: any): void {
		super.componentDidUpdate(previousProps, previousState, snapshot);
		if (this.state.points === undefined) return;
		const points = this.state.points.map((p: Point) => {
			return {x: p.x + 86400000, y: p.y + p.y * 0.2 / 30 }
		});
		console.log(this.state.points.slice(0, 2))
		console.log(points.slice(0, 2))
		this.chartJS.data.datasets[1].data = points;
		this.chartJS.update();
	}
}

class ChartCoef extends Chart {
	componentDidMount(): void {
		super.componentDidMount();
		this.chartJS.data.datasets.push({label: "Drop Cap", data: [], borderColor: "red", backgroundColor: "red"});
	}
	componentDidUpdate(previousProps: Readonly<any>, previousState: Readonly<any>, snapshot: any): void {
		super.componentDidUpdate(previousProps, previousState, snapshot);
		if (this.state.points === undefined) return;
		let lowest = Number.MAX_VALUE;
		let last = 0;
		const points = this.state.points.map((p: Point) => {
			if (p.y < last) lowest = p.y;
			last = p.y;
			return {x: p.x + 86400000, y: lowest * 1.1}
		});
		console.log(this.state.points.slice(0, 2))
		console.log(points.slice(0, 2))
		this.chartJS.data.datasets[1].data = points;
		this.chartJS.update();
	}
}

export default Home
