export interface Point {
  x: number
  y: number
}

function _unpackLogBin (data): Point[] {
  const points: Point[] = []
  const x = new DataView(data)
  for (let i = 0; i < data.byteLength; i += 6) {
    points.push({ x: x.getUint32(i, false) * 1000, y: x.getUint16(i + 4, false) })
  }
  return points
}

function _unpackLongBin (data): Point[] {
  const points: Point[] = []
  const x = new DataView(data)
  for (let i = 0; i < data.byteLength; i += 8) {
    points.push({ x: x.getUint32(i, false) * 1000, y: x.getUint32(i + 4, false) })
  }
  return points
}

export async function loadData (url: string, longBin?: boolean): Promise<Point[]> {
  return await fetch(url)
    .then(async response => await response.arrayBuffer())
    .then(data => longBin ? _unpackLongBin(data) : _unpackLogBin(data))
}
