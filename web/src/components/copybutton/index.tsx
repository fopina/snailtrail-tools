import { h, Component, type ComponentChildren } from 'preact'
import { FontAwesomeIcon } from '@aduh95/preact-fontawesome'
import * as FAIcons from '@fortawesome/free-solid-svg-icons'

interface CopyButtonProps {
  copyTest?: string
  children: ComponentChildren
}

class CopyButton extends Component<CopyButtonProps> {
  clicked = (): void => {
    // eslint-disable-next-line @typescript-eslint/no-base-to-string
    const copyTest = this.props.copyTest ?? this.props.children?.toString()
    void navigator.clipboard.writeText(copyTest ?? '').then(
      () => {
        alert('Address copied to clipboard, thank you!')
      }
    )
  }

  render (): h.JSX.Element {
    return (
      <div>
        {this.props.children}
        <a href="#" onClick={this.clicked}>
          <FontAwesomeIcon icon={FAIcons.faClipboard} />
        </a>
      </div>
    )
  }
}

export default CopyButton
