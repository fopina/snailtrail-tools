import { h, Component, createRef } from 'preact'
import { Chart as ChartJS } from 'chart.js/auto'
import { type Point, loadData } from '../../utils/utils'
import 'chartjs-adapter-date-fns'

interface ChartState {
  points: Point[]
  startDate?: any
  endDate?: any
}

interface ChartProps {
  url: string
  label: string
  onDataLoaded?: (points: Point[]) => void
  class?: string
}

class Chart extends Component<ChartProps, ChartState> {
  chart = createRef()
  chartJS: ChartJS | null = null

  componentDidMount (): void {
    this.chartJS = new ChartJS(this.chart.current, {
      type: 'line',
      data: {
        datasets: [
          {
            label: this.props.label,
            data: []
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day'
            }
          }
        }
      }
    })

    void loadData(this.props.url).then(points => {
      this.setState({ points })
      if (this.props.onDataLoaded != null) this.props.onDataLoaded(points)
    })
  }

  componentDidUpdate (previousProps: Readonly<any>, previousState: Readonly<ChartState>, snapshot: any): void {
    if (this.state.points === undefined) return
    let startDate = this.state.startDate

    if (startDate === undefined) {
      const initialFromDate = new Date()
      initialFromDate.setDate(new Date(this.state.points.slice(-1)[0].x).getDate() - 7)
      startDate = initialFromDate
    }

    if (this.chartJS?.options?.scales?.x) {
      this.chartJS.data.datasets[0].data = this.state.points
      this.chartJS.options.scales.x.min = startDate
      if (this.state.endDate !== undefined) this.chartJS.options.scales.x.max = this.state.endDate
      this.chartJS.update()
    }
  }

  render (): h.JSX.Element {
    return (
      <div class={`chart ${this.props.class ?? ''}`}>
        <canvas ref={this.chart} role="img" />
      </div>
    )
  }
}

export default Chart
